import React, { useState, useEffect } from 'react';
import { X, ExternalLink, Bookmark, BookmarkCheck, TrendingUp, AlertTriangle, Newspaper, FileText, Activity, Cpu, ChevronRight } from 'lucide-react';
import { fetchCountryFeed } from '../services/api';
import ExplainabilityPanel from './ExplainabilityPanel';

export default function RegionDrawer({
  region,
  onClose,
  isBookmarked,
  onToggleBookmark,
  initialSubTab = 'overview'
}) {
  const [activeSubTab, setActiveSubTab] = useState(initialSubTab);
  const [articles, setArticles] = useState([]);
  const [reports, setReports] = useState([]);
  const [feedLoading, setFeedLoading] = useState(false);

  useEffect(() => {
    if (initialSubTab) {
      setActiveSubTab(initialSubTab);
    }
  }, [initialSubTab, region?.region]);

  useEffect(() => {
    if (!region) return;

    let isMounted = true;
    setFeedLoading(true);

    fetchCountryFeed(region.region, region.country_code)
      .then(({ gdeltArticles, reliefwebReports }) => {
        if (isMounted) {
          setArticles(gdeltArticles);
          setReports(reliefwebReports);
          setFeedLoading(false);
        }
      })
      .catch(() => {
        if (isMounted) setFeedLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [region]);

  if (!region) return null;

  const getBadgeClass = (category) => {
    switch (category) {
      case 'Neglected Emergency': return 'badge-neglected';
      case 'Escalating Hotspot': return 'badge-escalating';
      case 'Protracted Crisis': return 'badge-protracted';
      case 'Stabilized Response': return 'badge-stabilized';
      default: return 'badge-protracted';
    }
  };

  const gapPercent = Math.min(100, Math.round((region.gap_score / 10) * 100));

  return (
    <aside className="region-drawer" aria-label="Hotspot Intelligence Dossier">
      {/* Drawer Header */}
      <div className="drawer-header">
        <div className="drawer-title-group">
          <div className="region-code-badge">{region.country_code}</div>
          <div>
            <h2 className="drawer-region-name">{region.region}</h2>
            <div className="drawer-coords">
              {region.lat.toFixed(4)}° N, {region.lon.toFixed(4)}° E
            </div>
          </div>
        </div>

        <div className="drawer-header-actions">
          <button
            className={`btn btn-icon ${isBookmarked ? 'btn-bookmarked' : ''}`}
            onClick={() => onToggleBookmark(region.region)}
            title={isBookmarked ? "Remove from Watchlist" : "Save to Watchlist"}
            aria-label="Toggle watchlist"
          >
            {isBookmarked ? <BookmarkCheck size={18} style={{ color: '#d97706' }} /> : <Bookmark size={18} />}
          </button>
          <button
            className="btn btn-icon"
            onClick={onClose}
            title="Close Dossier"
            aria-label="Close"
          >
            <X size={18} />
          </button>
        </div>
      </div>

      {/* Badges Bar */}
      <div className="drawer-badges">
        <button
          className={`badge ${getBadgeClass(region.category)} badge-interactive`}
          onClick={() => setActiveSubTab('explainability')}
          title="Click to inspect ML decision path & feature attribution"
          type="button"
        >
          {region.category}
          <span className="badge-inspect-arrow">↗</span>
        </button>
        {region.is_anomaly && (
          <button
            className="badge badge-anomaly badge-interactive"
            onClick={() => setActiveSubTab('explainability')}
            title="Click to view Isolation Forest anomaly breakdown"
            type="button"
          >
            <AlertTriangle size={12} />
            Statistical Outlier
            <span className="badge-inspect-arrow">↗</span>
          </button>
        )}
      </div>

      {/* Apple-styled Sub Tabs */}
      <div className="drawer-subtabs">
        <button
          className={`tab-btn ${activeSubTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('overview')}
        >
          <Activity size={15} />
          <span>Intelligence Metrics</span>
        </button>
        <button
          className={`tab-btn ${activeSubTab === 'explainability' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('explainability')}
        >
          <Cpu size={15} />
          <span>ML Attribution</span>
        </button>
        <button
          className={`tab-btn ${activeSubTab === 'news' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('news')}
        >
          <Newspaper size={15} />
          <span>GDELT News ({articles.length})</span>
        </button>
        <button
          className={`tab-btn ${activeSubTab === 'reliefweb' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('reliefweb')}
        >
          <FileText size={15} />
          <span>UN Reports ({reports.length})</span>
        </button>
      </div>

      {/* Drawer Content */}
      <div className="drawer-body">
        {activeSubTab === 'overview' && (
          <div className="drawer-overview-tab" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {/* Attention-Response Disparity Card */}
            <div className="gap-meter-card">
              <div className="meter-header">
                <div>
                  <span className="meter-label">Attention-Response Disparity</span>
                  <div className="meter-score font-mono font-bold">
                    <span style={{ color: region.gap_score >= 8 ? '#e02424' : '#0071e3' }}>
                      {region.gap_score?.toFixed(2)}
                    </span>
                    <span style={{ color: '#86868b', fontSize: '1rem', fontWeight: 500 }}> / 10.0</span>
                  </div>
                </div>
                <span className={`badge ${getBadgeClass(region.category)}`}>
                  {region.gap_score >= 8.0 ? 'CRITICAL DISPARITY' : region.gap_score >= 6.0 ? 'MODERATE DISPARITY' : 'PROPORTIONAL'}
                </span>
              </div>

              {/* Progress track */}
              <div className="meter-bar-track">
                <div
                  className="meter-bar-fill"
                  style={{
                    width: `${gapPercent}%`,
                    background: region.gap_score >= 8 ? 'linear-gradient(90deg, #f59e0b, #e02424)' : 'linear-gradient(90deg, #0284c7, #0071e3)'
                  }}
                />
              </div>

              <div className="meter-formula-note">
                Quantified disparity: Logarithmic scaling of 24h media volume & surge ratio penalized against active UN OCHA situation reports.
              </div>
            </div>

            {/* Feature Vector Grid */}
            <div className="vector-grid">
              <div className="vector-card">
                <span className="vector-label">24h Media Coverage</span>
                <div className="vector-val">{region.media_volume_24h?.toLocaleString()}</div>
                <span className="vector-sub">GDELT tracked mentions</span>
              </div>

              <div className="vector-card">
                <span className="vector-label">Volume Ratio (vs 7d)</span>
                <div className="vector-val" style={{ color: region.volume_ratio > 1.35 ? '#d97706' : '#1d1d1f' }}>
                  {region.volume_ratio?.toFixed(2)}&times;
                </div>
                <span className="vector-sub">
                  {region.volume_ratio > 1.35 ? 'Accelerated coverage' : 'Normal baseline'}
                </span>
              </div>

              <div className="vector-card">
                <span className="vector-label">UN Response Count</span>
                <div className="vector-val" style={{ color: '#0284c7' }}>
                  {region.reliefweb_response_count}
                </div>
                <span className="vector-sub">Appeals & situation reports</span>
              </div>

              <div className="vector-card">
                <span className="vector-label">Goldstein Conflict Scale</span>
                <div className="vector-val" style={{ color: region.avg_goldstein < -6 ? '#e02424' : '#1d1d1f' }}>
                  {region.avg_goldstein?.toFixed(1)}
                </div>
                <span className="vector-sub">[-10 War to +10 Peace]</span>
              </div>

              <div className="vector-card">
                <span className="vector-label">Tone Dispersion</span>
                <div className="vector-val">
                  {region.tone_volatility?.toFixed(2)} &sigma;
                </div>
                <span className="vector-sub">Sentiment variance</span>
              </div>

              <div className="vector-card">
                <span className="vector-label">Outlier Classification</span>
                <div className="vector-val" style={{ color: region.is_anomaly ? '#9333ea' : '#16a34a' }}>
                  {region.is_anomaly ? 'Detected' : 'Nominal'}
                </div>
                <span className="vector-sub">Isolation Forest model</span>
              </div>
            </div>

            {/* Operational Assessment */}
            <div className="insight-card">
              <h4 className="insight-title">
                <TrendingUp size={15} style={{ color: '#0071e3' }} />
                Operational Assessment
              </h4>
              <p className="insight-body">
                {region.category === 'Neglected Emergency' && (
                  `Critical attention-response deficit detected for ${region.region}. Despite severe conflict intensity (Goldstein: ${region.avg_goldstein}), UN OCHA tracking records only ${region.reliefweb_response_count} active situation reports/appeals, signaling acute under-resourcing.`
                )}
                {region.category === 'Escalating Hotspot' && (
                  `Surging conflict activity detected in ${region.region}. 24-hour media coverage is tracking at ${region.volume_ratio}x relative to the 7-day baseline, indicating rapidly unfolding hostilities requiring urgent logistics monitoring.`
                )}
                {region.category === 'Protracted Crisis' && (
                  `Long-term sustained crisis profile for ${region.region}. Reporting volume is consistent with historical baselines with regular ongoing humanitarian partner operations.`
                )}
                {region.category === 'Stabilized Response' && (
                  `${region.region} exhibits robust humanitarian response presence (${region.reliefweb_response_count} appeals/reports) maintaining parity with international news visibility.`
                )}
              </p>

              <button
                type="button"
                className="btn-explain-cta"
                onClick={() => setActiveSubTab('explainability')}
              >
                <span>Inspect ML Decision Tree & Feature Drivers</span>
                <ChevronRight size={14} />
              </button>
            </div>
          </div>
        )}

        {activeSubTab === 'explainability' && (
          <ExplainabilityPanel region={region} />
        )}

        {activeSubTab === 'news' && (
          <div className="drawer-feed-tab">
            {feedLoading ? (
              <div className="feed-loading">Loading GDELT news events...</div>
            ) : articles.length === 0 ? (
              <div className="feed-empty">No recent news events returned for this hotspot.</div>
            ) : (
              <div className="feed-list">
                {articles.map((art, idx) => (
                  <article key={idx} className="feed-item">
                    <div className="feed-meta">
                      <span className="feed-domain">{art.domain || 'Global Wire'}</span>
                      {art.tone !== undefined && (
                        <span className={`feed-tone ${art.tone < -4 ? 'tone-severe' : 'tone-neutral'}`}>
                          Tone: {art.tone?.toFixed(1)}
                        </span>
                      )}
                    </div>
                    <h5 className="feed-title">{art.title}</h5>
                    <div className="feed-footer">
                      <span style={{ fontSize: '0.725rem', color: '#86868b' }}>
                        {(() => {
                          if (!art.seendate) return 'Recent';
                          try {
                            // GDELT format: 20260929T210000Z
                            if (/^\d{8}T\d{6}Z$/.test(art.seendate)) {
                              const y = art.seendate.slice(0, 4);
                              const m = art.seendate.slice(4, 6);
                              const d = art.seendate.slice(6, 8);
                              const h = art.seendate.slice(9, 11);
                              const min = art.seendate.slice(11, 13);
                              return `${y}-${m}-${d} ${h}:${min} UTC`;
                            }
                            const d = new Date(art.seendate);
                            return isNaN(d.getTime()) ? 'Recent' : d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                          } catch {
                            return 'Recent';
                          }
                        })()}
                      </span>
                      {art.url && (
                        <a
                          href={art.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="feed-link"
                          title="Open original report"
                        >
                          <span>Read Source</span>
                          <ExternalLink size={12} />
                        </a>
                      )}
                    </div>
                  </article>
                ))}
              </div>
            )}
          </div>
        )}

        {activeSubTab === 'reliefweb' && (
          <div className="drawer-feed-tab">
            {feedLoading ? (
              <div className="feed-loading">Querying UN OCHA ReliefWeb records...</div>
            ) : reports.length === 0 ? (
              <div className="feed-empty">No ReliefWeb situation reports registered in current cache.</div>
            ) : (
              <div className="feed-list">
                {reports.map((rep, idx) => (
                  <article key={idx} className="feed-item">
                    <div className="feed-meta">
                      <span style={{ fontWeight: 600, color: '#1d1d1f' }}>{rep.source || 'UN OCHA'}</span>
                      <span className="badge badge-protracted">{rep.format || 'Situation Report'}</span>
                    </div>
                    <h5 className="feed-title">{rep.title}</h5>
                    <div className="feed-footer">
                      <span style={{ fontSize: '0.725rem', color: '#86868b' }}>UN Verified</span>
                      {rep.url && (
                        <a
                          href={rep.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="feed-link"
                          title="View on ReliefWeb"
                        >
                          <span>ReliefWeb Portal</span>
                          <ExternalLink size={12} />
                        </a>
                      )}
                    </div>
                  </article>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </aside>
  );
}
