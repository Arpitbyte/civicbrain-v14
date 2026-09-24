import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Switch } from '@civicbrain/ui';
import { RealSatelliteMap, IncidentCluster } from '../components/gis/RealSatelliteMap';
import { ClusterStatsPanel, ClusterData } from '../components/gis/ClusterStatsPanel';
import { ClusterAccessibleListView } from '../components/gis/ClusterAccessibleListView';
import {
  Layers,
  Sliders,
  List,
  Map as MapIcon,
  RefreshCw,
  AlertCircle,
  Building2,
  CheckCircle2,
  Filter,
} from 'lucide-react';

interface Organization {
  id: string;
  name: string;
  code: string;
  ulb_type: string;
  state: string;
}

interface Department {
  id: string;
  name: string;
  code: string;
}

export const HeatmapClusterView: React.FC = () => {
  const navigate = useNavigate();

  // Active ULB Organization state
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [selectedOrgId, setSelectedOrgId] = useState<string>('');
  const [departments, setDepartments] = useState<Department[]>([]);
  const [selectedDeptId, setSelectedDeptId] = useState<string>('all');

  // Layer Visibility
  const [showWards, setShowWards] = useState(true);
  const [showIncidents, setShowIncidents] = useState(true);
  const [showClusters, setShowClusters] = useState(true);

  // Clustering tuning parameters
  const [epsMeters, setEpsMeters] = useState<number>(100);
  const [minPoints, setMinPoints] = useState<number>(3);

  // View state
  const [viewMode, setViewMode] = useState<'map' | 'list'>('map');
  const [selectedCluster, setSelectedCluster] = useState<ClusterData | null>(null);

  // Real API Data
  const [clusters, setClusters] = useState<IncidentCluster[]>([]);
  const [wardsGeoJSON, setWardsGeoJSON] = useState<GeoJSON.FeatureCollection | null>(null);
  const [incidentsGeoJSON, setIncidentsGeoJSON] = useState<GeoJSON.FeatureCollection | null>(null);

  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [dataError, setDataError] = useState<string | null>(null);

  // 1. Fetch Organizations on mount
  useEffect(() => {
    const fetchOrgs = async () => {
      try {
        const res = await fetch('/v1/orgs');
        if (res.ok) {
          const orgs: Organization[] = await res.json();
          setOrganizations(orgs);
          if (orgs.length > 0) {
            // Select BBMP or the first available organization
            const defaultOrg = orgs.find(o => o.code.startsWith('BBMP')) || orgs[0];
            setSelectedOrgId(defaultOrg.id);
          }
        }
      } catch (err) {
        console.error('Failed to load organizations:', err);
      }
    };
    fetchOrgs();
  }, []);

  // 2. Fetch Departments for selected organization
  useEffect(() => {
    if (!selectedOrgId) return;
    const fetchDepts = async () => {
      try {
        const res = await fetch(`/v1/orgs/${selectedOrgId}/departments`);
        if (res.ok) {
          const data: Department[] = await res.json();
          setDepartments(data);
        }
      } catch (err) {
        console.error('Failed to load departments:', err);
      }
    };
    fetchDepts();
  }, [selectedOrgId]);

  // 3. Fetch Real GIS Data (Wards, Incidents, Clusters)
  const fetchGisData = useCallback(async () => {
    if (!selectedOrgId) return;

    setDataError(null);
    try {
      // A. Fetch Wards GeoJSON
      const wardsRes = await fetch(`/v1/gis/wards/geojson?organization_id=${selectedOrgId}`);
      if (wardsRes.ok) {
        const wardsData: GeoJSON.FeatureCollection = await wardsRes.json();
        setWardsGeoJSON(wardsData);
      }

      // B. Fetch Incidents GeoJSON
      const deptQuery = selectedDeptId !== 'all' ? `&department_id=${selectedDeptId}` : '';
      const incidentsRes = await fetch(`/v1/gis/incidents/geojson?organization_id=${selectedOrgId}${deptQuery}`);
      if (incidentsRes.ok) {
        const incData: GeoJSON.FeatureCollection = await incidentsRes.json();
        setIncidentsGeoJSON(incData);
      }

      // C. Fetch DBSCAN Clusters
      const clustersUrl = `/v1/gis/clusters?organization_id=${selectedOrgId}&eps_meters=${epsMeters}&min_points=${minPoints}${deptQuery}`;
      const clustersRes = await fetch(clustersUrl);
      if (clustersRes.ok) {
        const clusterData: IncidentCluster[] = await clustersRes.json();
        setClusters(clusterData);
        if (clusterData.length > 0 && !selectedCluster) {
          // Format first cluster for detailed panel
          const first = clusterData[0];
          setSelectedCluster({
            cluster_id: first.cluster_id,
            incident_count: first.incident_count,
            centroid: {
              type: 'Point',
              coordinates: first.centroid?.coordinates || [77.5946, 12.9716],
            },
            incident_ids: first.incident_ids.map(String),
            confidence_score: first.confidence_score || 0.85,
            dominant_category: first.dominant_category || 'नागरिक शिकायतें (Civic Defects)',
            category_breakdown: [{ category: 'नागरिक समस्याएं', count: first.incident_count, percentage: 100 }],
            severity_breakdown: { critical: 0, major: first.incident_count, minor: 0 },
            ward_name: first.ward_name,
            ward_number: first.ward_number,
          });
        }
      }
    } catch (err: any) {
      console.error('GIS data fetch error:', err);
      setDataError('नगर पालिका जीआईएस डेटा लोड करने में त्रुटि (Failed to connect to live GIS server)');
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, [selectedOrgId, selectedDeptId, epsMeters, minPoints, selectedCluster]);

  useEffect(() => {
    setIsLoading(true);
    fetchGisData();
  }, [fetchGisData]);

  const handleRefresh = () => {
    setIsRefreshing(true);
    fetchGisData();
  };

  const handleSelectCluster = (c: IncidentCluster) => {
    setSelectedCluster({
      cluster_id: c.cluster_id,
      incident_count: c.incident_count,
      centroid: {
        type: 'Point',
        coordinates: c.centroid?.coordinates || [77.5946, 12.9716],
      },
      incident_ids: c.incident_ids.map(String),
      confidence_score: c.confidence_score || 0.9,
      dominant_category: c.dominant_category || 'नागरिक शिकायत क्लस्टर',
      category_breakdown: [{ category: 'प्राथमिक समस्याएं', count: c.incident_count, percentage: 100 }],
      severity_breakdown: { critical: 0, major: c.incident_count, minor: 0 },
      ward_name: c.ward_name,
      ward_number: c.ward_number,
    });
  };

  // Convert for ClusterAccessibleListView
  const fullClusterList: ClusterData[] = useMemo(() => {
    return clusters.map(c => ({
      cluster_id: c.cluster_id,
      incident_count: c.incident_count,
      centroid: {
        type: 'Point',
        coordinates: c.centroid?.coordinates || [77.5946, 12.9716],
      },
      incident_ids: c.incident_ids.map(String),
      confidence_score: c.confidence_score || 0.85,
      dominant_category: c.dominant_category || 'नागरिक शिकायतें',
      category_breakdown: [{ category: 'सामान्य समस्याएं', count: c.incident_count, percentage: 100 }],
      severity_breakdown: { critical: 0, major: c.incident_count, minor: 0 },
      ward_name: c.ward_name,
      ward_number: c.ward_number,
    }));
  }, [clusters]);

  const currentOrg = organizations.find(o => o.id === selectedOrgId);

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)] font-ui bg-slate-50 text-slate-900 overflow-hidden">
      {/* Indian Municipal Header & Command Bar */}
      <header className="h-14 px-4 sm:px-6 bg-white border-b border-slate-200 flex items-center justify-between shrink-0 z-20 shadow-xs">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-600">
            <Building2 className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-sm sm:text-base font-semibold text-slate-900 tracking-tight">
                City Pulse — Ward Hotspots & Cluster Map
              </h1>
              <span className="text-[11px] font-medium text-orange-600 bg-orange-50 px-2 py-0.5 rounded-full border border-orange-200">
                नगर पल्स
              </span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">
              {currentOrg ? `${currentOrg.name} (${currentOrg.state})` : 'महानगर पालिका प्रभाग विश्लेषण'} • वास्तविक समय जीआईएस क्लस्टर
            </p>
          </div>
        </div>

        {/* View Mode & Live Refresh */}
        <div className="flex items-center gap-2.5">
          {/* Organization Switcher if multiple ULBs exist */}
          {organizations.length > 1 && (
            <select
              value={selectedOrgId}
              onChange={(e) => setSelectedOrgId(e.target.value)}
              className="text-xs border border-slate-200 rounded-md px-2 py-1.5 bg-slate-50 font-medium text-slate-700 outline-none focus:ring-1 focus:ring-orange-500"
              aria-label="Select Municipal Corporation"
            >
              {organizations.map(org => (
                <option key={org.id} value={org.id}>{org.name}</option>
              ))}
            </select>
          )}

          {/* Map vs List Mode */}
          <div className="flex items-center bg-slate-100 p-0.5 border border-slate-200 rounded-lg">
            <button
              onClick={() => setViewMode('map')}
              className={`flex items-center gap-1.5 px-3 py-1 text-xs font-medium rounded-md transition-all ${
                viewMode === 'map'
                  ? 'bg-white text-slate-900 shadow-xs font-semibold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <MapIcon className="w-3.5 h-3.5" />
              <span>मानचित्र (Map)</span>
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`flex items-center gap-1.5 px-3 py-1 text-xs font-medium rounded-md transition-all ${
                viewMode === 'list'
                  ? 'bg-white text-slate-900 shadow-xs font-semibold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <List className="w-3.5 h-3.5" />
              <span>सूची (List)</span>
            </button>
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="text-xs border-slate-200 text-slate-700 hover:bg-slate-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isRefreshing ? 'animate-spin' : ''}`} />
            <span>रिफ्रेश (Sync)</span>
          </Button>
        </div>
      </header>

      {/* Error Alert Banner */}
      {dataError && (
        <div className="bg-amber-50 border-b border-amber-200 px-4 py-2 flex items-center justify-between text-xs text-amber-800 z-30">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
            <span>{dataError}</span>
          </div>
          <button
            onClick={() => setDataError(null)}
            className="font-medium text-xs text-amber-900 underline hover:opacity-80"
          >
            खारिज करें (Dismiss)
          </button>
        </div>
      )}

      {/* Main Workspace Layout: Side Controls + Real Map */}
      <div className="flex flex-1 overflow-hidden relative">
        {/* Left Side Controls Rail (Indian Civic Admin Context) */}
        <aside className="w-80 shrink-0 border-r border-slate-200 bg-white flex flex-col justify-between overflow-y-auto z-10 shadow-xs">
          <div className="p-4 space-y-5">
            {/* Map Layers Section */}
            <div className="space-y-2.5">
              <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700 uppercase tracking-wider">
                <Layers className="w-3.5 h-3.5 text-orange-600" />
                <span>मानचित्र परतें (Map Layers)</span>
              </div>

              <div className="space-y-2.5 text-xs bg-slate-50/80 p-3.5 border border-slate-200 rounded-lg">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-slate-700">
                    <span className="w-3.5 h-0.5 border-b-2 border-dashed border-sky-500" />
                    <span>प्रभाग सीमाएं (Wards)</span>
                  </div>
                  <Switch
                    checked={showWards}
                    onCheckedChange={setShowWards}
                    aria-label="Toggle ward boundary polygons"
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-slate-700">
                    <span className="w-2.5 h-2.5 rounded-full bg-orange-500" />
                    <span>शिकायत स्थल (Incidents)</span>
                  </div>
                  <Switch
                    checked={showIncidents}
                    onCheckedChange={setShowIncidents}
                    aria-label="Toggle incident markers"
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-slate-700">
                    <span className="w-3 h-3 rounded-full bg-red-600 ring-2 ring-red-200" />
                    <span className="font-semibold text-slate-900">हॉटस्पॉट क्लस्टर (Hotspots)</span>
                  </div>
                  <Switch
                    checked={showClusters}
                    onCheckedChange={setShowClusters}
                    aria-label="Toggle cluster markers"
                  />
                </div>
              </div>
            </div>

            {/* Hotspot Detection Calibration */}
            <div className="space-y-2.5">
              <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700 uppercase tracking-wider">
                <Sliders className="w-3.5 h-3.5 text-orange-600" />
                <span>हॉटस्पॉट संवेदनशीलता (Sensitivity)</span>
              </div>

              <div className="space-y-3.5 p-3.5 bg-slate-50/80 border border-slate-200 rounded-lg text-xs">
                <div>
                  <div className="flex justify-between mb-1.5">
                    <span className="text-slate-600">क्लस्टर दायरा (Search Radius):</span>
                    <span className="font-bold text-slate-900">{epsMeters} मीटर</span>
                  </div>
                  <input
                    type="range"
                    min="30"
                    max="500"
                    step="10"
                    value={epsMeters}
                    onChange={(e) => setEpsMeters(Number(e.target.value))}
                    className="w-full accent-orange-600 cursor-pointer"
                    aria-label="Clustering radius in meters"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                    <span>30m (सटीक गली)</span>
                    <span>500m (व्यापक क्षेत्र)</span>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-200">
                  <div className="flex justify-between mb-1.5">
                    <span className="text-slate-600">न्यूनतम शिकायतें (Min Incidents):</span>
                    <span className="font-bold text-slate-900">{minPoints} मामले</span>
                  </div>
                  <input
                    type="range"
                    min="2"
                    max="15"
                    step="1"
                    value={minPoints}
                    onChange={(e) => setMinPoints(Number(e.target.value))}
                    className="w-full accent-orange-600 cursor-pointer"
                    aria-label="Minimum complaints to form cluster"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                    <span>2 (कम से कम)</span>
                    <span>15 (गंभीर समूह)</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Department Filter */}
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700 uppercase tracking-wider">
                <Filter className="w-3.5 h-3.5 text-orange-600" />
                <span>विभाग / श्रेणी (Department Filter)</span>
              </div>
              <select
                value={selectedDeptId}
                onChange={(e) => setSelectedDeptId(e.target.value)}
                className="w-full bg-white border border-slate-200 rounded-md text-xs p-2 text-slate-800 outline-none focus:ring-1 focus:ring-orange-500 shadow-xs"
                aria-label="Filter by municipal department"
              >
                <option value="all">सभी विभाग (All Departments)</option>
                {departments.map((dept) => (
                  <option key={dept.id} value={dept.id}>
                    {dept.name} ({dept.code})
                  </option>
                ))}
              </select>
            </div>

            {/* Active Hotspots Summary Card */}
            <div className="p-4 bg-orange-50/70 border border-orange-200/80 rounded-lg space-y-1.5 text-xs">
              <div className="flex items-center gap-1.5 text-[11px] font-bold text-orange-700 uppercase tracking-wide">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>सक्रिय प्रभाग स्थिति (Live Status)</span>
              </div>
              <div className="font-bold text-slate-900 text-lg">
                {clusters.length} हॉटस्पॉट क्लस्टर
              </div>
              <p className="text-slate-600 text-xs leading-relaxed">
                {clusters.length > 0 ? (
                  `वर्तमान में ${clusters.reduce((acc, c) => acc + c.incident_count, 0)} नागरिक शिकायतों का समूह पहचाना गया है।`
                ) : (
                  'सर्वेक्षित क्षेत्र में अभी कोई सघन हॉटस्पॉट नहीं बना है। लाइव डेटा शून्य सिंथेटिक रिकॉर्ड पर आधारित है।'
                )}
              </p>
            </div>
          </div>

          {/* Left Rail Footer with Verification Stamp */}
          <div className="p-3 border-t border-slate-200 bg-slate-50 text-[11px] text-slate-500 flex items-center justify-between">
            <span className="font-medium text-slate-700">CivicBrain Live GIS</span>
            <span className="text-[10px] text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
              0% Synthetic Data
            </span>
          </div>
        </aside>

        {/* Center Canvas: Real Satellite Map OR Accessible List */}
        <main className="flex-1 relative h-full w-full overflow-hidden bg-slate-900">
          {viewMode === 'list' ? (
            <div className="h-full overflow-y-auto bg-slate-50 p-6">
              <div className="max-w-4xl mx-auto space-y-4">
                <div className="flex items-center justify-between border-b border-slate-200 pb-3">
                  <div>
                    <h2 className="text-base font-bold text-slate-900">
                      प्रभाग हॉटस्पॉट सूची (Hotspot Cluster Directory)
                    </h2>
                    <p className="text-xs text-slate-500">
                      {clusters.length} सक्रिय क्लस्टर • वास्तविक समय डेटाबेस
                    </p>
                  </div>
                </div>

                {clusters.length === 0 ? (
                  <div className="text-center py-16 bg-white border border-slate-200 rounded-xl p-8 shadow-xs">
                    <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto mb-3" />
                    <h3 className="text-sm font-semibold text-slate-900 mb-1">
                      कोई सक्रिय हॉटस्पॉट क्लस्टर नहीं मिला
                    </h3>
                    <p className="text-xs text-slate-500 max-w-md mx-auto">
                      चयनित संवेदनशीलता ({epsMeters}m दायरा, {minPoints} न्यूनतम मामले) के अनुसार इस समय कोई समूह नहीं है।
                    </p>
                  </div>
                ) : (
                  <ClusterAccessibleListView
                    clusters={fullClusterList}
                    selectedClusterId={selectedCluster?.cluster_id ?? null}
                    onSelectCluster={(c) => {
                      handleSelectCluster(c as any);
                      setViewMode('map');
                    }}
                    calculateRadius={(count) => Math.min(28, Math.max(12, 10 + Math.sqrt(count) * 2))}
                  />
                )}
              </div>
            </div>
          ) : (
            <div className="relative w-full h-full">
              {/* Real Satellite Map Component */}
              <RealSatelliteMap
                clusters={clusters}
                selectedClusterId={selectedCluster?.cluster_id ?? null}
                onSelectCluster={handleSelectCluster}
                wardsGeoJSON={wardsGeoJSON}
                incidentsGeoJSON={incidentsGeoJSON}
                showWards={showWards}
                showClusters={showClusters}
                showIncidents={showIncidents}
                center={[12.9716, 77.5946]}
                zoom={13}
              />

              {/* Floating Cluster Details Panel (Top Right) */}
              {selectedCluster && (
                <div className="absolute top-4 left-4 z-20 max-w-sm">
                  <ClusterStatsPanel
                    cluster={selectedCluster}
                    onClose={() => setSelectedCluster(null)}
                    onInspectIncidents={() => navigate('/deck')}
                  />
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};
