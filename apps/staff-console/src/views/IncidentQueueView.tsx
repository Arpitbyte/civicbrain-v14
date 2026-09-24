import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  SharedQueueTable,
  BaseQueueItem,
  Button,
  Badge,
  Input,
} from '@civicbrain/ui';
import {
  Search,
  RefreshCw,
  Plus,
  Building2,
  AlertCircle,
  Inbox,
} from 'lucide-react';

interface Organization {
  id: string;
  name: string;
  code: string;
}

interface Department {
  id: string;
  name: string;
  code: string;
}

interface Ward {
  id: string;
  ward_number: number;
  name: string;
}

interface LiveIncident {
  id: string;
  organization_id: string;
  department_id: string;
  ward_id: string;
  category_code: string;
  status: string;
  severity: number;
  assigned_worker_id: string | null;
  created_at: string;
  updated_at: string;
}

const CATEGORY_NAMES_HI: Record<string, { en: string; hi: string }> = {
  ROAD_POTHOLE_ARTERIAL: { en: 'Arterial Road Pothole', hi: 'मुख्य मार्ग का गड्ढा' },
  DRAIN_CULVERT_BLOCKAGE: { en: 'Blocked Stormwater Culvert', hi: 'अवरुद्ध बरसाती नाला' },
  SOLID_WASTE_DUMP: { en: 'Solid Waste Blackspot', hi: 'कचरा ढेर / डंपिंग' },
  STREETLIGHT_OUTAGE: { en: 'Streetlight Failure', hi: 'स्ट्रीट लाइट खराबी' },
  WATER_PIPE_BURST: { en: 'Water Supply Pipe Burst', hi: 'पेयजल पाइपलाइन रिसाव' },
  ELECTRICAL_HAZARD: { en: 'Exposed Electrical Cable', hi: 'खुला बिजली तार' },
};

function formatCategory(code: string): string {
  const match = CATEGORY_NAMES_HI[code];
  if (match) return `${match.en} (${match.hi})`;
  return code
    .split('_')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
    .join(' ');
}

function timeAgo(dateString: string): string {
  const diffMs = Date.now() - new Date(dateString).getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return 'Just now';
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffHours = Math.floor(diffMin / 60);
  if (diffHours < 24) return `${diffHours}h ago`;
  const diffDays = Math.floor(diffHours / 24);
  return `${diffDays}d ago`;
}

