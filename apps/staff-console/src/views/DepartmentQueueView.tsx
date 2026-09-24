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
  Clock,
  CheckCircle2,
  AlertTriangle,
  FolderKanban,
} from 'lucide-react';

const MOCK_OPS_WORK_ORDERS: BaseQueueItem[] = [
  {
    id: 'wo-101-drain-culvert',
    tracking_token: 'CB-2026-W14-8892',
    title: 'Silt Clearance & Broken Paver Desilting',
    category: 'Culvert Blockage / Waterlogging',
    ward: 'Ward 14 (Indiranagar)',
    priority_score: 0.92,
    confidence_score: 0.84,
    status: 'in_progress',
    age: '4h ago',
    assigned_worker: 'Ramesh Kumar (Gang #4)',
    sla_timer: {
      label: 'SLA Escalation',
      hours_left: 6,
      target_hours: 24,
      status: 'urgent',
    },
    raw_priority_score: 0.78,
    equity_boost: 0.18,
  },
  {
    id: 'wo-102-manhole-cover',
    tracking_token: 'CB-2026-W14-9041',
    title: 'Open Heavy-Duty Ductile Iron Manhole Lid Replacement',
    category: 'Missing Manhole Cover',
    ward: 'Ward 14 (Indiranagar)',
    priority_score: 0.98,
    confidence_score: 0.95,
    status: 'assigned',
    age: '1h ago',
    assigned_worker: 'Suresh Patel (Crew #2)',
    sla_timer: {
      label: 'Urgent Hazard',
      hours_left: 3,
      target_hours: 6,
      status: 'urgent',
    },
    raw_priority_score: 0.85,
    equity_boost: 0.15,
  },
  {
    id: 'wo-103-storm-drain-inlet',
    tracking_token: 'CB-2026-W15-1102',
    title: 'Clearing Plastic Debris from Grate Inlet',
    category: 'Stormwater Grate Obstruction',
    ward: 'Ward 15 (Domlur)',
    priority_score: 0.68,
    confidence_score: 0.72,
    status: 'dispatched',
    age: '18h ago',
    assigned_worker: 'Anand Singh (Team #1)',
    sla_timer: {
      label: 'Standard SLA',
      hours_left: 22,
      target_hours: 48,
      status: 'normal',
    },
    raw_priority_score: 0.60,
    equity_boost: 0.12,
  },
  {
    id: 'wo-104-curb-side-silt',
    tracking_token: 'CB-2026-W12-7729',
    title: 'Post-Monsoon Roadside Sediment Removal',
    category: 'Channel Desilting',
    ward: 'Ward 12 (Ulsoor)',
    priority_score: 0.45,
    confidence_score: 0.65,
    status: 'accepted',
    age: '1d ago',
    assigned_worker: 'Unassigned',
    sla_timer: {
      label: 'Extended Window',
      hours_left: 38,
      target_hours: 72,
      status: 'normal',
    },
    raw_priority_score: 0.40,
    equity_boost: 0.10,
  },
  {
    id: 'wo-105-culvert-restoration',
    tracking_token: 'CB-2026-W14-6632',
    title: 'Reinforced Concrete Culvert Slab Replacement',
    category: 'Structural Culvert Collapse',
    ward: 'Ward 14 (Indiranagar)',
    priority_score: 0.88,
    confidence_score: 0.90,
    status: 'completed',
    age: '2d ago',
    assigned_worker: 'Ramesh Kumar (Gang #4)',
    sla_timer: {
      label: 'Met SLA',
      hours_left: 0,
      target_hours: 48,
      status: 'normal',
    },
    raw_priority_score: 0.75,
    equity_boost: 0.18,
  },
];

export const DepartmentQueueView: React.FC = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilter, setActiveFilter] = useState<'all' | 'urgent' | 'active' | 'completed'>('all');

  const filteredItems = MOCK_OPS_WORK_ORDERS.filter((item) => {
    const matchesSearch =
      item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.ward.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.tracking_token && item.tracking_token.toLowerCase().includes(searchTerm.toLowerCase()));

    if (!matchesSearch) return false;

    if (activeFilter === 'urgent') return item.sla_timer?.status === 'urgent';
    if (activeFilter === 'active') return item.status === 'in_progress' || item.status === 'assigned' || item.status === 'dispatched';
    if (activeFilter === 'completed') return item.status === 'completed';
    return true;
  });

  return (
    <div
      data-workspace="ops-board"
      className="flex flex-col min-h-screen bg-background text-primary font-ui transition-colors duration-fast"
    >
      {/* Top Header & Department Context Bar */}
      <div className="p-6 pb-4 border-b border-border flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <h1 className="text-xl font-bold tracking-tight text-primary">
              Department Operations Queue
            </h1>
            <Badge variant="neutral" size="sm">
              Stormwater & Drainage
            </Badge>
          </div>
          <p className="text-xs text-text-secondary mt-1">
            RLS-scoped to Department of Stormwater Drains. SLA timer is the dominant operational weight.
          </p>
        </div>

        {/* Quick Shift Summary Stats */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-sm bg-surface border border-border text-xs">
            <Clock className="w-3.5 h-3.5 text-status-danger" />
            <span>2 Critical SLA Breaches Imminent</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-sm bg-surface border border-border text-xs">
            <CheckCircle2 className="w-3.5 h-3.5 text-status-success" />
            <span>12 Resolved This Shift</span>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar (SCREEN_SPECS.md §2.5 / §2.10) */}
      <div className="px-6 py-3 bg-surface-raised border-b border-border flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3 flex-1 max-w-md">
          <div className="relative w-full">
            <Input
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search work orders, wards, or tokens..."
              leftIcon={<Search className="w-4 h-4 text-text-secondary" />}
              size="sm"
            />
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-2">
          {(['all', 'urgent', 'active', 'completed'] as const).map((filter) => (
            <button
              key={filter}
              type="button"
              onClick={() => setActiveFilter(filter)}
              className={`
                px-2.5 py-1 rounded-sm text-xs font-medium cursor-pointer transition-colors outline-none
                focus-visible:ring-1 focus-visible:ring-focus
                ${
                  activeFilter === filter
                    ? 'bg-action-primary text-text-inverse font-semibold'
                    : 'bg-surface hover:bg-surface-raised border border-border text-text-secondary hover:text-primary'
                }
              `}
            >
              {filter === 'all'
                ? 'All Orders'
                : filter === 'urgent'
                ? 'SLA Urgent'
                : filter === 'active'
                ? 'In-Flight'
                : 'Completed'}
            </button>
          ))}
        </div>
      </div>

      {/* Main Queue Content: Shared Table with Clipboard Motif & SLA-Dominant Column */}
      <div className="p-6 flex-1">
        <SharedQueueTable
          items={filteredItems}
          showDepartmentColumn={false} // Redundant in Ops Board per §2.10
          showSlaDominantColumn={true} // Dominant visual weight per §2.10
          topBindingMotif={true} // Clipboard motif per §2.10
          onOpenDetailRoute={(id) => navigate(`/ops/work-orders/${id}`)}
          emptyMessage="No departmental work orders found matching active query."
        />
      </div>
    </div>
  );
};
