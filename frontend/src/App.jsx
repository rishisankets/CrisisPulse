import React, { useState, useEffect, useCallback } from 'react';
import Navbar from './components/Navbar';
import KpiBar from './components/KpiBar';
import CrisisMap from './components/CrisisMap';
import RegionDrawer from './components/RegionDrawer';
import GapScoresTable from './components/GapScoresTable';
import AnomalyRadar from './components/AnomalyRadar';
import RawFeedsView from './components/RawFeedsView';
import { fetchAnalyticsOverview, fetchHealth, SEED_HOTSPOTS } from './services/api';
import './App.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('map');
  const [regions, setRegions] = useState(SEED_HOTSPOTS);
  const [stats, setStats] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [isLive, setIsLive] = useState(false);
  const [health, setHealth] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Filter states
  const [filterCategory, setFilterCategory] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [showOnlyAnomalies, setShowOnlyAnomalies] = useState(false);

  // Watchlist stored in localStorage
  const [bookmarks, setBookmarks] = useState(() => {
    try {
      const saved = localStorage.getItem('crisispulse_bookmarks');
      return saved ? JSON.parse(saved) : ['Sudan', 'Gaza / Palestine'];
    } catch {
      return ['Sudan', 'Gaza / Palestine'];
    }
  });

  const loadData = useCallback(async () => {
    setIsLoading(true);
    try {
      const [overviewRes, healthRes] = await Promise.all([
        fetchAnalyticsOverview(),
        fetchHealth()
      ]);

      setIsLive(overviewRes.isLive);
      setHealth(healthRes.data);

      if (overviewRes.data && overviewRes.data.results) {
        setRegions(overviewRes.data.results);
        setStats(overviewRes.data);
      }
    } catch (err) {
      console.error('Data load error:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const toggleBookmark = (regionName) => {
    setBookmarks(prev => {
      const next = prev.includes(regionName)
        ? prev.filter(r => r !== regionName)
        : [...prev, regionName];
      try {
        localStorage.setItem('crisispulse_bookmarks', JSON.stringify(next));
      } catch (e) {
        console.warn('Could not persist watchlist to localStorage', e);
      }
      return next;
    });
  };

  return (
    <div className="app-container">
      {/* Top Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isLive={isLive}
        health={health}
        onRefresh={loadData}
        isLoading={isLoading}
      />

      {/* Main Container */}
      <main className="main-content">
        {/* Top Intelligence KPI Metrics */}
        <KpiBar stats={stats} results={regions} />

        {/* View Switcher */}
        {activeTab === 'map' && (
          <div className="workspace-layout">
            <CrisisMap
              regions={regions}
              selectedRegion={selectedRegion}
              onSelectRegion={setSelectedRegion}
              filterCategory={filterCategory}
              setFilterCategory={setFilterCategory}
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              showOnlyAnomalies={showOnlyAnomalies}
              setShowOnlyAnomalies={setShowOnlyAnomalies}
            />

            {/* Slide-out Intelligence Deep Dive Drawer */}
            {selectedRegion && (
              <RegionDrawer
                region={selectedRegion}
                onClose={() => setSelectedRegion(null)}
                isBookmarked={bookmarks.includes(selectedRegion.region)}
                onToggleBookmark={toggleBookmark}
              />
            )}
          </div>
        )}

        {activeTab === 'rankings' && (
          <div className="workspace-layout">
            <div style={{ flex: 1 }}>
              <GapScoresTable
                regions={regions}
                onSelectRegion={setSelectedRegion}
                bookmarks={bookmarks}
                onToggleBookmark={toggleBookmark}
              />
            </div>

            {selectedRegion && (
              <RegionDrawer
                region={selectedRegion}
                onClose={() => setSelectedRegion(null)}
                isBookmarked={bookmarks.includes(selectedRegion.region)}
                onToggleBookmark={toggleBookmark}
              />
            )}
          </div>
        )}

        {activeTab === 'anomalies' && (
          <div className="workspace-layout">
            <div style={{ flex: 1 }}>
              <AnomalyRadar
                regions={regions}
                onSelectRegion={(reg) => {
                  setSelectedRegion(reg);
                }}
              />
            </div>

            {selectedRegion && (
              <RegionDrawer
                region={selectedRegion}
                onClose={() => setSelectedRegion(null)}
                isBookmarked={bookmarks.includes(selectedRegion.region)}
                onToggleBookmark={toggleBookmark}
              />
            )}
          </div>
        )}

        {activeTab === 'feeds' && (
          <RawFeedsView regions={regions} />
        )}
      </main>
    </div>
  );
}
