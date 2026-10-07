import React, { useState } from 'react';
import { Activity, ShieldAlert, Radio, RefreshCw, Layers, BarChart3, Database, Download, User, LogOut, ChevronDown, FileSpreadsheet, FileCode } from 'lucide-react';

import CrisisPulseLogo from './CrisisPulseLogo';
import { triggerDossierDownload } from '../services/api';

export default function Navbar({
  activeTab,
  setActiveTab,
  isLive,
  health,
  onRefresh,
  isLoading,
  currentUser,
  onOpenAuth,
  onLogout
}) {
  const [showExportMenu, setShowExportMenu] = useState(false);

  return (
    <header className="header-nav">
      <div className="nav-container">
        {/* Brand Identity */}
        <div className="brand-group">
          <div className="brand-icon-wrapper cp-logo-container">
            <CrisisPulseLogo size={36} />
          </div>
          <div>
            <div className="brand-title-wrap">
              <h1 className="brand-title">
                Crisis<span className="brand-title-pulse">Pulse</span>
              </h1>
              <span className="brand-version">Preview</span>
            </div>
            <p className="brand-subtitle">media attention vs. humanitarian response</p>
          </div>
        </div>

        {/* Segmented Controls */}
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

        {/* Status, Export & User Auth Controls */}
        <div className="nav-controls">
          {/* Export Dossier Dropdown */}
          <div className="export-menu-container">
            <button
              className="btn btn-secondary export-nav-btn"
              onClick={() => setShowExportMenu(!showExportMenu)}
              title="Download Crisis Dossier Report"
            >
              <Download size={14} />
              <span>Export</span>
              <ChevronDown size={12} />
            </button>
            {showExportMenu && (
              <div className="export-dropdown-menu" onClick={() => setShowExportMenu(false)}>
                <button
                  className="export-dropdown-item"
                  onClick={() => triggerDossierDownload('csv')}
                >
                  <FileSpreadsheet size={14} className="export-item-icon csv" />
                  <div>
                    <div className="export-item-title">CSV Spreadsheet</div>
                    <div className="export-item-desc">For Excel, R & Python data pipelines</div>
                  </div>
                </button>
                <button
                  className="export-dropdown-item"
                  onClick={() => triggerDossierDownload('json')}
                >
                  <FileCode size={14} className="export-item-icon json" />
                  <div>
                    <div className="export-item-title">JSON Intelligence Snapshot</div>
                    <div className="export-item-desc">Complete payload with ML attributions</div>
                  </div>
                </button>
              </div>
            )}
          </div>

          {/* User Auth Chip */}
          {currentUser ? (
            <div className="user-profile-chip" title={`Logged in as ${currentUser.email}`}>
              <div className="user-avatar-dot" />
              <span className="user-email-text">{currentUser.email.split('@')[0]}</span>
              <button
                className="user-logout-btn"
                onClick={onLogout}
                title="Log out of session"
                aria-label="Log out"
              >
                <LogOut size={13} />
              </button>
            </div>
          ) : (
            <button
              className="btn btn-secondary auth-nav-btn"
              onClick={onOpenAuth}
              title="Sign in to sync saved watchlists"
            >
              <User size={14} />
              <span>Sign In</span>
            </button>
          )}

          {/* Status Pill */}
          <div className="status-pill" title={isLive ? "FastAPI Backend & SQLite WAL Active" : "Offline mode — Verified seed intelligence"}>
            <span className={`status-dot ${isLive ? 'online' : 'offline'}`} />
            <span className="status-label">
              {isLive ? 'LIVE' : 'OFFLINE'}
            </span>
          </div>

          {/* Refresh Action */}
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

