import React, { useState, useMemo, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Button,
  IconButton,
  Switch,
  ConfidenceBadge,
  Skeleton,
} from '@civicbrain/ui';
import { CoordinateRulerFrame } from '../components/gis/CoordinateRulerFrame';
import { ClusterStatsPanel, ClusterData } from '../components/gis/ClusterStatsPanel';
import { ClusterAccessibleListView } from '../components/gis/ClusterAccessibleListView';
import { useGsapClusterReveal } from '../components/gis/useGsapClusterReveal';
import {
  Layers,
  MapPin,
  ZoomIn,
  ZoomOut,
  RefreshCw,
  AlertCircle,
  Eye,
  Sliders,
  List,
  Map as MapIcon,
  HelpCircle,
  Sparkles,
} from 'lucide-react';

/**
 * Cluster radius calculation strictly from DESIGN.md §3.4:
 * --map-point-radius-cluster: clamp(8px, calc(8px + sqrt(var(--cluster-count)) * 1.5px), 28px)
 */
export const calculateClusterRadius = (count: number): number => {
  return Math.min(28, Math.max(8, 8 + Math.sqrt(count) * 1.5));
};

// Initial realistic test clusters with >=3 distinct cluster sizes
const MOCK_CLUSTERS: ClusterData[] = [
  {
    cluster_id: 101,
    incident_count: 4, // Size 1: 4 points -> ~11.0px
    centroid: {
      type: 'Point',
      coordinates: [77.585, 12.985],
    },
    incident_ids: ['inc-001', 'inc-002', 'inc-003', 'inc-004'],
    confidence_score: 0.64,
    dominant_category: 'Streetlighting',
    ward_name: 'Malleshwaram',
    ward_number: 101,
    category_breakdown: [
      { category: 'Streetlighting', count: 3, percentage: 75 },
      { category: 'Drainage', count: 1, percentage: 25 },
    ],
    severity_breakdown: { critical: 0, major: 2, minor: 2 },
  },
  {
    cluster_id: 102,
    incident_count: 19, // Size 2: 19 points -> ~14.54px
    centroid: {
      type: 'Point',
      coordinates: [77.575, 12.965],
    },
    incident_ids: Array.from({ length: 19 }, (_, i) => `inc-102-${i + 1}`),
    confidence_score: 0.88,
    dominant_category: 'Solid Waste / Drainage',
    ward_name: 'Rajajinagar',
    ward_number: 102,
    category_breakdown: [
      { category: 'Solid Waste', count: 11, percentage: 58 },
      { category: 'Drainage', count: 6, percentage: 32 },
      { category: 'Road Hazards', count: 2, percentage: 10 },
    ],
    severity_breakdown: { critical: 3, major: 10, minor: 6 },
  },
  {
    cluster_id: 103,
    incident_count: 45, // Size 3: 45 points -> ~18.06px
    centroid: {
      type: 'Point',
      coordinates: [77.605, 12.972],
    },
    incident_ids: Array.from({ length: 45 }, (_, i) => `inc-103-${i + 1}`),
    confidence_score: 0.95,
    dominant_category: 'Water Supply / Potholes',
    ward_name: 'Gandhinagar',
    ward_number: 103,
    category_breakdown: [
      { category: 'Water Supply', count: 24, percentage: 53 },
      { category: 'Potholes', count: 16, percentage: 36 },
      { category: 'Sewage', count: 5, percentage: 11 },
    ],
    severity_breakdown: { critical: 8, major: 25, minor: 12 },
  },
  {
    cluster_id: 104,
    incident_count: 200, // Size 4: 200 points -> 28.0px (clamped max)
    centroid: {
      type: 'Point',
      coordinates: [77.618, 12.98],
    },
    incident_ids: Array.from({ length: 200 }, (_, i) => `inc-104-${i + 1}`),
    confidence_score: 0.99,
    dominant_category: 'Commercial Corridor Defect Hotspot',
    ward_name: 'Shivaji Nagar',
    ward_number: 104,
    category_breakdown: [
      { category: 'Potholes / Asphalt', count: 88, percentage: 44 },
      { category: 'Solid Waste', count: 62, percentage: 31 },
      { category: 'Streetlights', count: 50, percentage: 25 },
    ],
    severity_breakdown: { critical: 42, major: 110, minor: 48 },
  },
];

