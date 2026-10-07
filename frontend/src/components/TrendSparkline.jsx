import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { fetchRegionTrends } from '../services/api';

export default function TrendSparkline({ regionName, compact = true, initialTrends = null }) {
  const [trends, setTrends] = useState(initialTrends);
  const [loading, setLoading] = useState(!initialTrends);

  useEffect(() => {
    if (initialTrends) {
      setTrends(initialTrends);
      return;
    }
    let isMounted = true;
    async function load() {
      setLoading(true);
      const data = await fetchRegionTrends(regionName);
      if (isMounted && data) {
        setTrends(data);
      }
      if (isMounted) setLoading(false);
    }
    load();
    return () => { isMounted = false; };
  }, [regionName, initialTrends]);

  if (loading || !trends || !trends.history || trends.history.length === 0) {
    return <span className="sparkline-placeholder">...</span>;
  }

  const { history, trajectory, delta_24h } = trends;
  const scores = history.map(h => h.gap_score);
  const minScore = Math.min(...scores);
  const maxScore = Math.max(...scores);
  const range = maxScore - minScore || 1;

  // SVG dimensions
  const width = compact ? 64 : 140;
  const height = compact ? 22 : 36;
  const padding = 3;

  const points = history.map((pt, idx) => {
    const x = padding + (idx / (history.length - 1)) * (width - 2 * padding);
    const y = height - padding - ((pt.gap_score - minScore) / range) * (height - 2 * padding);
    return `${x},${y}`;
  }).join(' ');

  const strokeColor =
    trajectory === 'widening' ? '#ef4444' :
    trajectory === 'closing' ? '#10b981' : '#38bdf8';

  const TrajectoryIcon =
    trajectory === 'widening' ? TrendingUp :
    trajectory === 'closing' ? TrendingDown : Minus;

  const trajectoryLabel =
    trajectory === 'widening' ? `+${delta_24h} (widening)` :
    trajectory === 'closing' ? `${delta_24h} (closing)` : '±0.0 (stable)';

  if (compact) {
    return (
      <div className="sparkline-compact-wrap" title={`24h Trajectory: ${trajectoryLabel}`}>
        <svg width={width} height={height} className="sparkline-svg">
          <polyline
            fill="none"
            stroke={strokeColor}
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            points={points}
          />
          {/* Last point pulse dot */}
          {history.length > 0 && (
            <circle
              cx={padding + (width - 2 * padding)}
              cy={height - padding - ((history[history.length - 1].gap_score - minScore) / range) * (height - 2 * padding)}
              r="2.2"
              fill={strokeColor}
            />
          )}
        </svg>
        <span className={`trajectory-mini-badge ${trajectory}`}>
          <TrajectoryIcon size={11} />
          <span>{delta_24h >= 0 ? `+${delta_24h}` : delta_24h}</span>
        </span>
      </div>
    );
  }

  // Expanded card view for RegionDrawer
  return (
    <div className="sparkline-card">
      <div className="sparkline-card-header">
        <span className="sparkline-card-label">24h Attention-Response Trajectory</span>
        <span className={`trajectory-pill ${trajectory}`}>
          <TrajectoryIcon size={13} />
          <span>{trajectory.toUpperCase()} ({delta_24h >= 0 ? `+${delta_24h}` : delta_24h})</span>
        </span>
      </div>
      <div className="sparkline-chart-row">
        <svg width={width} height={height} className="sparkline-svg">
          <polyline
            fill="none"
            stroke={strokeColor}
            strokeWidth="2.4"
            strokeLinecap="round"
            strokeLinejoin="round"
            points={points}
          />
          {history.map((pt, idx) => {
            const x = padding + (idx / (history.length - 1)) * (width - 2 * padding);
            const y = height - padding - ((pt.gap_score - minScore) / range) * (height - 2 * padding);
            return (
              <circle
                key={idx}
                cx={x}
                cy={y}
                r="3"
                fill={strokeColor}
              />
            );
          })}
        </svg>
        <div className="sparkline-ticks">
          <span>-24h: {history[0].gap_score}</span>
          <span>Now: {history[history.length - 1].gap_score}</span>
        </div>
      </div>
    </div>
  );
}
