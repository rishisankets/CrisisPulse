import React from 'react';
import { CheckCircle2, XCircle, AlertTriangle, ShieldCheck, Cpu, GitFork, Gauge, Scale, Sparkles } from 'lucide-react';
import { getRegionExplainability } from '../services/api';

export default function ExplainabilityPanel({ region }) {
  if (!region) return null;

  const explainability = getRegionExplainability(region);
  const {
    archetype,
    primary_reason,
    is_anomaly,
    anomaly_reason,
    criteria = [],
    feature_drivers = []
  } = explainability;

  const getArchetypeColor = (cat) => {
    switch (cat) {
      case 'Neglected Emergency': return '#e02424';
      case 'Escalating Hotspot': return '#d97706';
      case 'Stabilized Response': return '#16a34a';
      default: return '#0284c7';
    }
  };

  const accentColor = getArchetypeColor(archetype);

  return (
    <div className="explainability-panel">
      {/* Top Banner / Badge */}
      <div className="explain-header-card">
        <div className="explain-tag">
          <Cpu size={14} />
          <span>ML Interpretability & Attribution Engine</span>
        </div>
        <h3 className="explain-title">
          Classification Logic for <span style={{ color: accentColor }}>{region.region}</span>
        </h3>
        <p className="explain-subtitle">
          Demonstrating exact decision boundaries and feature vectors behind the{' '}
          <strong style={{ color: accentColor }}>{archetype}</strong> designation.
        </p>

        {/* Primary Rationale Callout */}
        <div className="explain-primary-callout" style={{ borderLeftColor: accentColor }}>
          <div className="callout-icon" style={{ color: accentColor }}>
            <Sparkles size={16} />
          </div>
          <div className="callout-text">
            <strong>Primary Driver:</strong> {primary_reason}
          </div>
        </div>
      </div>

      {/* Decision Tree / Boundary Checklist */}
      <div className="explain-section">
        <div className="section-header-compact">
          <GitFork size={15} style={{ color: '#0071e3' }} />
          <h4>Decision Boundary Traversal</h4>
        </div>

        <div className="rules-checklist">
          {criteria.map((c, i) => (
            <div
              key={i}
              className={`rule-row ${c.triggered ? 'rule-triggered' : 'rule-inactive'}`}
            >
              <div className="rule-status-icon">
                {c.triggered ? (
                  <CheckCircle2 size={16} style={{ color: '#16a34a' }} />
                ) : (
                  <XCircle size={16} style={{ color: '#86868b' }} />
                )}
              </div>

              <div className="rule-details">
                <div className="rule-name-bar">
                  <span className="rule-name">{c.rule_name}</span>
                  <span className={`rule-chip ${c.triggered ? 'chip-triggered' : 'chip-skipped'}`}>
                    {c.triggered ? 'Condition Met' : 'Not Met'}
                  </span>
                </div>
                <div className="rule-formula font-mono">
                  <span>{c.label}: </span>
                  <strong>{c.actual_value}</strong>
                  <span className="rule-comparison"> {c.operator} </span>
                  <span className="text-muted">{c.threshold}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Feature Drivers vs Cohort Baseline */}
      <div className="explain-section">
        <div className="section-header-compact">
          <Gauge size={15} style={{ color: '#0071e3' }} />
          <h4>Multidimensional Driver Attribution</h4>
        </div>

        <div className="driver-cards-list">
          {feature_drivers.map((drv, i) => {
            // Compute percentage relative to baseline for visual representation
            const ratio = drv.baseline > 0 ? (drv.value / drv.baseline) : 1;
            const barWidth = Math.min(100, Math.max(15, Math.round(ratio * 50)));

            return (
              <div key={i} className="driver-bar-item">
                <div className="driver-top">
                  <span className="driver-feature-name">{drv.feature}</span>
                  <div className="driver-values font-mono">
                    <span className="driver-actual">{drv.value} {drv.unit}</span>
                    <span className="driver-baseline text-muted"> (baseline: {drv.baseline} {drv.unit})</span>
                  </div>
                </div>

                <div className="driver-track">
                  <div
                    className="driver-fill"
                    style={{
                      width: `${barWidth}%`,
                      backgroundColor: drv.direction === 'severe' || drv.direction === 'deficit' || drv.direction === 'higher'
                        ? '#d97706'
                        : '#0071e3'
                    }}
                  />
                  {/* Baseline marker at 50% */}
                  <div className="driver-baseline-mark" title="Cohort average baseline" />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Isolation Forest Anomaly Section */}
      <div className="explain-section">
        <div className="section-header-compact">
          <Scale size={15} style={{ color: '#9333ea' }} />
          <h4>Unsupervised Outlier Diagnostics (Isolation Forest)</h4>
        </div>

        <div className={`anomaly-diag-box ${is_anomaly ? 'box-anomaly' : 'box-nominal'}`}>
          <div className="anomaly-diag-header">
            {is_anomaly ? (
              <>
                <AlertTriangle size={18} style={{ color: '#9333ea' }} />
                <span className="font-semibold" style={{ color: '#9333ea' }}>
                  Statistical Anomaly Flagged
                </span>
              </>
            ) : (
              <>
                <ShieldCheck size={18} style={{ color: '#16a34a' }} />
                <span className="font-semibold" style={{ color: '#16a34a' }}>
                  Nominal Behavioral Cluster
                </span>
              </>
            )}
          </div>
          <p className="anomaly-diag-desc">
            {is_anomaly
              ? (anomaly_reason || 'Region feature vector lies beyond the 80th percentile isolation tree leaf depth in the 6-dimensional phase space.')
              : 'Vector features sit comfortably within the standard operational cluster distribution (contamination threshold = 0.20).'}
          </p>
        </div>
      </div>

      {/* Academic Defense Note */}
      <div className="academic-footnote">
        <strong>Academic Defensibility:</strong> CrisisPulse replaces subjective heuristics with deterministic boundary checks and scikit-learn Isolation Forest partitioning to ensure reproducibility during humanitarian auditing.
      </div>
    </div>
  );
}
