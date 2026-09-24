import React, { useState } from 'react';
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
  Filter,
  RefreshCw,
  Plus,
  ArrowUpDown,
} from 'lucide-react';

const MOCK_CITY_INCIDENTS: BaseQueueItem[] = [
  {
    id: 'inc-9921-bengaluru',
    tracking_token: 'CB-2026-W14-8892',
    title: 'Arterial Road Paver Failure & Waterlogging',
    category: 'Roadway Paver Collapse',
    ward: 'Ward 14 (Indiranagar)',
    department: 'Roads & Infrastructure',
    priority_score: 0.99,
    confidence_score: 0.88,
    status: 'assigned',
    age: '2d ago',
    raw_priority_score: 0.84,
    equity_boost: 0.18,
  },
  {
    id: 'inc-9922-drainage',
    tracking_token: 'CB-2026-W14-8893',
    title: 'Blocked Stormwater Culvert at 100ft Road',
    category: 'Culvert Blockage',
    ward: 'Ward 14 (Indiranagar)',
    department: 'Stormwater Drains',
    priority_score: 0.92,
    confidence_score: 0.74,
    status: 'triaged',
    age: '1d ago',
    raw_priority_score: 0.78,
    equity_boost: 0.18,
  },
  {
    id: 'inc-9923-swm',
    tracking_token: 'CB-2026-W11-4012',
    title: 'Commercial Solid Waste Dump Clearing',
    category: 'Garbage Blackspot',
    ward: 'Ward 11 (Malleshwaram)',
    department: 'Solid Waste Management',
    priority_score: 0.75,
    confidence_score: 0.91,
    status: 'resolved',
    age: '3d ago',
    raw_priority_score: 0.65,
    equity_boost: 0.15,
  },
  {
    id: 'inc-9924-electrical',
    tracking_token: 'CB-2026-W18-5521',
    title: 'Substation Transformer Oil Leakage',
    category: 'Electrical Hazard',
    ward: 'Ward 18 (Shantinagar)',
    department: 'Electrical & Power',
    priority_score: 0.89,
    confidence_score: 0.94,
    status: 'in_progress',
    age: '5h ago',
    raw_priority_score: 0.80,
    equity_boost: 0.11,
  },
  {
    id: 'inc-9925-health',
    tracking_token: 'CB-2026-W09-1099',
    title: 'Mosquito Larval Breeding Stagnant Pool',
    category: 'Public Health Sanitation',
    ward: 'Ward 09 (Rajajinagar)',
    department: 'Public Health',
    priority_score: 0.62,
    confidence_score: 0.68,
    status: 'verified',
    age: '12h ago',
    raw_priority_score: 0.55,
    equity_boost: 0.13,
  },
];

export const IncidentQueueView: React.FC = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDept, setSelectedDept] = useState<string>('all');

  const filteredItems = MOCK_CITY_INCIDENTS.filter((item) => {
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
              City Incident Triage Queue
            </h1>
            <Badge variant="neutral" size="sm">
              Command Deck
            </Badge>
          </div>
          <p className="text-xs text-text-secondary mt-1">
            City-wide incident prioritization and dispatch triage. Click row for quick-glance drawer or open full case.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="primary"
            size="sm"
            onClick={() => navigate('/deck/dispatch/new')}
            leftIcon={<Plus className="w-3.5 h-3.5" />}
          >
            Dispatch Work Order
          </Button>
        </div>
      </div>

      {/* Filter and Search Bar (SCREEN_SPECS.md §2.5) */}
      <div className="px-6 py-3 bg-surface-raised border-b border-border flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3 flex-1 max-w-md">
          <div className="relative w-full">
            <Input
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search incidents, categories, or wards..."
              leftIcon={<Search className="w-4 h-4 text-text-secondary" />}
              size="sm"
            />
          </div>
        </div>

        {/* Department Filter Selector */}
        <div className="flex items-center gap-2">
          <label htmlFor="dept-filter" className="text-xs font-semibold text-text-secondary">
            Filter Dept:
          </label>
          <select
            id="dept-filter"
            value={selectedDept}
            onChange={(e) => setSelectedDept(e.target.value)}
            className="text-xs bg-surface border border-border rounded-sm py-1 px-2.5 font-medium text-primary outline-none focus:ring-1 focus:ring-focus"
          >
            <option value="all">All Municipal Departments</option>
            <option value="Roads & Infrastructure">Roads & Infrastructure</option>
            <option value="Stormwater Drains">Stormwater Drains</option>
            <option value="Solid Waste Management">Solid Waste Management</option>
            <option value="Electrical & Power">Electrical & Power</option>
            <option value="Public Health">Public Health</option>
          </select>
        </div>
      </div>

      {/* Main Queue Content: Shared Table (Ledger rows without clipboard top rule) */}
      <div className="p-6 flex-1">
        <SharedQueueTable
          items={filteredItems}
          showDepartmentColumn={true} // Needed in Command Deck city-wide view
          showSlaDominantColumn={false}
          topBindingMotif={false} // Command Deck uses classic ledger-line aesthetic
          onOpenDetailRoute={(id) => navigate(`/deck/incidents/${id}`)}
          emptyMessage="No incidents found matching active triage filters."
        />
      </div>
    </div>
  );
};
