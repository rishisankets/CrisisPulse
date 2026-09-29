import React from 'react';
import { Globe, AlertTriangle, Flame, ShieldAlert, Scale } from 'lucide-react';

export default function KpiBar({ stats, results = [] }) {
  const totalAnalyzed = stats?.total_analyzed ?? results.length;
  const neglectedCount = stats?.neglected_count ?? results.filter(r => r.category === 'Neglected Emergency').length;
  const escalatingCount = stats?.escalating_count ?? results.filter(r => r.category === 'Escalating Hotspot').length;
  const anomaliesCount = stats?.anomalies_detected ?? results.filter(r => r.is_anomaly).length;

  const avgGap = results.length > 0
    ? (results.reduce((acc, curr) => acc + (curr.gap_score || 0), 0) / results.length).toFixed(2)
    : '0.00';

  return (
    <section className="kpi-grid">
      <div className="card-clean kpi-card">
        <div className="kpi-icon-wrap" style={{ background: '#f0f9ff', color: '#0284c7' }}>
          <Globe size={22} />
        </div>
        <div className="kpi-content">
          <span className="kpi-label">Monitored Crises</span>
          <div className="kpi-val">{totalAnalyzed}</div>
          <span className="kpi-sub">Continuous 24h & 7d fusion</span>
        </div>
      </div>

      <div className="card-clean kpi-card">
        <div className="kpi-icon-wrap" style={{ background: '#fef2f2', color: '#e02424' }}>
          <AlertTriangle size={22} />
        </div>
        <div className="kpi-content">
          <span className="kpi-label">Neglected Emergencies</span>
          <div className="kpi-val" style={{ color: '#e02424' }}>{neglectedCount}</div>
          <span className="kpi-sub">Severe response lag</span>
        </div>
      </div>

      <div className="card-clean kpi-card">
        <div className="kpi-icon-wrap" style={{ background: '#fffbeb', color: '#d97706' }}>
          <Flame size={22} />
        </div>
        <div className="kpi-content">
          <span className="kpi-label">Escalating Hotspots</span>
          <div className="kpi-val" style={{ color: '#d97706' }}>{escalatingCount}</div>
          <span className="kpi-sub">Coverage surge &gt;1.35&times;</span>
        </div>
      </div>

      <div className="card-clean kpi-card">
        <div className="kpi-icon-wrap" style={{ background: '#faf5ff', color: '#9333ea' }}>
          <ShieldAlert size={22} />
        </div>
        <div className="kpi-content">
          <span className="kpi-label">Statistical Outliers</span>
          <div className="kpi-val" style={{ color: '#9333ea' }}>{anomaliesCount}</div>
          <span className="kpi-sub">Isolation Forest detections</span>
        </div>
      </div>

      <div className="card-clean kpi-card">
        <div className="kpi-icon-wrap" style={{ background: '#f5f5f7', color: '#1d1d1f' }}>
          <Scale size={22} />
        </div>
        <div className="kpi-content">
          <span className="kpi-label">Mean Disparity Gap</span>
          <div className="kpi-val">{avgGap}<span style={{ fontSize: '0.85rem', color: '#86868b', fontWeight: 500 }}> / 10</span></div>
          <span className="kpi-sub">Attention vs aid balance</span>
        </div>
      </div>
    </section>
  );
}
