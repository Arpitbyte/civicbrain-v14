import React, { useState } from 'react';
import {
  PriorityChip,
  ConfidenceBadge,
  Badge,
  ScoreBreakdown,
  Drawer,
  Button,
} from '@civicbrain/ui';
import {
  ChevronRight,
  ExternalLink,
  Layers,
  ArrowUpDown,
  Search,
  Clock,
  UserCheck,
} from 'lucide-react';

export interface BaseQueueItem {
  id: string;
  tracking_token?: string;
  title: string;
  category: string;
  ward: string;
  department?: string; // Optional if scoped by workspace
  priority_score: number;
  confidence_score?: number | null;
  status: string;
  age: string;
  sla_timer?: {
    label: string;
    hours_left: number;
    target_hours: number;
    status: 'urgent' | 'warning' | 'normal' | 'breached';
  };
  assigned_worker?: string;
  raw_priority_score?: number;
  equity_boost?: number;
  subscores?: any;
  weights_used?: any;
}

export interface SharedQueueTableProps {
  items: BaseQueueItem[];
  showDepartmentColumn?: boolean;
  showSlaDominantColumn?: boolean;
  onOpenDetailRoute?: (id: string) => void;
  topBindingMotif?: boolean; // Clipboard motif for Ops Board
  emptyMessage?: string;
  isLoading?: boolean;
}

/**
 * SharedQueueTable
 * Implements the canonical table grammar from SCREEN_SPECS.md §2.5 & §2.10:
 * - High-density sticky table header
 * - Columns: Priority (PriorityChip), Category, Ward, [Department], Status (Badge), SLA Timer, Age
 * - Row click opens quick-glance inline drawer OR opens full case route on dedicated icon
 * - Keyboard row navigation support
 * - Motion: Quiet tier (instant state changes)
 * - Top-binding rule motif: subtle clipboard header bar on Ops Board
 */
