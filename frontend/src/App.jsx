import React, { useState, useEffect, useCallback } from 'react';
import Navbar from './components/Navbar';
import KpiBar from './components/KpiBar';
import CrisisMap from './components/CrisisMap';
import RegionDrawer from './components/RegionDrawer';
import GapScoresTable from './components/GapScoresTable';
import AnomalyRadar from './components/AnomalyRadar';
import RawFeedsView from './components/RawFeedsView';
import AuthModal from './components/AuthModal';
import {
  fetchAnalyticsOverview,
  fetchHealth,
  SEED_HOTSPOTS,
  getStoredAuth,
  clearStoredAuth,
  fetchCurrentUser,
  fetchServerWatchlist,
  addServerWatchlist,
  removeServerWatchlist
} from './services/api';
import './App.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('map');
  const [regions, setRegions] = useState(SEED_HOTSPOTS);
  const [stats, setStats] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [drawerTab, setDrawerTab] = useState('overview');
  const [isLive, setIsLive] = useState(false);
  const [health, setHealth] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // User Auth & Modal States
  const [currentUser, setCurrentUser] = useState(() => getStoredAuth().user);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  const handleSelectRegion = (region, tab = 'overview') => {
    setSelectedRegion(region);
    setDrawerTab(tab);
  };

  // Filter states
  const [filterCategory, setFilterCategory] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [showOnlyAnomalies, setShowOnlyAnomalies] = useState(false);

  // Watchlist stored in localStorage + synced with server if logged in
  const [bookmarks, setBookmarks] = useState(() => {
    try {
      const saved = localStorage.getItem('crisispulse_bookmarks');
      return saved ? JSON.parse(saved) : ['Sudan', 'Gaza / Palestine'];
    } catch {
      return ['Sudan', 'Gaza / Palestine'];
    }
  });

  // Verify auth session & sync server watchlists
  useEffect(() => {
    async function initAuth() {
      const user = await fetchCurrentUser();
      if (user) {
        setCurrentUser(user);
        const serverItems = await fetchServerWatchlist();
        if (serverItems && serverItems.length > 0) {
          setBookmarks(serverItems);
          try {
            localStorage.setItem('crisispulse_bookmarks', JSON.stringify(serverItems));
          } catch (e) {
            console.warn(e);
          }
        }
      } else {
        const stored = getStoredAuth();
        if (stored.token) {
          clearStoredAuth();
          setCurrentUser(null);
        }
      }
    }
    initAuth();
  }, []);

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

  const toggleBookmark = async (regionName) => {
    const isCurrentlyBookmarked = bookmarks.includes(regionName);
    const next = isCurrentlyBookmarked
      ? bookmarks.filter(r => r !== regionName)
      : [...bookmarks, regionName];

    setBookmarks(next);
    try {
      localStorage.setItem('crisispulse_bookmarks', JSON.stringify(next));
    } catch (e) {
      console.warn('Could not persist watchlist to localStorage', e);
    }

    if (currentUser) {
      if (isCurrentlyBookmarked) {
        await removeServerWatchlist(regionName);
      } else {
        await addServerWatchlist(regionName);
      }
    }
  };

  const handleAuthSuccess = async (user) => {
    setCurrentUser(user);
    const serverItems = await fetchServerWatchlist();
    if (serverItems && serverItems.length > 0) {
      setBookmarks(serverItems);
      localStorage.setItem('crisispulse_bookmarks', JSON.stringify(serverItems));
    } else {
      // Sync local bookmarks to server
      for (const item of bookmarks) {
        await addServerWatchlist(item);
      }
    }
  };

  const handleLogout = () => {
    clearStoredAuth();
    setCurrentUser(null);
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
        currentUser={currentUser}
        onOpenAuth={() => setIsAuthModalOpen(true)}
        onLogout={handleLogout}
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
              onSelectRegion={handleSelectRegion}
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
                initialSubTab={drawerTab}
              />
            )}
          </div>
        )}

        {activeTab === 'rankings' && (
          <div className="workspace-layout">
            <div style={{ flex: 1 }}>
              <GapScoresTable
                regions={regions}
                onSelectRegion={handleSelectRegion}
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
                initialSubTab={drawerTab}
              />
            )}
          </div>
        )}

        {activeTab === 'anomalies' && (
          <div className="workspace-layout">
            <div style={{ flex: 1 }}>
              <AnomalyRadar
                regions={regions}
                onSelectRegion={(reg, tab) => handleSelectRegion(reg, tab || 'explainability')}
              />
            </div>

            {selectedRegion && (
              <RegionDrawer
                region={selectedRegion}
                onClose={() => setSelectedRegion(null)}
                isBookmarked={bookmarks.includes(selectedRegion.region)}
                onToggleBookmark={toggleBookmark}
                initialSubTab={drawerTab}
              />
            )}
          </div>
        )}

        {activeTab === 'feeds' && (
          <RawFeedsView regions={regions} />
        )}
      </main>

      {/* Auth Modal */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onAuthSuccess={handleAuthSuccess}
      />
    </div>
  );
}

