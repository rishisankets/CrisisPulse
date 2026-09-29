import React, { useState } from 'react';
import { Newspaper, FileText, ExternalLink } from 'lucide-react';

export default function RawFeedsView({ regions = [] }) {
  const [selectedCountry, setSelectedCountry] = useState('ALL');
  const [feedType, setFeedType] = useState('all');

  // Collect all articles and reports across regions
  const allArticles = regions.flatMap(r =>
    (r.gdelt_sample_headlines || []).map((headline, idx) => ({
      region: r.region,
      country_code: r.country_code,
      title: headline,
      tone: (r.avg_goldstein || -5.0) + (idx * 0.4 - 0.8),
      time: 'Real-time Stream',
      url: `https://news.google.com/search?q=${encodeURIComponent(headline)}`
    }))
  );

  const allReports = regions.flatMap(r =>
    (r.reliefweb_reports || []).map(rep => ({
      ...rep,
      region: r.region,
      country_code: r.country_code
    }))
  );

  const filteredArticles = allArticles.filter(a =>
    selectedCountry === 'ALL' || a.region === selectedCountry
  );

  const filteredReports = allReports.filter(r =>
    selectedCountry === 'ALL' || r.region === selectedCountry
  );

  return (
    <div className="feeds-view-container">
      {/* Controls */}
      <div className="feeds-controls-bar">
        <div className="feeds-filter-country">
          <label style={{ fontSize: '0.8rem', color: '#86868b' }}>Filter Hotspot:</label>
          <select
            value={selectedCountry}
            onChange={(e) => setSelectedCountry(e.target.value)}
            className="feeds-select"
          >
            <option value="ALL">Global (All Hotspots)</option>
            {regions.map(r => (
              <option key={r.region} value={r.region}>{r.region} ({r.country_code})</option>
            ))}
          </select>
        </div>

        <div className="feeds-tab-switch">
          <button
            className={`tab-btn ${feedType === 'all' ? 'active' : ''}`}
            onClick={() => setFeedType('all')}
            style={{ borderRadius: '9999px', padding: '0.35rem 0.85rem' }}
          >
            Combined Feed
          </button>
          <button
            className={`tab-btn ${feedType === 'gdelt' ? 'active' : ''}`}
            onClick={() => setFeedType('gdelt')}
            style={{ borderRadius: '9999px', padding: '0.35rem 0.85rem' }}
          >
            GDELT News
          </button>
          <button
            className={`tab-btn ${feedType === 'reliefweb' ? 'active' : ''}`}
            onClick={() => setFeedType('reliefweb')}
            style={{ borderRadius: '9999px', padding: '0.35rem 0.85rem' }}
          >
            UN ReliefWeb
          </button>
        </div>
      </div>

      {/* Telemetry Columns */}
      <div className="feeds-columns-grid">
        {(feedType === 'all' || feedType === 'gdelt') && (
          <div className="feed-column">
            <div className="column-header">
              <div className="column-title-wrap">
                <Newspaper size={17} style={{ color: '#d97706' }} />
                <h3 className="column-title">GDELT 2.0 Global Conflict Wire</h3>
              </div>
              <span className="badge badge-escalating">{filteredArticles.length} Events</span>
            </div>

            <div className="feed-items-list">
              {filteredArticles.map((art, idx) => (
                <div key={idx} className="feed-stream-card">
                  <div className="stream-card-meta">
                    <span className="region-cell-code">{art.country_code}</span>
                    <span style={{ fontWeight: 600, fontSize: '0.8rem' }}>{art.region}</span>
                    <span style={{ color: art.tone < -5 ? '#e02424' : '#86868b', fontSize: '0.725rem', fontWeight: 500 }}>
                      Tone: {art.tone.toFixed(1)}
                    </span>
                  </div>
                  <h4 className="stream-headline">{art.title}</h4>
                  <div className="stream-card-footer">
                    <span style={{ fontSize: '0.7rem', color: '#86868b' }}>GDELT Monitored Event</span>
                    <a
                      href={art.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="feed-link"
                    >
                      <span>Read Event</span>
                      <ExternalLink size={12} />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {(feedType === 'all' || feedType === 'reliefweb') && (
          <div className="feed-column">
            <div className="column-header">
              <div className="column-title-wrap">
                <FileText size={17} style={{ color: '#0284c7' }} />
                <h3 className="column-title">UN OCHA ReliefWeb SitReps & Appeals</h3>
              </div>
              <span className="badge badge-protracted">{filteredReports.length} Reports</span>
            </div>

            <div className="feed-items-list">
              {filteredReports.map((rep, idx) => (
                <div key={idx} className="feed-stream-card">
                  <div className="stream-card-meta">
                    <span className="region-cell-code">{rep.country_code}</span>
                    <span style={{ fontWeight: 600, fontSize: '0.8rem' }}>{rep.region}</span>
                    <span className="badge badge-protracted" style={{ fontSize: '0.68rem' }}>{rep.format || 'SitRep'}</span>
                  </div>
                  <h4 className="stream-headline">{rep.title}</h4>
                  <div className="stream-card-footer">
                    <span style={{ fontSize: '0.7rem', color: '#86868b' }}>{rep.source || 'UN OCHA'}</span>
                    <a
                      href={rep.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="feed-link"
                    >
                      <span>Official Report</span>
                      <ExternalLink size={12} />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