export const IncidentQueueView: React.FC = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDept, setSelectedDept] = useState<string>('all');
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [selectedOrgId, setSelectedOrgId] = useState<string>('');
  const [departments, setDepartments] = useState<Department[]>([]);
  const [wardsMap, setWardsMap] = useState<Record<string, string>>({});
  const [incidents, setIncidents] = useState<BaseQueueItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Load organizations
  useEffect(() => {
    async function loadOrgs() {
      try {
        const res = await fetch('/v1/orgs');
        if (res.ok) {
          const orgs: Organization[] = await res.json();
          setOrganizations(orgs);
          if (orgs.length > 0) {
            setSelectedOrgId(orgs[0].id);
          }
        }
      } catch (err) {
        console.warn('Could not load organizations:', err);
      }
    }
    loadOrgs();
  }, []);

  // Load departments, wards, and incidents for the selected organization
  const fetchIncidents = useCallback(async (orgId: string) => {
    if (!orgId) return;
    setIsLoading(true);
    setError(null);
    try {
      // 1. Fetch departments
      const deptsRes = await fetch(`/v1/orgs/${orgId}/departments`);
      const depts: Department[] = deptsRes.ok ? await deptsRes.json() : [];
      setDepartments(depts);
      const deptMap: Record<string, string> = {};
      depts.forEach(d => {
        deptMap[d.id] = d.name;
      });

      // 2. Fetch wards
      const wardsRes = await fetch(`/v1/orgs/${orgId}/wards`);
      const wards: Ward[] = wardsRes.ok ? await wardsRes.json() : [];
      const wMap: Record<string, string> = {};
      wards.forEach(w => {
        wMap[w.id] = `वार्ड ${w.ward_number} (${w.name})`;
      });
      setWardsMap(wMap);

      // 3. Fetch real incidents (ZERO synthetic data)
      const incRes = await fetch(`/v1/incidents?organization_id=${orgId}&page_size=100`);
      if (!incRes.ok) {
        throw new Error(`Failed to load incidents: ${incRes.statusText}`);
      }
      const rawIncidents: LiveIncident[] = await incRes.json();

      const queueItems: BaseQueueItem[] = rawIncidents.map(inc => ({
        id: inc.id,
        tracking_token: `CB-${inc.id.slice(0, 8).toUpperCase()}`,
        title: formatCategory(inc.category_code),
        category: inc.category_code,
        ward: wMap[inc.ward_id] || `Ward #${inc.ward_id.slice(0, 6)}`,
        department: deptMap[inc.department_id] || 'General Municipal Services',
        priority_score: inc.severity ? Math.min(1.0, inc.severity / 5.0) : 0.5,
        confidence_score: 0.9,
        status: (inc.status as any) || 'triaged',
        age: timeAgo(inc.created_at),
        raw_priority_score: inc.severity ? inc.severity / 5.0 : 0.5,
        equity_boost: 0.0,
      }));

      setIncidents(queueItems);
    } catch (err: any) {
      console.error('Incident fetch error:', err);
      setError(err.message || 'Error fetching incidents from backend');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (selectedOrgId) {
      fetchIncidents(selectedOrgId);
    }
  }, [selectedOrgId, fetchIncidents]);

  const filteredItems = incidents.filter(item => {
    const matchesSearch =
      item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.ward.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.tracking_token && item.tracking_token.toLowerCase().includes(searchTerm.toLowerCase()));

    if (!matchesSearch) return false;
    if (selectedDept !== 'all' && item.department !== selectedDept) return false;
    return true;
  });

  return (
    <div
      data-workspace="command-deck"
      className="flex flex-col min-h-screen bg-background text-primary font-ui transition-colors duration-fast"
    >
      {/* Top Header Bar */}
      <div className="p-6 pb-4 border-b border-border flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <h1 className="text-xl font-bold tracking-tight text-primary">
              नगर शिकायत एवं निवारण कतार / City Incident Queue
            </h1>
            <Badge variant="neutral" size="sm">
              कमांड डेस्क
            </Badge>
          </div>
          <p className="text-xs text-text-secondary mt-1">
            वार्ड स्तर पर नागरिक शिकायतों का वास्तविक समय सत्यापन, प्राथमिकता और कार्य आदेश प्रेषण। (Real-time live municipal queue with zero synthetic data).
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* Organization Switcher */}
          {organizations.length > 0 && (
            <div className="flex items-center gap-1.5 bg-surface-raised border border-border px-2.5 py-1 rounded text-xs">
              <Building2 className="w-3.5 h-3.5 text-text-secondary" />
              <select
                value={selectedOrgId}
                onChange={e => setSelectedOrgId(e.target.value)}
                className="bg-transparent font-medium text-primary outline-none cursor-pointer"
                aria-label="Select Municipal Corporation"
              >
                {organizations.map(org => (
                  <option key={org.id} value={org.id} className="bg-surface text-primary">
                    {org.name} ({org.code})
                  </option>
                ))}
              </select>
            </div>
          )}

          <Button
            variant="ghost"
            size="sm"
            onClick={() => selectedOrgId && fetchIncidents(selectedOrgId)}
            leftIcon={<RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />}
            disabled={isLoading}
          >
            ताज़ा करें / Refresh
          </Button>

          <Button
            variant="primary"
            size="sm"
            onClick={() => navigate('/deck/dispatch/new')}
            leftIcon={<Plus className="w-3.5 h-3.5" />}
          >
            नया कार्य आदेश / Dispatch Work Order
          </Button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="px-6 py-3 bg-surface-raised border-b border-border flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3 flex-1 max-w-md">
          <div className="relative w-full">
            <Input
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              placeholder="खोजें: शिकायत, श्रेणी, या वार्ड (Search incident, ward, token)..."
              leftIcon={<Search className="w-4 h-4 text-text-secondary" />}
              size="sm"
            />
          </div>
        </div>

        {/* Department Filter Selector */}
        <div className="flex items-center gap-2">
          <label htmlFor="dept-filter" className="text-xs font-semibold text-text-secondary">
            विभाग / Department:
          </label>
          <select
            id="dept-filter"
            value={selectedDept}
            onChange={e => setSelectedDept(e.target.value)}
            className="text-xs bg-surface border border-border rounded py-1 px-2.5 font-medium text-primary outline-none focus:ring-1 focus:ring-focus"
          >
            <option value="all">सभी विभाग / All Municipal Departments</option>
            {departments.map(d => (
              <option key={d.id} value={d.name}>
                {d.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Queue Content */}
      <div className="p-6 flex-1 flex flex-col">
        {error ? (
          <div className="p-4 bg-red-500/10 border border-red-500/30 rounded text-red-700 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        ) : isLoading ? (
          <div className="flex-1 flex flex-col items-center justify-center py-16 text-text-secondary">
            <RefreshCw className="w-6 h-6 animate-spin mb-3 text-primary" />
            <p className="text-sm font-medium">डेटाबेस से वास्तविक शिकायतें लोड हो रही हैं...</p>
            <p className="text-xs text-text-secondary mt-1">Fetching live municipal records from PostgreSQL</p>
          </div>
        ) : incidents.length === 0 ? (
          /* Authentic zero synthetic data empty state */
          <div className="flex-1 flex flex-col items-center justify-center py-20 px-4 text-center bg-surface-raised/30 rounded-lg border border-border border-dashed my-4">
            <div className="w-12 h-12 rounded-full bg-surface-raised flex items-center justify-center mb-3 text-text-secondary">
              <Inbox className="w-6 h-6" />
            </div>
            <h3 className="text-base font-semibold text-primary">
              कोई सक्रिय शिकायत दर्ज नहीं है / No Active Incidents Recorded
            </h3>
            <p className="text-xs text-text-secondary max-w-md mt-1.5 leading-relaxed">
              इस नगर निगम क्षेत्र में कोई लंबित शिकायत नहीं है। सिविकब्रेन की शून्य कृत्रिम डेटा (0 Synthetic Data) नीति के अनुसार केवल वास्तविक नागरिकों या फील्ड कार्यकर्ताओं द्वारा दर्ज की गई शिकायतें ही यहाँ प्रदर्शित होती हैं।
            </p>
            <div className="mt-5 flex items-center gap-3">
              <Button
                variant="outline"
                size="sm"
                onClick={() => selectedOrgId && fetchIncidents(selectedOrgId)}
                leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
              >
                जाँचें / Recheck Live DB
              </Button>
            </div>
          </div>
        ) : (
          <SharedQueueTable
            items={filteredItems}
            showDepartmentColumn={true}
            showSlaDominantColumn={false}
            topBindingMotif={false}
            onOpenDetailRoute={id => navigate(`/deck/incidents/${id}`)}
            emptyMessage="सक्रिय फ़िल्टर से मेल खाती कोई शिकायत नहीं मिली। (No incidents matching active filters)."
          />
        )}
      </div>
    </div>
  );
};
