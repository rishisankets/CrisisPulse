# CrisisPulse — Global Conflict & Humanitarian Response Tracker

CrisisPulse is a research-grade, full-stack intelligence platform that bridges the gap between global media attention and boots-on-the-ground humanitarian response. By continuously fusing **GDELT 2.0** (monitoring global broadcast, print, and web news) with **UN OCHA ReliefWeb** (tracking UN humanitarian appeals, situation reports, and funding allocations), CrisisPulse quantifies the "attention-response gap" to identify under-reported crises and overlooked emergencies worldwide.

---

## System Architecture

```
                               ┌────────────────────────────────┐
                               │       CrisisPulse Frontend     │
                               │  (React, Vite, Leaflet, D3)    │
                               └───────────────┬────────────────┘
                                               │ HTTP / REST
                                               ▼
                               ┌────────────────────────────────┐
                               │       FastAPI REST Backend     │
                               │        (Python 3.13)           │
                               └───────┬───────────────┬────────┘
                                       │               │
            ┌──────────────────────────┴────┐    ┌─────┴────────────────────────┐
            ▼                               ▼    ▼                              ▼
 ┌──────────────────────┐        ┌──────────────────────┐        ┌──────────────────────┐
 │    GDELT 2.0 API     │        │    ReliefWeb v2      │        │    SQLite Database   │
 │ (Doc API / Tone /    │        │ (UN OCHA Reports &   │        │   (Users, Caches,    │
 │  Media Volume)       │        │  Appeals)            │        │    Feature Vectors)  │
 └──────────────────────┘        └──────────────────────┘        └──────────────────────┘
```

---

## Week 1 Milestone: Foundations & Data Layer

### Core Deliverables Completed
1. **Repository & Backend Scaffolding**: Structured FastAPI application with modular services, configuration, and API routing.
2. **SQLite Schema with WAL Mode**: Initialized persistent SQLite database (`crisispulse.db`) with core tables:
   - `users`: User authentication records.
   - `watchlists`: User tracked countries and crises.
   - `gap_score_cache`: Historical snapshots of attention vs. response gap scores.
   - `region_classifications`: Hotspot cluster categories and anomaly flags.
   - `session_tokens`: JWT user session management.
   - `api_cache`: 30-minute TTL response cache mitigating external API rate limits.
3. **Resilient GDELT 2.0 API Client**:
   - Fetches global crisis and conflict news articles with title sentiment analysis.
   - Normalizes raw article objects with tone and Goldstein conflict-cooperation intensity scores.
   - Implements automated cache lookup and HTTP 429 throttling backoff with reference hotspot fallbacks.
4. **UN OCHA ReliefWeb v2 Client**:
   - Queries emergency situation reports, appeals, and country response activity levels.
   - Addresses ReliefWeb API changes (v1 decommissioning and v2 pre-approved appname requirements).
5. **Multi-dimensional Aggregation Engine**:
   - Combines raw GDELT events across time horizons (24h vs. 7d) with ReliefWeb response counts.
   - Calculates ML-ready feature vectors:
     - `event_volume_24h` (media activity)
     - `event_volume_7d` (baseline media volume)
     - `volume_ratio` ($24\text{h volume} / \text{daily baseline}$)
     - `avg_goldstein` (mean conflict/cooperation intensity $[-10, +10]$)
     - `goldstein_trend` (short-term escalation delta)
     - `tone_volatility` (standard deviation of sentiment)
     - `reliefweb_response_count` (humanitarian presence)

---

---

## Week 2 Milestone: Analytical & ML Intelligence Core