export const SharedQueueTable: React.FC<SharedQueueTableProps> = ({
  items,
  showDepartmentColumn = true,
  showSlaDominantColumn = false,
  onOpenDetailRoute,
  topBindingMotif = false,
  emptyMessage = 'No items found matching active filters.',
  isLoading = false,
}) => {
  const [selectedItem, setSelectedItem] = useState<BaseQueueItem | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [sortAsc, setSortAsc] = useState(false);

  const sortedItems = [...items].sort((a, b) =>
    sortAsc ? a.priority_score - b.priority_score : b.priority_score - a.priority_score
  );

  const handleRowClick = (item: BaseQueueItem) => {
    setSelectedItem(item);
    setDrawerOpen(true);
  };

  return (
    <div
      className={`
        w-full bg-surface rounded-md border border-border overflow-hidden font-ui shadow-flat
        ${topBindingMotif ? 'border-t-4 border-t-station-600' : ''}
      `}
    >
      {/* Top binding clipboard clip motif for Ops Board (§2.10) */}
      {topBindingMotif && (
        <div className="bg-surface-raised px-4 py-1.5 border-b border-border flex items-center justify-between text-[11px] font-mono text-text-secondary select-none">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-border inline-block" />
            <span className="font-semibold uppercase tracking-wider text-primary">
              Departmental Dispatch Clipboard
            </span>
          </div>
          <span className="text-[10px]">RLS Scoped · Active Shifts</span>
        </div>
      )}

      {/* Responsive Table Container */}
      <div className="overflow-x-auto w-full">
        <table className="w-full text-left border-collapse text-xs">
          {/* Sticky Table Header */}
          <thead>
            <tr className="border-b border-border bg-surface-raised font-mono text-text-secondary select-none text-[11px] uppercase tracking-wider">
              <th className="py-3 px-4 font-semibold">
                <button
                  type="button"
                  onClick={() => setSortAsc(!sortAsc)}
                  className="flex items-center gap-1 hover:text-primary outline-none focus-visible:ring-1 focus-visible:ring-focus cursor-pointer"
                >
                  <span>Priority</span>
                  <ArrowUpDown className="w-3 h-3" />
                </button>
              </th>

              {showSlaDominantColumn && (
                <th className="py-3 px-4 font-semibold text-primary">
                  SLA Target Timer
                </th>
              )}

              <th className="py-3 px-4 font-semibold">Category / Title</th>
              <th className="py-3 px-4 font-semibold">Ward</th>

              {showDepartmentColumn && (
                <th className="py-3 px-4 font-semibold">Department</th>
              )}

              <th className="py-3 px-4 font-semibold">Status</th>
              <th className="py-3 px-4 font-semibold">Age</th>
              <th className="py-3 px-4 font-semibold">Confidence</th>
              <th className="py-3 px-4 font-semibold text-right">Actions</th>
            </tr>
          </thead>

          {/* Table Body */}
          <tbody className="divide-y divide-border/60">
            {sortedItems.length === 0 ? (
              <tr>
                <td
                  colSpan={showDepartmentColumn ? (showSlaDominantColumn ? 9 : 8) : 8}
                  className="py-12 text-center text-text-secondary"
                >
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              sortedItems.map((item) => {
                const priorityTier =
                  item.priority_score >= 0.85
                    ? 4
                    : item.priority_score >= 0.65
                    ? 3
                    : item.priority_score >= 0.4
                    ? 2
                    : 1;

                return (
                  <tr
                    key={item.id}
                    onClick={() => handleRowClick(item)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') handleRowClick(item);
                    }}
                    tabIndex={0}
                    className="
                      hover:bg-surface-raised transition-colors duration-fast cursor-pointer
                      focus-visible:bg-surface-raised focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-focus
                    "
                  >
                    {/* Priority Column */}
                    <td className="py-3 px-4 whitespace-nowrap">
                      <PriorityChip
                        level={priorityTier as any}
                        score={item.priority_score}
                        size="sm"
                      />
                    </td>

                    {/* SLA Timer (Visually dominant on Ops Board §2.10) */}
                    {showSlaDominantColumn && (
                      <td className="py-3 px-4 whitespace-nowrap">
                        {item.sla_timer ? (
                          <div
                            className={`
                              inline-flex items-center gap-1.5 px-2.5 py-1 rounded-sm border font-mono font-bold text-xs
                              ${
                                item.sla_timer.status === 'urgent'
                                  ? 'bg-status-danger/15 text-status-danger border-status-danger/30'
                                  : item.sla_timer.status === 'warning'
                                  ? 'bg-status-warning/15 text-station-900 border-status-warning/40'
                                  : 'bg-surface-raised text-primary border-border'
                              }
                            `}
                          >
                            <Clock className="w-3.5 h-3.5 flex-shrink-0" />
                            <span>{item.sla_timer.label}</span>
                            <span className="text-[10px] font-normal text-text-secondary">
                              ({item.sla_timer.hours_left}h rem)
                            </span>
                          </div>
                        ) : (
                          <span className="text-text-secondary font-mono">No SLA</span>
                        )}
                      </td>
                    )}

                    {/* Category & Alphanumeric Token */}
                    <td className="py-3 px-4">
                      <div className="flex flex-col">
                        <span className="font-semibold text-primary truncate max-w-xs">
                          {item.title}
                        </span>
                        {item.tracking_token && (
                          <span className="text-[11px] font-mono text-text-secondary">
                            {item.tracking_token}
                          </span>
                        )}
                      </div>
                    </td>

                    {/* Ward Column */}
                    <td className="py-3 px-4 whitespace-nowrap">
                      <span className="font-mono text-text-secondary">
                        {item.ward}
                      </span>
                    </td>

                    {/* Department Column (if not scoped) */}
                    {showDepartmentColumn && (
                      <td className="py-3 px-4 whitespace-nowrap text-text-secondary">
                        {item.department}
                      </td>
                    )}

                    {/* Status Badge */}
                    <td className="py-3 px-4 whitespace-nowrap">
                      <Badge
                        size="sm"
                        variant={
                          item.status === 'resolved' || item.status === 'completed'
                            ? 'success'
                            : 'neutral'
                        }
                      >
                        {item.status.replace('_', ' ')}
                      </Badge>
                    </td>

                    {/* Age */}
                    <td className="py-3 px-4 whitespace-nowrap font-mono text-text-secondary">
                      {item.age}
                    </td>

                    {/* Confidence */}
                    <td className="py-3 px-4 whitespace-nowrap">
                      <ConfidenceBadge
                        confidence_score={item.confidence_score}
                        size="sm"
                      />
                    </td>

                    {/* Action Affordance */}
                    <td className="py-3 px-4 text-right whitespace-nowrap">
                      <div className="flex items-center justify-end gap-1">
                        {onOpenDetailRoute && (
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              onOpenDetailRoute(item.id);
                            }}
                            className="p-1 text-text-secondary hover:text-primary rounded-sm outline-none focus-visible:ring-1 focus-visible:ring-focus cursor-pointer"
                            title="Open full case detail"
                            aria-label={`Open full case detail for ${item.title}`}
                          >
                            <ExternalLink className="w-3.5 h-3.5" />
                          </button>
                        )}
                        <ChevronRight className="w-3.5 h-3.5 text-text-secondary" />
                      </div>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Inline Quick-Glance Score Drawer (§2.5 / §2.10) */}
      <Drawer
        open={drawerOpen}
        onOpenChange={setDrawerOpen}
        title={selectedItem?.title || 'Case Quick-Glance'}
        description={`Tracking Token: ${selectedItem?.tracking_token || selectedItem?.id || ''}`}
        footer={
          onOpenDetailRoute && selectedItem ? (
            <Button
              variant="primary"
              onClick={() => onOpenDetailRoute(selectedItem.id)}
              rightIcon={<ExternalLink className="w-4 h-4" />}
            >
              Open Full Case File
            </Button>
          ) : undefined
        }
      >
        {selectedItem && (
          <div className="space-y-5 text-xs font-ui">
            <div className="p-3 bg-surface-raised rounded-md border border-border flex items-center justify-between">
              <div>
                <div className="text-[11px] font-mono text-text-secondary">Ward & Location</div>
                <div className="font-semibold text-primary">{selectedItem.ward}</div>
              </div>
              <PriorityChip
                level={
                  (selectedItem.priority_score >= 0.85
                    ? 4
                    : selectedItem.priority_score >= 0.65
                    ? 3
                    : selectedItem.priority_score >= 0.4
                    ? 2
                    : 1) as any
                }
                score={selectedItem.priority_score}
                size="sm"
              />
            </div>

            {/* Score Breakdown (Glass-box AHP math) */}
            <ScoreBreakdown
              priority_score={selectedItem.priority_score}
              raw_priority_score={selectedItem.raw_priority_score || selectedItem.priority_score * 0.85}
              equity_boost={selectedItem.equity_boost || 0.15}
              confidence_score={selectedItem.confidence_score}
              subscores={selectedItem.subscores}
              weights_used={selectedItem.weights_used}
              defaultExpanded={true}
            />

            {selectedItem.assigned_worker && (
              <div className="p-3 bg-surface-raised rounded-md border border-border flex items-center gap-2">
                <UserCheck className="w-4 h-4 text-action-primary flex-shrink-0" />
                <div>
                  <span className="font-semibold text-primary">Assigned Personnel: </span>
                  <span className="text-text-secondary">{selectedItem.assigned_worker}</span>
                </div>
              </div>
            )}
          </div>
        )}
      </Drawer>
    </div>
  );
};
