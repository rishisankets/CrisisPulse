import math
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from app.models.schemas import RegionFeatureVector
from app.database import (
    get_db_connection,
    record_gap_score,
    get_latest_gap_scores,
    get_cached_api_response,
    set_cached_api_response
)

logger = logging.getLogger(__name__)

class AnalyticsEngine:
    """Analytical engine computing:
    1. Attention-Response Gap Score (0.0 to 10.0 scale)
    2. Hotspot archetype categorization (Neglected Emergency, Escalating Hotspot, Protracted Crisis, Stabilized Response)
    3. Anomaly detection via Isolation Forest on multi-dimensional feature vectors.
    """

    def calculate_gap_score(self, vector: RegionFeatureVector) -> float:
        """Calculates normalized attention-response disparity score.
        
        High media volume + low humanitarian response + negative tone -> High Gap Score (e.g., Sudan, Haiti)
        High media volume + high humanitarian response -> Lower Gap Score (proportional response)
        Low media volume + high humanitarian response -> Well-served or aid-established
        
        Formula:
          Media Factor: log(vol_24h + 1) * volume_ratio
          Response Factor: log(reliefweb_response_count + 1)
          Severity Factor: max(0.1, -1 * avg_goldstein) / 10.0 (Goldstein negative = conflict)
          Raw Gap = (Media Factor / (Response Factor + 1)) * (1.0 + Severity Factor)
          Normalized to 0.0 - 10.0 range.
        """
        vol_24h = max(1, vector.event_volume_24h)
        resp_count = max(0, vector.reliefweb_response_count)
        vol_ratio = max(0.2, min(5.0, vector.volume_ratio))
        goldstein = vector.avg_goldstein  # typically -10.0 to +10.0

        # Conflict severity multiplier (conflict intensity elevates urgency)
        severity_multiplier = 1.0 + max(0.0, (-goldstein) / 10.0)

        # Disparity index
        media_intensity = math.log10(vol_24h + 10) * vol_ratio
        response_saturation = math.log10(resp_count + 5)

        raw_score = (media_intensity / response_saturation) * severity_multiplier
        
        # Scale to 0.0 - 10.0
        gap_score = round(min(10.0, max(0.0, raw_score * 2.2)), 2)
        return gap_score

    def classify_hotspot(self, vector: RegionFeatureVector, gap_score: float) -> str:
        """Categorizes crisis region based on gap score, response level, and volume dynamics:
        - Neglected Emergency: High media spike or severe conflict, but disproportionately low UN response (gap_score >= 6.5)
        - Escalating Hotspot: High volume ratio (sudden surge > 1.4) or strong negative goldstein trend (< -1.0)
        - Protracted Crisis: Sustained volume with steady moderate humanitarian presence
        - Stabilized / High-Aid: High humanitarian response volume relative to media attention
        """
        if gap_score >= 6.8 and vector.reliefweb_response_count < 35:
            return "Neglected Emergency"
        elif vector.volume_ratio >= 1.35 or vector.goldstein_trend <= -0.8:
            return "Escalating Hotspot"
        elif vector.reliefweb_response_count >= 40 and vector.volume_ratio < 1.1:
            return "Stabilized Response"
        else:
            return "Protracted Crisis"

    def detect_anomalies(self, feature_vectors: List[RegionFeatureVector]) -> Dict[str, bool]:
        """Runs unsupervised Isolation Forest anomaly detection across regional feature sets.
        Flags regions exhibiting outlier combinations (e.g., severe sentiment drop + media surge).
        """
        if len(feature_vectors) < 4:
            # Insufficient samples for statistically valid Isolation Forest, return default
            return {v.region: False for v in feature_vectors}

        try:
            # Features: [vol_24h, vol_ratio, avg_goldstein, goldstein_trend, tone_volatility, reliefweb_response_count]
            X = np.array([
                [
                    float(v.event_volume_24h),
                    float(v.volume_ratio),
                    float(v.avg_goldstein),
                    float(v.goldstein_trend),
                    float(v.tone_volatility),
                    float(v.reliefweb_response_count)
                ]
                for v in feature_vectors
            ], dtype=np.float64)

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)  # type: ignore[arg-type]

            # Contamination set to ~15-20% outlier rate
            clf = IsolationForest(contamination=0.2, random_state=42)
            preds = clf.fit_predict(X_scaled)  # -1 for anomaly, 1 for inlier

            return {feature_vectors[i].region: bool(preds[i] == -1) for i in range(len(feature_vectors))}
        except Exception as e:
            logger.warning(f"Anomaly detection fallback to heuristic due to: {e}")
            # Heuristic fallback: outlier if volume_ratio > 1.8 or tone_volatility > 3.0
            return {
                v.region: bool(v.volume_ratio > 1.8 or v.tone_volatility > 3.0)
                for v in feature_vectors
            }

    def process_and_persist(self, feature_vectors: List[RegionFeatureVector]) -> List[Dict[str, Any]]:
        """Computes gap scores, archetypes, and anomaly flags for all regions and writes snapshots to SQLite."""
        anomalies_map = self.detect_anomalies(feature_vectors)
        results = []
        now_str = datetime.now(timezone.utc).isoformat()

        with get_db_connection() as conn:
            cursor = conn.cursor()
            for v in feature_vectors:
                gap = self.calculate_gap_score(v)
                category = self.classify_hotspot(v, gap)
                is_anomaly = anomalies_map.get(v.region, False)

                # Persist gap score
                cursor.execute(
                    """
                    INSERT INTO gap_score_cache (region, gap_score, media_volume, response_volume, computed_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (v.region, gap, v.event_volume_24h, v.reliefweb_response_count, now_str)
                )

                # Persist classification
                cursor.execute(
                    """
                    INSERT INTO region_classifications (region, category, is_anomaly, computed_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (v.region, category, 1 if is_anomaly else 0, now_str)
                )

                results.append({
                    "region": v.region,
                    "country_code": v.country_code,
                    "lat": v.lat,
                    "lon": v.lon,
                    "gap_score": gap,
                    "category": category,
                    "is_anomaly": is_anomaly,
                    "media_volume_24h": v.event_volume_24h,
                    "reliefweb_response_count": v.reliefweb_response_count,
                    "volume_ratio": v.volume_ratio,
                    "avg_goldstein": v.avg_goldstein,
                    "tone_volatility": v.tone_volatility,
                    "computed_at": now_str
                })

        return sorted(results, key=lambda x: x["gap_score"], reverse=True)

    def get_persisted_classifications(self) -> List[Dict[str, Any]]:
        """Retrieves most recent classification and anomaly status per region."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT rc.region, rc.category, rc.is_anomaly, rc.computed_at
                FROM region_classifications rc
                INNER JOIN (
                    SELECT region, MAX(computed_at) as max_comp
                    FROM region_classifications
                    GROUP BY region
                ) latest ON rc.region = latest.region AND rc.computed_at = latest.max_comp
                ORDER BY rc.region ASC
            """)
            return [
                {
                    "region": row["region"],
                    "category": row["category"],
                    "is_anomaly": bool(row["is_anomaly"]),
                    "computed_at": row["computed_at"]
                }
                for row in cursor.fetchall()
            ]