### Core Deliverables Completed
1. **Attention-Response Gap Score Calculation Engine**:
   - Quantifies the disparity between media volume and humanitarian response saturation:
     $$\text{Gap Score} = \min\left(10, \frac{\log_{10}(\text{Volume}_{24\text{h}} + 10) \times \text{Volume Ratio}}{\log_{10}(\text{Response Count} + 5)} \times \left(1 + \frac{\max(0, -\text{Goldstein})}{10}\right) \times 2.2\right)$$
   - Disparity indices range strictly from $0.0$ (proportional response/stable) to $10.0$ (severe attention-response gap, e.g. under-aided active warzones).
   - Real-time snapshots are automatically persisted to the SQLite `gap_score_cache` table.
2. **Crisis Archetype Classification**:
   - Classifies hotspots into operational humanitarian archetypes:
     - `Neglected Emergency`: Severe conflict intensity and high attention gap with critically low UN response (<35 reports/appeals).
     - `Escalating Hotspot`: Rapid surge in media volume ratio (>1.35) or sharp negative Goldstein sentiment trend (<-0.8).
     - `Protracted Crisis`: Sustained baseline activity with moderate humanitarian presence.
     - `Stabilized Response`: High relative response saturation and balanced reporting.
3. **Unsupervised Outlier & Anomaly Detection**:
   - Deploys **scikit-learn Isolation Forest** (`contamination=0.2`) across multi-dimensional regional vectors (`event_volume_24h`, `volume_ratio`, `avg_goldstein`, `goldstein_trend`, `tone_volatility`, `reliefweb_response_count`).
   - Identifies acute statistical anomalies (e.g. sharp sentiment collapses with zero response increase).
   - Records outputs in the `region_classifications` table.
4. **Analytics REST API**:
   - `GET /api/analytics/overview`: Real-time computed gap scores, archetype counts, anomaly alerts, and full breakdown.
   - `GET /api/analytics/gap-scores`: Current ranking of regions ordered by attention-response gap score.
   - `GET /api/analytics/anomalies`: Filtered list of regions triggering Isolation Forest anomaly detection.
   - `GET /api/analytics/classifications`: Historical and current archetype assignments from SQLite.

---

## API Reference

### Week 1 Endpoints (Data Layer)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status and root navigation |
| `GET` | `/api/health` | SQLite connectivity and data service health check |
| `GET` | `/api/gdelt/raw` | Query raw and normalized GDELT news events |
| `GET` | `/api/reliefweb/raw` | Query raw and normalized UN OCHA ReliefWeb reports |
| `GET` | `/api/data/aggregated` | Compute and return per-region feature vectors |

### Week 2 Endpoints (Analytics & ML Intelligence Layer)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/analytics/overview` | Full intelligence summary: gap scores, archetypes, and anomalies |
| `GET` | `/api/analytics/gap-scores` | Ranked list of crisis regions by attention-response gap |
| `GET` | `/api/analytics/anomalies` | Detected outlier regions via Isolation Forest |
| `GET` | `/api/analytics/classifications` | Persisted archetype classifications from SQLite |

---

## Real-world Findings & Known Limitations (Report Section)

1. **GDELT Noise & Rate Limiting**:
   - *Observation*: GDELT Doc 2.0 API enforces tight per-IP rate limits (HTTP 429). Furthermore, at the individual-article level, automated machine translation and event coding can produce false positives.
   - *Mitigation*: CrisisPulse aggregates news trends across hundreds of events per region rather than relying on individual items. Queries are cached in SQLite with a 30-minute TTL, and 429 errors trigger a non-blocking fallback with curated baseline data.
2. **ReliefWeb API Evolution**:
   - *Observation*: The legacy ReliefWeb `v1` endpoint has been decommissioned (`410 Gone`). The modern `v2` endpoint requires a pre-approved `appname` obtained through an official UN OCHA request form.
   - *Mitigation*: The backend exposes a configurable `RELIEFWEB_APPNAME` in `.env`. When running in development without a registered appname, the service gracefully degrades to verified UN OCHA situation reports while logging clear setup instructions.

---

## Local Development Setup

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Tests
```bash
python -m pytest tests/ -v
```

### 3. Start Development Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive Swagger documentation is available at `http://localhost:8000/docs`.
