import React from 'react';
import { ShieldAlert, AlertTriangle, ArrowRight, Cpu } from 'lucide-react';

export default function AnomalyRadar({
  regions = [],
  onSelectRegion
}) {
  const anomalies = regions.filter(r => r.is_anomaly);
  const normalCount = regions.length - anomalies.length;

  return (
    <div className="anomaly-view-container">
      {/* Overview Banner */}
      <div className="anomaly-hero">
        <div className="anomaly-hero-content">
          <div className="anomaly-badge-top">
            <Cpu size={15} />
            <span>UNSUPERVISED ISOLATION FOREST (CONTAMINATION = 0.2)</span>
          </div>
          <h2 className="hero-title">Statistical Disparity & Outlier Detection</h2>
          <p className="hero-description">
            CrisisPulse evaluates multi-dimensional regional vectors across media volume, surge ratios, conflict intensity, and humanitarian response.
            Statistical anomalies represent crises where conflict velocity or reporting attention fundamentally diverges from humanitarian mobilization.
          </p>
        </div>

        <div className="anomaly-metrics-pill">
          <div className="stat-box">
            <span className="stat-label">Outliers Flagged</span>
            <div className="stat-value font-mono" style={{ fontSize: '1.75rem', fontWeight: 700, color: '#9333ea' }}>{anomalies.length}</div>
          </div>
          <div className="stat-divider"></div>
          <div className="stat-box">
            <span className="stat-label">Nominal Hotspots</span>
            <div className="stat-value font-mono" style={{ fontSize: '1.75rem', fontWeight: 700, color: '#515154' }}>{normalCount}</div>
          </div>
        </div>
      </div>

      {/* Detected Anomalies Grid */}
      <div className="anomalies-section">
        <h3 className="section-title">
          <ShieldAlert size={18} style={{ color: '#9333ea' }} />
          Flagged Outlier Profiles
        </h3>

        {anomalies.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: '#86868b', background: '#ffffff', borderRadius: '14px', border: '1px solid rgba(0,0,0,0.08)' }}>
            No statistical outliers currently detected in the active telemetry window.
          </div>
        ) : (
          <div className="anomaly-cards-grid">
            {anomalies.map((item) => (
              <div
                key={item.region}
                className="anomaly-card"
                onClick={() => onSelectRegion(item)}
              >
                <div className="anomaly-card-header">
                  <div className="region-meta">
                    <span className="region-cell-code">{item.country_code}</span>
                    <h4 className="anomaly-region-name">{item.region}</h4>
                  </div>
                  <span className="badge badge-anomaly">
                    <AlertTriangle size={11} />
                    Outlier Detected
                  </span>
                </div>

                <div className="anomaly-disparity-metric">
                  <span style={{ fontSize: '0.8rem', color: '#86868b' }}>Disparity Score:</span>
                  <strong className="font-mono" style={{ fontSize: '1.3rem', color: '#e02424' }}>
                    {item.gap_score?.toFixed(2)} / 10
                  </strong>
                </div>

                {/* Multidimensional trigger breakdown */}
                <div className="anomaly-signals">
                  <div className="signal-item">
                    <span className="signal-label">Media Surge Ratio:</span>
                    <span style={{ fontWeight: 600, color: '#d97706' }}>{item.volume_ratio?.toFixed(2)}&times;</span>
                  </div>
                  <div className="signal-item">
                    <span className="signal-label">Goldstein Conflict:</span>
                    <span style={{ fontWeight: 600, color: '#e02424' }}>{item.avg_goldstein?.toFixed(1)}</span>
                  </div>
                  <div className="signal-item">
                    <span className="signal-label">Tone Volatility:</span>
                    <span style={{ fontWeight: 600, color: '#9333ea' }}>{item.tone_volatility?.toFixed(2)} &sigma;</span>
                  </div>
                  <div className="signal-item">
                    <span className="signal-label">ReliefWeb Reports:</span>
                    <span style={{ fontWeight: 600, color: '#0284c7' }}>{item.reliefweb_response_count}</span>
                  </div>
                </div>

                <div className="anomaly-explanation">
                  Vector divergence: Significant negative conflict sentiment combined with heightened reporting acceleration and lagging response reports.
                </div>

                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem' }}>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    style={{ flex: 1, fontSize: '0.8rem', padding: '0.5rem 0.75rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '5px' }}
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectRegion(item, 'explainability');
                    }}
                  >
                    <Cpu size={14} style={{ color: '#9333ea' }} />
                    <span>Explain Outlier</span>
                  </button>
                  <button
                    type="button"
                    className="btn btn-primary"
                    style={{ flex: 1, fontSize: '0.8rem', padding: '0.5rem 0.75rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '5px' }}
                    onClick={() => onSelectRegion(item, 'overview')}
                  >
                    <span>Dossier</span>
                    <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