// Municipal Wards Polygons (simplified SVG paths for visualization)
const MOCK_WARDS = [
  { id: 101, name: 'Malleshwaram', code: 'W-101', path: 'M 100,50 L 320,40 L 350,220 L 120,240 Z' },
  { id: 102, name: 'Rajajinagar', code: 'W-102', path: 'M 80,250 L 340,230 L 320,440 L 90,420 Z' },
  { id: 103, name: 'Gandhinagar', code: 'W-103', path: 'M 360,60 L 620,80 L 640,300 L 370,260 Z' },
  { id: 104, name: 'Shivaji Nagar', code: 'W-104', path: 'M 630,90 L 880,110 L 860,420 L 650,320 Z' },
];

// Synthetic background incident scatter points
const MOCK_INCIDENTS = [
  { x: 140, y: 80, cat: 'Streetlighting' },
  { x: 190, y: 120, cat: 'Streetlighting' },
  { x: 220, y: 90, cat: 'Drainage' },
  { x: 260, y: 140, cat: 'Drainage' },
  { x: 180, y: 310, cat: 'Solid Waste' },
  { x: 210, y: 290, cat: 'Solid Waste' },
  { x: 250, y: 340, cat: 'Drainage' },
  { x: 290, y: 320, cat: 'Road Hazards' },
  { x: 420, y: 140, cat: 'Water Supply' },
  { x: 460, y: 180, cat: 'Water Supply' },
  { x: 490, y: 160, cat: 'Potholes' },
  { x: 530, y: 210, cat: 'Sewage' },
  { x: 720, y: 160, cat: 'Potholes' },
  { x: 760, y: 220, cat: 'Solid Waste' },
  { x: 800, y: 260, cat: 'Streetlights' },
];

