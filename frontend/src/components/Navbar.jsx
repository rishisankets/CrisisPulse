import React from 'react';
import { Activity, ShieldAlert, Radio, RefreshCw, Layers, BarChart3, Database } from 'lucide-react';

export default function Navbar({
  activeTab,
  setActiveTab,
  isLive,
  health,
  onRefresh,
  isLoading
}) {
  return (
    <header className="header-nav">
      <div className="nav-container">
        {/* Apple Brand Identity */}
        <div className="brand-group">
          <div className="brand-icon-wrapper">
            <Radio className="text-accent" size={19} />
          </div>
          <div>
            <div className="brand-title-wrap">
              <h1 className="brand-title">CrisisPulse</h1>
              <span className="brand-version">Preview</span>
            </div>
            <p className="brand-subtitle">Global Conflict & Humanitarian Disparity Monitor</p>
          </div>
        </div>

        {/* Apple Segmented Controls */}
        <nav className="nav-tabs" role="tablist">
          <button
            role="tab"
            aria-selected={activeTab === 'map'}
            className={`nav-tab-btn ${activeTab === 'map' ? 'active' : ''}`}
            onClick={() => setActiveTab('map')}
          >
            <Layers size={15} />
            <span>Map</span>
          </button>
          <button
            role="tab"
            aria-selected={activeTab === 'rankings'}
            className={`nav-tab-btn ${activeTab === 'rankings' ? 'active' : ''}`}
            onClick={() => setActiveTab('rankings')}
          >
            <BarChart3 size={15} />
            <span>Disparity Index</span>
          </button>
          <button
            role="tab"
            aria-selected={activeTab === 'anomalies'}
            className={`nav-tab-btn ${activeTab === 'anomalies' ? 'active' : ''}`}
            onClick={() => setActiveTab('anomalies')}
          >
            <ShieldAlert size={15} />
            <span>ML Anomalies</span>
          </button>
          <button
            role="tab"
            aria-selected={activeTab === 'feeds'}
            className={`nav-tab-btn ${activeTab === 'feeds' ? 'active' : ''}`}
            onClick={() => setActiveTab('feeds')}
          >
            <Database size={15} />
            <span>Live Telemetry</span>
          </button>
        </nav>

        {/* Status & Refresh Action */}
        <div className="nav-controls">
          <div className="status-pill" title={isLive ? "FastAPI Backend & SQLite WAL Active" : "Offline mode — Verified seed intelligence"}>
            <span className={`status-dot ${isLive ? 'online' : 'offline'}`} />
            <span className="status-label">
              {isLive ? 'LIVE' : 'OFFLINE'}
            </span>
          </div>

          <button
            className="btn btn-icon refresh-btn"
            onClick={onRefresh}
            disabled={isLoading}
            title="Refresh Intelligence Data"
            aria-label="Refresh data"
          >
            <RefreshCw size={15} className={isLoading ? 'spinning' : ''} />
          </button>
        </div>
      </div>
    </header>
  );
}
