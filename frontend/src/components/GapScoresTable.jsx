import React, { useState } from 'react';
import { ArrowUpDown, Search, Bookmark, BookmarkCheck, ExternalLink, AlertTriangle, Cpu } from 'lucide-react';

export default function GapScoresTable({
  regions = [],
  onSelectRegion,
  bookmarks = [],
  onToggleBookmark
}) {
  const [sortField, setSortField] = useState('gap_score');
  const [sortAsc, setSortAsc] = useState(false);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('ALL');

  const handleSort = (field) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(false);
    }
  };

  const filtered = regions.filter(item => {
    if (categoryFilter !== 'ALL' && item.category !== categoryFilter) return false;
    if (search.trim()) {
      const q = search.toLowerCase();
      return item.region.toLowerCase().includes(q) || item.country_code?.toLowerCase().includes(q);
    }
    return true;
  });

  const sorted = [...filtered].sort((a, b) => {
    let aVal = a[sortField];
    let bVal = b[sortField];
    if (typeof aVal === 'string') {
      return sortAsc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    }
    return sortAsc ? (aVal - bVal) : (bVal - aVal);
  });

  const getBadgeClass = (category) => {
    switch (category) {
      case 'Neglected Emergency': return 'badge-neglected';
      case 'Escalating Hotspot': return 'badge-escalating';
      case 'Protracted Crisis': return 'badge-protracted';
      case 'Stabilized Response': return 'badge-stabilized';
      default: return 'badge-protracted';
    }
  };

  return (
    <div className="table-view-container">
      {/* Controls Bar */}
      <div className="table-controls-bar">
        <div className="search-wrap">
          <Search size={15} className="text-muted" />
          <input
            type="text"
            placeholder="Search crisis region or code..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="table-search-input"
          />
        </div>

        <div className="table-filter-group">
          <label style={{ fontSize: '0.8rem', color: '#86868b' }}>Classification:</label>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="table-filter-select"
          >
            <option value="ALL">All Classifications</option>
            <option value="Neglected Emergency">Neglected Emergency</option>
            <option value="Escalating Hotspot">Escalating Hotspot</option>
            <option value="Protracted Crisis">Protracted Crisis</option>
            <option value="Stabilized Response">Stabilized Response</option>
          </select>
        </div>
      </div>

      {/* Leaderboard Table */}
      <div className="table-wrapper">
        <table className="crisispulse-table">
          <thead>
            <tr>
              <th style={{ width: '48px', textAlign: 'center' }}>Rank</th>
              <th onClick={() => handleSort('region')} style={{ cursor: 'pointer' }}>
                <div className="th-content">
                  <span>Hotspot</span>
                  <ArrowUpDown size={12} />
                </div>
              </th>
              <th onClick={() => handleSort('gap_score')} style={{ cursor: 'pointer' }}>
                <div className="th-content">
                  <span>Disparity Index</span>
                  <ArrowUpDown size={12} />
                </div>
              </th>
              <th>Classification Archetype</th>
              <th onClick={() => handleSort('media_volume_24h')} style={{ cursor: 'pointer', textAlign: 'right' }}>
                <div className="th-content" style={{ justifyContent: 'flex-end' }}>
                  <span>24h Coverage</span>
                  <ArrowUpDown size={12} />
                </div>
              </th>
              <th onClick={() => handleSort('volume_ratio')} style={{ cursor: 'pointer', textAlign: 'right' }}>
                <div className="th-content" style={{ justifyContent: 'flex-end' }}>
                  <span>Surge Ratio</span>
                  <ArrowUpDown size={12} />
                </div>
              </th>
              <th onClick={() => handleSort('reliefweb_response_count')} style={{ cursor: 'pointer', textAlign: 'right' }}>
                <div className="th-content" style={{ justifyContent: 'flex-end' }}>
                  <span>UN Reports</span>
                  <ArrowUpDown size={12} />
                </div>
              </th>
              <th onClick={() => handleSort('avg_goldstein')} style={{ cursor: 'pointer', textAlign: 'right' }}>
                <div className="th-content" style={{ justifyContent: 'flex-end' }}>
                  <span>Goldstein Scale</span>
                  <ArrowUpDown size={12} />
                </div>
              </th>
              <th style={{ textAlign: 'center' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {sorted.length === 0 ? (
              <tr>
                <td colSpan={9} style={{ textAlign: 'center', padding: '3rem', color: '#86868b' }}>
                  No crisis hotspots match your search.
                </td>
              </tr>
            ) : (
              sorted.map((item, index) => {
                const isBookmarked = bookmarks.includes(item.region);
                const gapBarWidth = Math.min(100, Math.round((item.gap_score / 10) * 100));

                return (
                  <tr
                    key={item.region}
                    className="table-row hover-row"
                    onClick={() => onSelectRegion(item)}
                  >
                    <td style={{ textAlign: 'center', fontWeight: 600, color: '#86868b' }}>
                      #{index + 1}
                    </td>
                    <td>
                      <div className="region-cell">
                        <span className="region-cell-code">{item.country_code}</span>
                        <div>
                          <strong className="region-cell-name">{item.region}</strong>
                          {item.is_anomaly && (
                            <span
                              className="anomaly-tiny-badge"
                              title="Statistical outlier detected — click to inspect ML attribution"
                              onClick={(e) => {
                                e.stopPropagation();
                                onSelectRegion(item, 'explainability');
                              }}
                              style={{ cursor: 'pointer' }}
                            >
                              <AlertTriangle size={10} />
                              Outlier ↗
                            </span>
                          )}
                        </div>
                      </div>
                    </td>
                    <td>
                      <div className="score-cell">
                        <div className="score-num font-mono">
                          <span style={{ color: item.gap_score >= 8.0 ? '#e02424' : item.gap_score >= 6.0 ? '#d97706' : '#0284c7' }}>
                            {item.gap_score?.toFixed(2)}
                          </span>
                          <span style={{ color: '#86868b', fontSize: '0.75rem', fontWeight: 400 }}> / 10</span>
                        </div>
                        <div className="score-mini-bar">
                          <div
                            className="score-mini-fill"
                            style={{
                              width: `${gapBarWidth}%`,
                              background: item.gap_score >= 8.0 ? '#e02424' : item.gap_score >= 6.0 ? '#d97706' : '#0284c7'
                            }}
                          />
                        </div>
                      </div>
                    </td>
                    <td>
                      <button
                        type="button"
                        className={`badge ${getBadgeClass(item.category)} badge-interactive`}
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectRegion(item, 'explainability');
                        }}
                        title="Click to inspect ML decision path & feature attribution"
                      >
                        {item.category}
                        <span className="badge-inspect-arrow">↗</span>
                      </button>
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      {item.media_volume_24h?.toLocaleString()}
                    </td>
                    <td style={{ textAlign: 'right', fontWeight: item.volume_ratio > 1.35 ? 600 : 400, color: item.volume_ratio > 1.35 ? '#d97706' : 'inherit' }}>
                      {item.volume_ratio?.toFixed(2)}&times;
                    </td>
                    <td style={{ textAlign: 'right', fontWeight: 600, color: '#0284c7' }}>
                      {item.reliefweb_response_count}
                    </td>
                    <td style={{ textAlign: 'right', color: item.avg_goldstein < -6 ? '#e02424' : '#515154' }}>
                      {item.avg_goldstein?.toFixed(1)}
                    </td>
                    <td>
                      <div className="action-buttons-cell" style={{ justifyContent: 'center' }} onClick={(e) => e.stopPropagation()}>
                        <button
                          className="btn btn-icon btn-sm"
                          onClick={() => onSelectRegion(item, 'explainability')}
                          title="Inspect ML Decision & Feature Attribution"
                          aria-label="Explain"
                        >
                          <Cpu size={13} style={{ color: '#0071e3' }} />
                        </button>
                        <button
                          className="btn btn-icon btn-sm"
                          onClick={() => onToggleBookmark(item.region)}
                          title={isBookmarked ? "Remove Bookmark" : "Bookmark Hotspot"}
                          aria-label="Bookmark"
                        >
                          {isBookmarked ? (
                            <BookmarkCheck size={14} style={{ color: '#d97706' }} />
                          ) : (
                            <Bookmark size={14} />
                          )}
                        </button>
                        <button
                          className="btn btn-icon btn-sm btn-primary"
                          onClick={() => onSelectRegion(item)}
                          title="View Intelligence Dossier"
                          aria-label="Inspect"
                        >
                          <ExternalLink size={13} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
