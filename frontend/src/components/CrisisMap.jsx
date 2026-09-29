import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { Search, ShieldAlert } from 'lucide-react';
import './mapTooltip.css';

const CATEGORY_COLORS = {
  'Neglected Emergency': '#e02424',
  'Escalating Hotspot': '#d97706',
  'Protracted Crisis': '#0284c7',
  'Stabilized Response': '#16a34a'
};

export default function CrisisMap({
  regions = [],
  selectedRegion,
  onSelectRegion,
  filterCategory,
  setFilterCategory,
  searchQuery,
  setSearchQuery,
  showOnlyAnomalies,
  setShowOnlyAnomalies
}) {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersLayerRef = useRef(null);

  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (mapContainerRef.current._leaflet_id) {
      delete mapContainerRef.current._leaflet_id;
    }

    if (mapInstanceRef.current) {
      mapInstanceRef.current.remove();
      mapInstanceRef.current = null;
    }

    const map = L.map(mapContainerRef.current, {
      center: [20.0, 30.0],
      zoom: 3,
      minZoom: 2,
      maxZoom: 12,
      zoomControl: false
    });

    L.control.zoom({ position: 'topright' }).addTo(map);

    // Free, crisp, public OpenStreetMap tile layer (no API key required, reliable worldwide tiles)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | GDELT & UN OCHA',
      subdomains: ['a', 'b', 'c']
    }).addTo(map);

    const markersGroup = L.layerGroup().addTo(map);
    markersLayerRef.current = markersGroup;
    mapInstanceRef.current = map;

    const t1 = setTimeout(() => map.invalidateSize(), 150);
    const t2 = setTimeout(() => map.invalidateSize(), 500);

    const handleResize = () => map.invalidateSize();
    window.addEventListener('resize', handleResize);

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      window.removeEventListener('resize', handleResize);
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  useEffect(() => {
    if (!mapInstanceRef.current || !markersLayerRef.current) return;

    const markersGroup = markersLayerRef.current;
    markersGroup.clearLayers();

    const filtered = regions.filter(item => {
      if (filterCategory !== 'ALL' && item.category !== filterCategory) return false;
      if (showOnlyAnomalies && !item.is_anomaly) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchesName = item.region.toLowerCase().includes(q);
        const matchesCode = item.country_code?.toLowerCase().includes(q);
        if (!matchesName && !matchesCode) return false;
      }
      return true;
    });

    filtered.forEach(item => {
      const color = CATEGORY_COLORS[item.category] || '#0071e3';
      const isSelected = selectedRegion?.region === item.region;
      const isAnomaly = item.is_anomaly;

      const radius = Math.min(22, Math.max(12, Math.round(Math.sqrt(item.media_volume_24h || 100) * 0.48)));

      if (isAnomaly) {
        L.circleMarker([item.lat, item.lon], {
          radius: radius + 8,
          color: '#9333ea',
          weight: 2,
          dashArray: '4, 4',
          fillColor: '#9333ea',
          fillOpacity: 0.15,
          interactive: false
        }).addTo(markersGroup);
      }

      const circle = L.circleMarker([item.lat, item.lon], {
        radius: isSelected ? radius + 4 : radius,
        fillColor: color,
        fillOpacity: 0.95,
        color: '#ffffff',
        weight: isSelected ? 3.5 : 2.5,
      }).addTo(markersGroup);

      circle.bindTooltip(
        `<span style="font-weight:700;">${item.region}</span> <span style="color:${color};font-family:monospace;font-weight:700;">${(item.gap_score || 0).toFixed(1)}</span>`,
        {
          permanent: true,
          direction: 'top',
          offset: [0, -radius - 4],
          className: 'apple-map-tooltip'
        }
      );

      const popupHtml = `
        <div class="map-popup">
          <div class="popup-header">
            <span class="popup-flag">${item.country_code || 'UN'}</span>
            <strong class="popup-title">${item.region}</strong>
          </div>
          <div class="popup-category" style="color: ${color}; font-weight: 600;">
            ${item.category}
          </div>
          <div class="popup-stats">
            <div>
              <span class="stat-label">Disparity Gap:</span>
              <span class="stat-value font-mono">${(item.gap_score || 0).toFixed(2)} / 10</span>
            </div>
            <div>
              <span class="stat-label">24h Media Volume:</span>
              <span class="stat-value font-mono">${item.media_volume_24h?.toLocaleString() || 0}</span>
            </div>
            <div>
              <span class="stat-label">UN SitReps & Appeals:</span>
              <span class="stat-value font-mono">${item.reliefweb_response_count || 0}</span>
            </div>
            ${item.is_anomaly ? `<div class="popup-anomaly-tag">Outlier Disparity Detected</div>` : ''}
          </div>
          <button class="popup-btn" id="inspect-btn-${item.country_code}">
            View Hotspot Dossier &rarr;
          </button>
        </div>
      `;

      circle.bindPopup(popupHtml, { maxWidth: 280 });

      circle.on('popupopen', () => {
        const btn = document.getElementById(`inspect-btn-${item.country_code}`);
        if (btn) {
          btn.onclick = () => onSelectRegion(item);
        }
      });

      circle.on('click', () => {
        onSelectRegion(item);
      });
    });
  }, [regions, filterCategory, searchQuery, showOnlyAnomalies, selectedRegion]);

  useEffect(() => {
    if (selectedRegion && mapInstanceRef.current) {
      mapInstanceRef.current.flyTo([selectedRegion.lat, selectedRegion.lon], 5, {
        duration: 1.2,
        easeLinearity: 0.25
      });
    }
  }, [selectedRegion]);

  return (
    <div className="map-view-wrapper">
      <div className="map-controls-panel">
        <div className="map-search-bar">
          <Search size={15} className="text-muted" />
          <input
            type="text"
            placeholder="Search hotspot (e.g. Sudan, Ukraine)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="map-search-input"
          />
        </div>

        <div className="map-filter-tags">
          <button
            className={`filter-chip ${filterCategory === 'ALL' ? 'active' : ''}`}
            onClick={() => setFilterCategory('ALL')}
          >
            All Crises ({regions.length})
          </button>
          <button
            className={`filter-chip chip-neglected ${filterCategory === 'Neglected Emergency' ? 'active' : ''}`}
            onClick={() => setFilterCategory('Neglected Emergency')}
          >
            Neglected
          </button>
          <button
            className={`filter-chip chip-escalating ${filterCategory === 'Escalating Hotspot' ? 'active' : ''}`}
            onClick={() => setFilterCategory('Escalating Hotspot')}
          >
            Escalating
          </button>
          <button
            className={`filter-chip chip-protracted ${filterCategory === 'Protracted Crisis' ? 'active' : ''}`}
            onClick={() => setFilterCategory('Protracted Crisis')}
          >
            Protracted
          </button>
          <button
            className={`filter-chip chip-stabilized ${filterCategory === 'Stabilized Response' ? 'active' : ''}`}
            onClick={() => setFilterCategory('Stabilized Response')}
          >
            Stabilized
          </button>
          <button
            className={`filter-chip chip-anomaly ${showOnlyAnomalies ? 'active' : ''}`}
            onClick={() => setShowOnlyAnomalies(!showOnlyAnomalies)}
          >
            <ShieldAlert size={13} />
            Anomalies
          </button>
        </div>
      </div>

      <div className="map-legend-panel">
        <div className="legend-title">Classification</div>
        <div className="legend-items">
          <div className="legend-item">
            <span className="legend-dot" style={{ background: '#e02424' }}></span>
            <span>Neglected (High gap, response lag)</span>
          </div>
          <div className="legend-item">
            <span className="legend-dot" style={{ background: '#d97706' }}></span>
            <span>Escalating (Surging coverage &gt;1.35x)</span>
          </div>
          <div className="legend-item">
            <span className="legend-dot" style={{ background: '#0284c7' }}></span>
            <span>Protracted (Sustained baseline)</span>
          </div>
          <div className="legend-item">
            <span className="legend-dot" style={{ background: '#16a34a' }}></span>
            <span>Stabilized (Proportional response)</span>
          </div>
        </div>
      </div>

      <div ref={mapContainerRef} className="leaflet-map-canvas" />
    </div>
  );
}
