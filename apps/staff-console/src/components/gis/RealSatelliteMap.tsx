import React, { useEffect, useRef, useState, useCallback } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Satellite, Map as MapIcon, RotateCcw, ZoomIn, ZoomOut, AlertCircle } from 'lucide-react';

export interface IncidentCluster {
  cluster_id: number;
  incident_count: number;
  centroid: {
    type?: string;
    coordinates: [number, number]; // [lon, lat]
  };
  incident_ids: string[];
  dominant_category?: string;
  ward_name?: string;
  ward_number?: number;
  confidence_score?: number;
}

export interface RealSatelliteMapProps {
  clusters?: IncidentCluster[];
  selectedClusterId?: number | null;
  onSelectCluster?: (cluster: IncidentCluster) => void;
  wardsGeoJSON?: GeoJSON.FeatureCollection | null;
  incidentsGeoJSON?: GeoJSON.FeatureCollection | null;
  showWards?: boolean;
  showClusters?: boolean;
  showIncidents?: boolean;
  showDensityHeatmap?: boolean;
  center?: [number, number]; // [lat, lon]
  zoom?: number;
  className?: string;
}

const ESRI_SATELLITE_URL = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
const ESRI_LABELS_URL = 'https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}';
const OSM_STREETS_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

export const RealSatelliteMap: React.FC<RealSatelliteMapProps> = ({
  clusters = [],
  selectedClusterId = null,
  onSelectCluster,
  wardsGeoJSON = null,
  incidentsGeoJSON = null,
  showWards = true,
  showClusters = true,
  showIncidents = true,
  center = [12.9716, 77.5946], // Default Bengaluru coordinates
  zoom = 13,
  className = '',
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);

  // Layer group refs
  const satelliteTilesRef = useRef<L.TileLayer | null>(null);
  const satelliteLabelsRef = useRef<L.TileLayer | null>(null);
  const streetTilesRef = useRef<L.TileLayer | null>(null);
  const wardsLayerGroupRef = useRef<L.GeoJSON | null>(null);
  const clustersLayerGroupRef = useRef<L.LayerGroup | null>(null);
  const incidentsLayerGroupRef = useRef<L.LayerGroup | null>(null);

  const [basemap, setBasemap] = useState<'satellite' | 'streets'>('satellite');

  // Initialize Map
  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapInstanceRef.current) {
      const map = L.map(mapContainerRef.current, {
        center,
        zoom,
        zoomControl: false, // We render clean custom controls
        attributionControl: false,
      });

      // Add Attribution cleanly in bottom-right
      L.control
        .attribution({ position: 'bottomright', prefix: 'CivicBrain GIS' })
        .addAttribution('&copy; Esri &bull; &copy; OpenStreetMap')
        .addTo(map);

      // Create base layers
      const sat = L.tileLayer(ESRI_SATELLITE_URL, {
        maxZoom: 19,
        attribution: 'Tiles &copy; Esri',
      });

      const satLabels = L.tileLayer(ESRI_LABELS_URL, {
        maxZoom: 19,
        pane: 'overlayPane',
      });

      const streets = L.tileLayer(OSM_STREETS_URL, {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors',
      });

      // Add default satellite basemap
      sat.addTo(map);
      satLabels.addTo(map);

      satelliteTilesRef.current = sat;
      satelliteLabelsRef.current = satLabels;
      streetTilesRef.current = streets;

      // Create overlay layer groups
      clustersLayerGroupRef.current = L.layerGroup().addTo(map);
      incidentsLayerGroupRef.current = L.layerGroup().addTo(map);

      mapInstanceRef.current = map;

      // Handle window resize cleanly
      const resizeObserver = new ResizeObserver(() => {
        map.invalidateSize();
      });
      resizeObserver.observe(mapContainerRef.current);

      return () => {
        resizeObserver.disconnect();
        map.remove();
        mapInstanceRef.current = null;
      };
    }
  }, []);

  // Switch basemap between Satellite and Streets
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map) return;

    if (basemap === 'satellite') {
      if (streetTilesRef.current) map.removeLayer(streetTilesRef.current);
      if (satelliteTilesRef.current && !map.hasLayer(satelliteTilesRef.current)) {
        satelliteTilesRef.current.addTo(map);
      }
      if (satelliteLabelsRef.current && !map.hasLayer(satelliteLabelsRef.current)) {
        satelliteLabelsRef.current.addTo(map);
      }
    } else {
      if (satelliteTilesRef.current) map.removeLayer(satelliteTilesRef.current);
      if (satelliteLabelsRef.current) map.removeLayer(satelliteLabelsRef.current);
      if (streetTilesRef.current && !map.hasLayer(streetTilesRef.current)) {
        streetTilesRef.current.addTo(map);
      }
    }
  }, [basemap]);

  // Render Ward Boundaries (GeoJSON)
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map) return;

    if (wardsLayerGroupRef.current) {
      map.removeLayer(wardsLayerGroupRef.current);
      wardsLayerGroupRef.current = null;
    }

    if (showWards && wardsGeoJSON && wardsGeoJSON.features && wardsGeoJSON.features.length > 0) {
      const isSat = basemap === 'satellite';
      const geoLayer = L.geoJSON(wardsGeoJSON, {
        style: () => ({
          color: isSat ? '#38bdf8' : '#0284c7', // Sky blue for satellite, civic blue for streets
          weight: 2,
          dashArray: '5, 5',
          fillColor: isSat ? '#0284c7' : '#38bdf8',
          fillOpacity: isSat ? 0.15 : 0.1,
        }),
        onEachFeature: (feature, layer) => {
          const props = feature.properties || {};
          const wardName = props.name || 'नगर प्रभाग';
          const wardNum = props.ward_number != null ? `प्रभाग ${props.ward_number}` : '';
          const wardCode = props.code || '';

          layer.bindTooltip(
            `<div style="font-family: inherit; font-size: 12px; line-height: 1.4;">
              <strong style="color: #0f172a;">${wardNum ? wardNum + ' — ' : ''}${wardName}</strong>
              ${wardCode ? `<div style="color: #64748b; font-size: 11px;">कोड: ${wardCode}</div>` : ''}
            </div>`,
            { sticky: true, opacity: 0.95 }
          );

          layer.on({
            mouseover: () => {
              if (layer instanceof L.Path) {
                layer.setStyle({ fillOpacity: 0.35, weight: 3 });
              }
            },
            mouseout: () => {
              if (layer instanceof L.Path) {
                layer.setStyle({ fillOpacity: isSat ? 0.15 : 0.1, weight: 2 });
              }
            },
          });
        },
      });

      geoLayer.addTo(map);
      wardsLayerGroupRef.current = geoLayer;

      // Fit bounds to wards if available
      try {
        const bounds = geoLayer.getBounds();
        if (bounds.isValid()) {
          map.fitBounds(bounds, { padding: [30, 30] });
        }
      } catch (e) {
        // Fallback gracefully
      }
    }
  }, [wardsGeoJSON, showWards, basemap]);

  // Render Clusters
  useEffect(() => {
    const map = mapInstanceRef.current;
    const group = clustersLayerGroupRef.current;
    if (!map || !group) return;

    group.clearLayers();

    if (!showClusters || !clusters || clusters.length === 0) return;

    clusters.forEach((cluster) => {
      const coords = cluster.centroid?.coordinates;
      if (!coords || coords.length < 2) return;

      const [lon, lat] = coords;
      const isSelected = selectedClusterId === cluster.cluster_id;
      const count = cluster.incident_count || 1;

      // Calculate dynamic radius
      const radius = Math.min(30, Math.max(12, 10 + Math.sqrt(count) * 2.5));

      // Outer glow / pulse circle
      const outerCircle = L.circleMarker([lat, lon], {
        radius: radius + (isSelected ? 8 : 4),
        color: isSelected ? '#ea580c' : '#dc2626',
        weight: isSelected ? 3 : 1.5,
        fillColor: '#ef4444',
        fillOpacity: isSelected ? 0.35 : 0.2,
      });

      // Inner core marker
      const coreCircle = L.circleMarker([lat, lon], {
        radius,
        color: '#ffffff',
        weight: 2,
        fillColor: isSelected ? '#ea580c' : '#dc2626',
        fillOpacity: 0.9,
      });

      // Number label HTML marker
      const labelIcon = L.divIcon({
        className: 'cluster-count-label',
        html: `<div style="
          color: white; 
          font-weight: 700; 
          font-size: ${count > 99 ? '10px' : '11px'}; 
          text-align: center; 
          line-height: ${radius * 2}px; 
          pointer-events: none;
          text-shadow: 0 1px 2px rgba(0,0,0,0.8);
        ">${count}</div>`,
        iconSize: [radius * 2, radius * 2],
        iconAnchor: [radius, radius],
      });

      const labelMarker = L.marker([lat, lon], {
        icon: labelIcon,
        interactive: false,
      });

      // Click handler
      const handleClick = () => {
        if (onSelectCluster) onSelectCluster(cluster);
      };

      coreCircle.on('click', handleClick);
      outerCircle.on('click', handleClick);

      // Popup
      const popupContent = `
        <div style="font-family: inherit; font-size: 12px; line-height: 1.5; min-width: 180px;">
          <div style="font-weight: 700; color: #dc2626; font-size: 13px; margin-bottom: 4px;">
            हॉटस्पॉट #${cluster.cluster_id}
          </div>
          <div style="margin-bottom: 2px;">
            <strong>शिकायतें:</strong> ${count} मामले
          </div>
          ${cluster.dominant_category ? `<div style="margin-bottom: 2px;"><strong>प्रमुख श्रेणी:</strong> ${cluster.dominant_category}</div>` : ''}
          ${cluster.ward_name ? `<div style="margin-bottom: 2px;"><strong>प्रभाग:</strong> ${cluster.ward_name}</div>` : ''}
          <div style="color: #64748b; font-size: 11px; margin-top: 4px;">
            निर्देशांक: ${lat.toFixed(4)}° N, ${lon.toFixed(4)}° E
          </div>
        </div>
      `;

      coreCircle.bindPopup(popupContent);

      group.addLayer(outerCircle);
      group.addLayer(coreCircle);
      group.addLayer(labelMarker);
    });
  }, [clusters, selectedClusterId, showClusters, onSelectCluster]);

  // Render Individual Incident Points
  useEffect(() => {
    const map = mapInstanceRef.current;
    const group = incidentsLayerGroupRef.current;
    if (!map || !group) return;

    group.clearLayers();

    if (!showIncidents || !incidentsGeoJSON || !incidentsGeoJSON.features) return;

    incidentsGeoJSON.features.forEach((feature) => {
      const geom = feature.geometry;
      if (!geom || geom.type !== 'Point' || !geom.coordinates) return;

      const [lon, lat] = geom.coordinates;
      const props = feature.properties || {};

      const marker = L.circleMarker([lat, lon], {
        radius: 5,
        color: '#ffffff',
        weight: 1.5,
        fillColor: '#f97316', // Orange
        fillOpacity: 0.85,
      });

      marker.bindTooltip(
        `<div style="font-size: 11px;">
          <strong>श्रेणी:</strong> ${props.category_code || 'सामान्य'}<br/>
          <strong>स्थिति:</strong> ${props.status || 'Reported'}
        </div>`,
        { opacity: 0.95 }
      );

      group.addLayer(marker);
    });
  }, [incidentsGeoJSON, showIncidents]);

  // Custom Controls Action Handlers
  const handleZoomIn = () => {
    mapInstanceRef.current?.zoomIn();
  };

  const handleZoomOut = () => {
    mapInstanceRef.current?.zoomOut();
  };

  const handleResetView = () => {
    if (!mapInstanceRef.current) return;
    if (wardsLayerGroupRef.current) {
      const bounds = wardsLayerGroupRef.current.getBounds();
      if (bounds.isValid()) {
        mapInstanceRef.current.fitBounds(bounds, { padding: [30, 30] });
        return;
      }
    }
    mapInstanceRef.current.setView(center, zoom);
  };

  return (
    <div className={`relative w-full h-full overflow-hidden ${className}`}>
      {/* Real Leaflet Map Container */}
      <div ref={mapContainerRef} className="w-full h-full z-0 bg-slate-900" />

      {/* Floating Map Controls & Indian Context Tiles Switcher */}
      <div className="absolute top-4 right-4 z-20 flex flex-col items-end gap-2.5">
        {/* Basemap Switcher (Satellite vs Streets) */}
        <div className="bg-white/95 backdrop-blur-md border border-slate-200 shadow-md rounded-lg p-1 flex items-center gap-1">
          <button
            onClick={() => setBasemap('satellite')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
              basemap === 'satellite'
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
            }`}
            title="उपग्रह दृश्य (Satellite View)"
            aria-label="Switch to satellite view"
          >
            <Satellite className="w-3.5 h-3.5" />
            <span>उपग्रह / Satellite</span>
          </button>
          <button
            onClick={() => setBasemap('streets')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
              basemap === 'streets'
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
            }`}
            title="सड़क मानचित्र (Street View)"
            aria-label="Switch to street view"
          >
            <MapIcon className="w-3.5 h-3.5" />
            <span>सड़क / Streets</span>
          </button>
        </div>

        {/* Zoom & Reset Controls */}
        <div className="bg-white/95 backdrop-blur-md border border-slate-200 shadow-md rounded-lg flex flex-col p-1 gap-1">
          <button
            onClick={handleZoomIn}
            className="p-2 text-slate-700 hover:text-slate-900 hover:bg-slate-100 rounded-md transition-colors"
            title="ज़ूम इन (Zoom In)"
            aria-label="Zoom in"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={handleZoomOut}
            className="p-2 text-slate-700 hover:text-slate-900 hover:bg-slate-100 rounded-md transition-colors"
            title="ज़ूम आउट (Zoom Out)"
            aria-label="Zoom out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <div className="w-full h-px bg-slate-200 my-0.5" />
          <button
            onClick={handleResetView}
            className="p-2 text-slate-700 hover:text-slate-900 hover:bg-slate-100 rounded-md transition-colors"
            title="शहर केंद्रित करें (Reset to City Extent)"
            aria-label="Reset map view"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Real-time Satellite Map Legend */}
      <div className="absolute bottom-4 left-4 z-20 bg-white/90 backdrop-blur-md border border-slate-200 rounded-lg px-3 py-2 text-[11px] text-slate-700 shadow-md flex items-center gap-4">
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-red-600 ring-2 ring-red-300" />
          <span className="font-medium">हॉटस्पॉट क्लस्टर (Hotspots)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-orange-500" />
          <span>शिकायत स्थल (Incidents)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3.5 h-0.5 border-b-2 border-dashed border-sky-500" />
          <span>प्रभाग सीमाएं (Wards)</span>
        </div>
      </div>
    </div>
  );
};