export const HeatmapClusterView: React.FC = () => {
  const navigate = useNavigate();

  // Layer Controls State
  const [showWards, setShowWards] = useState(true);
  const [showIncidents, setShowIncidents] = useState(true);
  const [showClusters, setShowClusters] = useState(true);
  const [showDensityHeatmap, setShowDensityHeatmap] = useState(false);

  // Clustering tuning parameters
  const [epsMeters, setEpsMeters] = useState(100);
  const [minPoints, setMinPoints] = useState(3);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  // UI state
  const [viewMode, setViewMode] = useState<'map' | 'list'>('map');
  const [zoomLevel, setZoomLevel] = useState(13);
  const [selectedCluster, setSelectedCluster] = useState<ClusterData | null>(MOCK_CLUSTERS[1]);
  const [isLoading, setIsLoading] = useState(false);
  const [dataError, setDataError] = useState<string | null>(null);

  // Filter clusters based on category and minPoints
  const filteredClusters = useMemo(() => {
    return MOCK_CLUSTERS.filter((c) => {
      if (c.incident_count < minPoints) return false;
      if (selectedCategory !== 'all' && !c.dominant_category.toLowerCase().includes(selectedCategory.toLowerCase())) {
        return false;
      }
      return true;
    });
  }, [minPoints, selectedCategory]);

  // GSAP Cluster Reveal Hook
  const { containerRef } = useGsapClusterReveal({
    triggerKey: `${zoomLevel}-${filteredClusters.length}-${showClusters}`,
    selector: '.gsap-cluster-circle',
    getTargetRadius: (circle) => {
      const count = parseInt(circle.getAttribute('data-point-count') || '10', 10);
      return calculateClusterRadius(count);
    },
  });

  const handleZoomIn = () => setZoomLevel((z) => Math.min(18, z + 1));
  const handleZoomOut = () => setZoomLevel((z) => Math.max(9, z - 1));

  const handleInspectIncidents = (cluster: ClusterData) => {
    navigate('/deck');
  };

  const isTooZoomedInForClusters = zoomLevel >= 16;

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)] font-ui bg-background text-primary overflow-hidden">
      {/* City Pulse Sub-header / Command Bar */}
      <header className="h-13 px-4 sm:px-6 border-b border-border bg-surface flex items-center justify-between shrink-0 z-20">
        <div className="flex items-center gap-3">
          <div className="w-2.5 h-2.5 rounded-full bg-channel-600 animate-pulse" />
          <div>
            <h1 className="text-base font-semibold text-primary tracking-tight">
              City Pulse — Hotspot & Cluster Spatial Analysis
            </h1>
            <p className="text-[11px] font-mono text-secondary">
              DBSCAN In-Database Defect Hotspots • POSTGIS ST_ClusterDBSCAN
            </p>
          </div>
        </div>

        {/* View Switcher & Action Controls */}
        <div className="flex items-center gap-2">
          <div className="flex items-center bg-field-100 p-0.5 border border-border rounded-sm">
            <button
              onClick={() => setViewMode('map')}
              className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-xs transition-colors ${
                viewMode === 'map'
                  ? 'bg-surface text-primary shadow-xs'
                  : 'text-secondary hover:text-primary'
              }`}
              aria-pressed={viewMode === 'map'}
            >
              <MapIcon className="w-3.5 h-3.5" />
              <span>Map View</span>
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-xs transition-colors ${
                viewMode === 'list'
                  ? 'bg-surface text-primary shadow-xs'
                  : 'text-secondary hover:text-primary'
              }`}
              aria-pressed={viewMode === 'list'}
            >
              <List className="w-3.5 h-3.5" />
              <span>Accessible List</span>
            </button>
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setIsLoading(true);
              setTimeout(() => setIsLoading(false), 500);
            }}
            disabled={isLoading}
            className="hidden sm:flex text-xs"
          >
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Re-query GIS</span>
          </Button>
        </div>
      </header>

      {/* Non-blocking Layer Error Banner (SCREEN_SPECS.md §2.12: doesn't fail the whole map) */}
      {dataError && (
        <div
          role="alert"
          className="bg-status-warning/15 border-b border-status-warning/30 px-4 py-2 flex items-center justify-between text-xs text-primary z-30"
        >
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-status-warning shrink-0" />
            <span>{dataError}</span>
          </div>
          <button
            onClick={() => setDataError(null)}
            className="font-mono text-xs text-status-warning underline hover:opacity-80"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Main Layout: 280px Left Rail + Map / List Container */}
      <div className="flex flex-1 overflow-hidden relative">
        {/* 280px Left Layer Control Rail (SCREEN_SPECS.md §2.12) */}
        <aside
          role="region"
          aria-label="GIS Layer Controls & DBSCAN Filters"
          className="w-72 shrink-0 border-r border-border bg-surface flex flex-col justify-between overflow-y-auto z-10"
        >
          <div className="p-4 space-y-6">
            {/* Layer Visibility Toggles */}
            <div className="space-y-3">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-secondary uppercase font-mono tracking-wider">
                <Layers className="w-3.5 h-3.5 text-channel-600" />
                <span>Map Layers</span>
              </div>

              <div className="space-y-2.5 text-xs bg-field-50/60 p-3 border border-border rounded-sm">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-0.5 border-b-2 border-dashed border-station-500" />
                    <span>Ward Boundaries</span>
                  </div>
                  <Switch
                    checked={showWards}
                    onCheckedChange={setShowWards}
                    aria-label="Toggle ward boundaries"
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-marker-500" />
                    <span>Incident Points (6px)</span>
                  </div>
                  <Switch
                    checked={showIncidents}
                    onCheckedChange={setShowIncidents}
                    aria-label="Toggle individual incident points"
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-status-danger border border-white" />
                    <span className="font-medium text-primary">DBSCAN Clusters</span>
                  </div>
                  <Switch
                    checked={showClusters}
                    onCheckedChange={setShowClusters}
                    aria-label="Toggle DBSCAN clusters"
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-xs bg-channel-500" />
                    <span>Density Heatmap</span>
                  </div>
                  <Switch
                    checked={showDensityHeatmap}
                    onCheckedChange={setShowDensityHeatmap}
                    aria-label="Toggle density heatmap gradient"
                  />
                </div>
              </div>
            </div>

            {/* Clustering Calibration (DBSCAN params) */}
            <div className="space-y-3">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-secondary uppercase font-mono tracking-wider">
                <Sliders className="w-3.5 h-3.5 text-channel-600" />
                <span>Hotspot Sensitivity</span>
              </div>

              <div className="space-y-4 p-3 bg-field-50/60 border border-border rounded-sm text-xs font-mono">
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-secondary">Radius (ε meters):</span>
                    <span className="font-semibold text-primary">{epsMeters}m</span>
                  </div>
                  <input
                    type="range"
                    min="30"
                    max="300"
                    step="10"
                    value={epsMeters}
                    onChange={(e) => setEpsMeters(Number(e.target.value))}
                    className="w-full accent-channel-600 cursor-pointer"
                    aria-label="Epsilon clustering distance in meters"
                  />
                </div>

                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-secondary">Min Incidents (min_pts):</span>
                    <span className="font-semibold text-primary">{minPoints}</span>
                  </div>
                  <input
                    type="range"
                    min="2"
                    max="15"
                    step="1"
                    value={minPoints}
                    onChange={(e) => setMinPoints(Number(e.target.value))}
                    className="w-full accent-channel-600 cursor-pointer"
                    aria-label="Minimum incidents required to form a cluster"
                  />
                </div>
              </div>
            </div>

            {/* Category Filter */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-secondary uppercase font-mono tracking-wider">
                Filter Category
              </label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full bg-field-50 border border-border rounded-sm text-xs font-mono p-2 focus:ring-1 focus:ring-focus outline-none text-primary"
                aria-label="Filter hotspots by incident category"
              >
                <option value="all">All Incident Categories</option>
                <option value="streetlighting">Streetlighting</option>
                <option value="drainage">Solid Waste / Drainage</option>
                <option value="water">Water Supply</option>
                <option value="potholes">Road Hazards / Potholes</option>
              </select>
            </div>

            {/* Cluster Stats Summary */}
            <div className="p-3 bg-field-100/60 border border-border rounded-sm space-y-1 text-xs">
              <div className="font-mono text-secondary text-[11px] uppercase">
                Active Spatial Read
              </div>
              <div className="font-semibold text-primary text-sm">
                {filteredClusters.length} Hotspots Detected
              </div>
              <p className="text-secondary text-[11px]">
                Showing {filteredClusters.reduce((acc, c) => acc + c.incident_count, 0)} total
                clustered incidents across 4 surveyed wards.
              </p>
            </div>
          </div>

          {/* Rail Footer */}
          <div className="p-3 border-t border-border bg-field-50 text-[10px] font-mono text-secondary">
            <span>DATA SOURCE: /v1/gis/clusters</span>
          </div>
        </aside>

        {/* View Content: Interactive Map OR Accessible List */}
        <main
          id="main-content"
          className="flex-1 relative h-full w-full overflow-hidden bg-field-50 flex flex-col"
        >
          {viewMode === 'list' ? (
            <div className="flex-1 overflow-y-auto">
              <ClusterAccessibleListView
                clusters={filteredClusters}
                selectedClusterId={selectedCluster?.cluster_id ?? null}
                onSelectCluster={(c) => {
                  setSelectedCluster(c);
                  setViewMode('map');
                }}
                calculateRadius={calculateClusterRadius}
              />
            </div>
          ) : (
            <CoordinateRulerFrame center={[77.5946, 12.9716]} zoom={zoomLevel}>
              {/* Zoom Out Warning Hint (SCREEN_SPECS.md §2.12: "zoom out" hint at empty-cluster zoom levels) */}
              {isTooZoomedInForClusters && (
                <div
                  role="status"
                  className="absolute top-4 left-1/2 -translate-x-1/2 z-30 bg-surface/95 border border-channel-600/40 shadow-lifted px-4 py-2 rounded-sm text-xs font-mono text-primary flex items-center gap-2"
                >
                  <AlertCircle className="w-4 h-4 text-channel-600" />
                  <span>Zoom out to see cluster density envelopes (Level: {zoomLevel})</span>
                  <button
                    onClick={handleZoomOut}
                    className="ml-2 underline text-channel-700 font-semibold"
                  >
                    Zoom Out
                  </button>
                </div>
              )}

              {/* Map Canvas & SVG Graphics */}
              <div
                className="relative w-full h-full flex items-center justify-center select-none"
                style={{
                  background:
                    'radial-gradient(circle at center, var(--field-100) 0%, var(--field-50) 100%)',
                }}
              >
                {/* Muted Surveying Vector Grid */}
                <div
                  className="absolute inset-0 pointer-events-none opacity-25"
                  style={{
                    backgroundImage: `
                      linear-gradient(to right, var(--station-400) 1px, transparent 1px),
                      linear-gradient(to bottom, var(--station-400) 1px, transparent 1px)
                    `,
                    backgroundSize: '40px 40px',
                  }}
                />

                {/* Basemap Skeleton Loader (DESIGN.md §10) */}
                {isLoading ? (
                  <div className="absolute inset-0 flex flex-col items-center justify-center bg-field-50/80 z-20 space-y-3">
                    <div className="w-48 h-3 bg-field-300 animate-pulse rounded-sm" />
                    <div className="w-32 h-2.5 bg-field-200 animate-pulse rounded-sm" />
                    <span className="font-mono text-xs text-secondary">
                      Loading GeoJSON Layers...
                    </span>
                  </div>
                ) : null}

                {/* SVG Spatial Layer Container */}
                <svg
                  ref={containerRef}
                  viewBox="0 0 1000 600"
                  className="w-full h-full cursor-grab active:cursor-grabbing"
                  aria-label="City Pulse Spatial Map Canvas"
                >
                  {/* Layer 1: Ward Boundaries (Dashed Station-500) */}
                  {showWards && (
                    <g
                      id="ward-boundaries-layer"
                      className="transition-opacity duration-220"
                      aria-label="Ward boundary polygons"
                    >
                      {MOCK_WARDS.map((ward) => (
                        <g key={ward.id}>
                          <path
                            d={ward.path}
                            fill="var(--color-surface)"
                            fillOpacity="0.35"
                            stroke="var(--color-gis-ward-boundary)"
                            strokeWidth="1.5"
                            strokeDasharray="4,4"
                            className="transition-colors hover:fill-channel-500/10"
                          />
                          <text
                            x={
                              ward.id === 101 ? 160 : ward.id === 102 ? 140 : ward.id === 103 ? 420 : 700
                            }
                            y={
                              ward.id === 101 ? 90 : ward.id === 102 ? 280 : ward.id === 103 ? 120 : 150
                            }
                            fill="var(--station-600)"
                            fontSize="11"
                            fontFamily="IBM Plex Mono"
                            fontWeight="500"
                            opacity="0.8"
                          >
                            {ward.code} • {ward.name}
                          </text>
                        </g>
                      ))}
                    </g>
                  )}

                  {/* Layer 2: Density Heatmap Gradient (Optional) */}
                  {showDensityHeatmap && (
                    <g id="density-heatmap-layer" opacity="0.4">
                      <circle cx="210" cy="110" r="90" fill="url(#heatGradient)" />
                      <circle cx="220" cy="310" r="110" fill="url(#heatGradient)" />
                      <circle cx="480" cy="180" r="140" fill="url(#heatGradient)" />
                      <circle cx="760" cy="220" r="160" fill="url(#heatGradient)" />
                    </g>
                  )}

                  {/* Layer 3: Incident Scatter Points (6px dots) */}
                  {showIncidents && (
                    <g id="incident-points-layer" className="transition-opacity duration-220">
                      {MOCK_INCIDENTS.map((inc, i) => (
                        <circle
                          key={i}
                          cx={inc.x}
                          cy={inc.y}
                          r="3"
                          fill="var(--color-gis-incident-point)"
                          stroke="var(--color-surface)"
                          strokeWidth="1"
                          opacity="0.75"
                        />
                      ))}
                    </g>
                  )}

                  {/* Layer 4: DBSCAN Clusters with Real Formula Radii & GSAP Reveal */}
                  {showClusters && !isTooZoomedInForClusters && (
                    <g id="dbscan-clusters-layer">
                      {filteredClusters.map((cluster) => {
                        const radius = calculateClusterRadius(cluster.incident_count);
                        // Approximate SVG coordinates for each cluster centroid
                        const cx =
                          cluster.cluster_id === 101
                            ? 210
                            : cluster.cluster_id === 102
                            ? 220
                            : cluster.cluster_id === 103
                            ? 480
                            : 760;
                        const cy =
                          cluster.cluster_id === 101
                            ? 110
                            : cluster.cluster_id === 102
                            ? 310
                            : cluster.cluster_id === 103
                            ? 180
                            : 220;

                        const isSelected = selectedCluster?.cluster_id === cluster.cluster_id;

                        return (
                          <g
                            key={cluster.cluster_id}
                            className="cursor-pointer group"
                            onClick={() => setSelectedCluster(cluster)}
                            role="button"
                            tabIndex={0}
                            aria-label={`Select Cluster #${cluster.cluster_id} with ${cluster.incident_count} incidents`}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter' || e.key === ' ') {
                                setSelectedCluster(cluster);
                              }
                            }}
                          >
                            {/* Outer Pulsing Halo when Selected */}
                            {isSelected && (
                              <circle
                                cx={cx}
                                cy={cy}
                                r={radius + 8}
                                fill="none"
                                stroke="var(--color-gis-selected-ring)"
                                strokeWidth="2"
                                strokeDasharray="3,3"
                                className="animate-spin"
                                style={{ transformOrigin: `${cx}px ${cy}px` }}
                              />
                            )}

                            {/* Density Fill Ring */}
                            <circle
                              cx={cx}
                              cy={cy}
                              r={radius * 1.5}
                              fill="var(--color-gis-cluster-fill)"
                              fillOpacity={cluster.incident_count > 30 ? '0.22' : '0.12'}
                            />

                            {/* GSAP-Animated Target Circle */}
                            <circle
                              cx={cx}
                              cy={cy}
                              r={radius}
                              data-point-count={cluster.incident_count}
                              data-cluster-id={cluster.cluster_id}
                              className="gsap-cluster-circle transition-transform duration-200 group-hover:scale-105"
                              fill="var(--color-gis-cluster-fill)"
                              fillOpacity="0.8"
                              stroke={isSelected ? 'var(--color-gis-selected-ring)' : 'var(--color-surface)'}
                              strokeWidth={isSelected ? '2.5' : '1.5'}
                            />

                            {/* Center Count Badge */}
                            <text
                              x={cx}
                              y={cy + 4}
                              textAnchor="middle"
                              fill="var(--color-text-inverse)"
                              fontSize={radius > 16 ? '12' : '10'}
                              fontFamily="IBM Plex Mono"
                              fontWeight="bold"
                              pointerEvents="none"
                            >
                              {cluster.incident_count}
                            </text>
                          </g>
                        );
                      })}
                    </g>
                  )}

                  {/* Radial Heat Gradient Definition */}
                  <defs>
                    <radialGradient id="heatGradient">
                      <stop offset="0%" stopColor="var(--status-danger)" stopOpacity="0.5" />
                      <stop offset="60%" stopColor="var(--flag-amber-500)" stopOpacity="0.2" />
                      <stop offset="100%" stopColor="var(--channel-500)" stopOpacity="0" />
                    </radialGradient>
                  </defs>
                </svg>

                {/* Map Navigation Overlay Controls */}
                <div className="absolute bottom-6 left-6 z-20 flex flex-col gap-1 bg-surface border border-border rounded-sm shadow-lifted p-1">
                  <IconButton
                    variant="ghost"
                    size="sm"
                    label="Zoom in"
                    icon={<ZoomIn className="w-4 h-4 text-primary" />}
                    onClick={handleZoomIn}
                  />
                  <div className="w-full h-px bg-border my-0.5" />
                  <IconButton
                    variant="ghost"
                    size="sm"
                    label="Zoom out"
                    icon={<ZoomOut className="w-4 h-4 text-primary" />}
                    onClick={handleZoomOut}
                  />
                </div>

                {/* Floating Stats Panel (Top-Right on Desktop, Bottom Sheet on Mobile) */}
                {selectedCluster && (
                  <div className="absolute top-4 right-4 z-30 sm:block">
                    <ClusterStatsPanel
                      cluster={selectedCluster}
                      onClose={() => setSelectedCluster(null)}
                      onInspectIncidents={handleInspectIncidents}
                    />
                  </div>
                )}
              </div>
            </CoordinateRulerFrame>
          )}
        </main>
      </div>
    </div>
  );
};
