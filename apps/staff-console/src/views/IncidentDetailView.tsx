import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  EvidencePhotoCard,
  ScoreBreakdown,
  StatusTimeline,
  ConfidenceBadge,
  PriorityChip,
  Badge,
  Button,
  Skeleton,
  ErrorState,
  IncidentStatusType,
  useToast,
} from '@civicbrain/ui';
import {
  ArrowLeft,
  MapPin,
  Calendar,
  Layers,
  ArrowRight,
  GitBranch,
  ShieldAlert,
  Send,
  CheckCircle2,
  RefreshCw,
  FileText,
} from 'lucide-react';
import { getValidNextStatuses, STATUS_LABELS } from '../logic/lifecycle';

export interface CausalLinkItem {
  id: string;
  type: 'upstream_cause' | 'downstream_symptom';
  related_incident_id: string;
  category: string;
  department: string;
  coupling_coefficient: number;
}

export interface IncidentDetailData {
  id: string;
  tracking_token: string;
  category_code: string;
  category_name: string;
  department_name: string;
  ward_name: string;
  ward_code: string;
  address_text: string;
  created_at: string;
  status: IncidentStatusType;
  priority_score: number;
  raw_priority_score: number;
  equity_boost: number;
  confidence_score: number | null;
  subscores: {
    severity: number;
    risk: number;
    exposure: number;
    criticality: number;
    urgency: number;
  };
  weights_used: {
    severity: number;
    risk: number;
    exposure: number;
    criticality: number;
    urgency: number;
  };
  observations: Array<{
    id: string;
    department: string;
    category: string;
    status: IncidentStatusType;
    severity_score: number;
    confidence: number | null;
    image_url: string;
    resolution_proof_url?: string;
    updated_at: string;
    notes: string;
  }>;
  causal_links?: CausalLinkItem[];
}

const MOCK_INCIDENT_CASE: IncidentDetailData = {
  id: 'inc-9921-bengaluru',
  tracking_token: 'CB-2026-W14-8892',
  category_code: 'ROAD_POTHOLE_ARTERIAL',
  category_name: 'Arterial Road Paver Failure & Waterlogging',
  department_name: 'Roads & Infrastructure',
  ward_name: 'Indiranagar',
  ward_code: 'Ward 14 (South Zone)',
  address_text: 'Near Indiranagar Metro Station, 100ft Road, Ward 14',
  created_at: '2026-09-22 14:20 IST (2 days ago)',
  status: 'assigned',
  priority_score: 0.99,
  raw_priority_score: 0.84,
  equity_boost: 0.18,
  confidence_score: 0.74,
  subscores: {
    severity: 0.88,
    risk: 0.76,
    exposure: 0.82,
    criticality: 0.90,
    urgency: 0.85,
  },
  weights_used: {
    severity: 0.35,
    risk: 0.25,
    exposure: 0.15,
    criticality: 0.15,
    urgency: 0.10,
  },
  observations: [
    {
      id: 'obs-001',
      department: 'Roads & Infrastructure',
      category: 'Pothole (Arterial Roadway)',
      status: 'assigned',
      severity_score: 0.82,
      confidence: 0.88,
      image_url: 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=800&auto=format&fit=crop&q=80',
      updated_at: '2026-09-23 11:30 IST',
      notes: 'Road gang #4 assigned. Equipment mobilization in progress.',
    },
    {
      id: 'obs-002',
      department: 'Stormwater Drains',
      category: 'Blocked Culvert / Silt Accumulation',
      status: 'triaged',
      severity_score: 0.90,
      confidence: 0.74,
      image_url: 'https://images.unsplash.com/photo-1541888946425-d0fbb186c5f9?w=800&auto=format&fit=crop&q=80',
      updated_at: '2026-09-22 15:45 IST',
      notes: 'Culvert blockage causing roadway runoff. Excavation required.',
    },
  ],
  causal_links: [
    {
      id: 'causal-link-01',
      type: 'upstream_cause',
      related_incident_id: 'inc-9915-drainage',
      category: 'Main Stormwater Conduit Siltation',
      department: 'Stormwater Drains',
      coupling_coefficient: 0.85,
    },
  ],
};

export const IncidentDetailView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();

  const [isLoading, setIsLoading] = useState(false);
  const [incident, setIncident] = useState<IncidentDetailData>(MOCK_INCIDENT_CASE);
  const [isTransitioning, setIsTransitioning] = useState(false);

  // Compute valid next states client-side from the current status
  const validNextStates = getValidNextStatuses(incident.status);

  const handleStatusTransition = async (nextStatus: IncidentStatusType) => {
    setIsTransitioning(true);
    // Optimistic update per SCREEN_SPECS.md §2.6
    const previousStatus = incident.status;
    setIncident((prev) => ({
      ...prev,
      status: nextStatus,
    }));

    try {
      // Simulate or execute PATCH /v1/incidents/{id}/status
      await new Promise((r) => setTimeout(r, 300));
      toast({
        title: 'Status Transition Committed',
        description: `Incident status updated from "${previousStatus}" to "${nextStatus}". Parent report re-aggregated.`,
        variant: 'success',
      });
    } catch {
      // Rollback on error
      setIncident((prev) => ({ ...prev, status: previousStatus }));
      toast({
        title: 'Transition Failed',
        description: 'Could not commit status update to server. Rolled back.',
        variant: 'danger',
      });
    } finally {
      setIsTransitioning(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 space-y-6">
        <Skeleton variant="rect" height={64} className="w-full" />
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-7 space-y-4">
            <Skeleton variant="rect" height={320} className="w-full" />
          </div>
          <div className="lg:col-span-5 space-y-4">
            <Skeleton variant="rect" height={320} className="w-full" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-background text-primary font-ui">
      {/* Top Sticky 64px Context Strip (SCREEN_SPECS.md §2.6) */}
      <header className="sticky top-0 z-sticky h-16 bg-surface border-b border-border px-6 flex items-center justify-between shadow-flat">
        <div className="flex items-center gap-4 min-w-0">
          <Link
            to="/deck"
            className="p-1.5 rounded-sm hover:bg-surface-raised border border-border text-text-secondary hover:text-primary transition-colors"
            aria-label="Back to Command Deck Incident Queue"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>

          <div className="flex items-center gap-2.5 truncate">
            <span className="font-mono text-xs font-bold text-text-secondary">
              {incident.tracking_token}
            </span>
            <span className="text-border">|</span>
            <h1 className="text-sm font-semibold text-primary truncate">
              {incident.category_name}
            </h1>
            <Badge variant="neutral" size="sm" className="hidden sm:inline-flex">
              {incident.ward_code}
            </Badge>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <PriorityChip level={4} score={incident.priority_score} size="sm" />
          <Badge
            variant={
              incident.status === 'resolved' || incident.status === 'confirmed'
                ? 'success'
                : 'default'
            }
            size="sm"
          >
            {incident.status.replace('_', ' ')}
          </Badge>
        </div>
      </header>

      {/* Main Content: 60/40 Split on Desktop (lg:grid-cols-12), 100/100 Stacked below 1024px */}
      <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left 60% = Observation List + Evidence Gallery + Causal Links (SCREEN_SPECS.md §2.6) */}
          <section className="lg:col-span-7 flex flex-col gap-8 order-1">
            
            {/* Header info card */}
            <div className="p-5 bg-surface rounded-md border border-border flex flex-col gap-3">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
                    Incident Case Overview
                  </span>
                  <h2 className="text-lg font-bold text-primary mt-0.5">
                    {incident.category_name}
                  </h2>
                </div>
                <ConfidenceBadge confidence_score={incident.confidence_score} size="md" />
              </div>

              <div className="flex flex-wrap items-center gap-4 text-xs font-mono text-text-secondary pt-2 border-t border-border">
                <span className="flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-action-primary" />
                  <span>{incident.address_text}</span>
                </span>
                <span className="flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5" />
                  <span>{incident.created_at}</span>
                </span>
              </div>
            </div>

            {/* Evidence Gallery Stack (DESIGN.md §7: full EvidencePhotoCard treatment) */}
            <div className="flex flex-col gap-4">
              <div className="flex items-center justify-between pb-2 border-b border-border">
                <div className="flex items-center gap-2">
                  <Layers className="w-4 h-4 text-action-primary" />
                  <h3 className="text-sm font-semibold text-primary uppercase tracking-wider">
                    Evidence Photography ({incident.observations.length} Observations)
                  </h3>
                </div>
                <span className="text-xs font-mono text-text-secondary">
                  Native 4:3 Aspect · PII Redacted
                </span>
              </div>

              <div className="space-y-6">
                {incident.observations.map((obs, idx) => (
                  <div key={obs.id} className="flex flex-col gap-2">
                    <div className="flex items-center justify-between text-xs px-1">
                      <span className="font-semibold text-primary">
                        Observation #{idx + 1}: {obs.category} ({obs.department})
                      </span>
                      <Badge size="sm">{obs.status.replace('_', ' ')}</Badge>
                    </div>

                    <EvidencePhotoCard
                      src={obs.image_url}
                      alt={`${obs.category} on 100ft Road Indiranagar`}
                      coordinates="12.9716° N, 77.5946° E"
                      timestamp={obs.updated_at}
                      caption={`Ingest Media · ${obs.department}`}
                      isRedacted={true}
                    />

                    {obs.notes && (
                      <div className="p-3 bg-surface-raised rounded-sm border border-border text-xs text-text-secondary font-mono">
                        <strong className="text-primary font-medium">Field Dispatch Note: </strong>
                        {obs.notes}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Causal Links (Root-Cause / Symptom mapping) */}
            {incident.causal_links && incident.causal_links.length > 0 && (
              <div className="p-5 bg-surface rounded-md border border-border flex flex-col gap-3">
                <div className="flex items-center gap-2 pb-2 border-b border-border">
                  <GitBranch className="w-4 h-4 text-channel-600" />
                  <h3 className="text-sm font-semibold text-primary uppercase tracking-wider">
                    Causal Intelligence Links
                  </h3>
                </div>

                <div className="space-y-2">
                  {incident.causal_links.map((link) => (
                    <div
                      key={link.id}
                      className="p-3 bg-surface-raised rounded-sm border border-border flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs"
                    >
                      <div className="flex flex-col">
                        <span className="font-semibold text-primary flex items-center gap-1.5">
                          <span className="text-status-warning font-mono">Upstream Root Cause:</span>
                          <span>{link.category}</span>
                        </span>
                        <span className="text-[11px] text-text-secondary font-mono">
                          Linked Case: {link.related_incident_id} · Dept: {link.department}
                        </span>
                      </div>

                      <div className="font-mono text-xs text-right self-end sm:self-auto">
                        <span className="text-text-secondary">Coupling: </span>
                        <strong className="text-action-primary">{(link.coupling_coefficient * 100).toFixed(0)}%</strong>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>

          {/* Right 40% = ScoreBreakdown (Expanded) + Status Controls + Dispatch Actions */}
          <aside className="lg:col-span-5 flex flex-col gap-6 order-2">
            
            {/* Status Transition Control (High consequence interactive element) */}
            <div className="p-5 bg-surface rounded-md border-2 border-border shadow-flat flex flex-col gap-4">
              <div className="flex items-center justify-between pb-2 border-b border-border">
                <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
                  Case Status Transition Control
                </span>
                <Badge variant="neutral" size="sm">
                  11-State Machine
                </Badge>
              </div>

              <div className="flex items-center justify-between bg-surface-raised p-3 rounded-sm border border-border">
                <span className="text-xs text-text-secondary">Current State:</span>
                <span className="font-mono font-bold text-sm uppercase tracking-wide text-primary">
                  {incident.status.replace('_', ' ')}
                </span>
              </div>

              {/* Staff-Only Valid Next State Transition Buttons (Never a free-form dropdown!) */}
              <div className="flex flex-col gap-2">
                <span className="text-xs font-medium text-text-secondary">
                  Permitted Valid Next Transitions:
                </span>

                {validNextStates.length > 0 ? (
                  <div className="flex flex-col gap-2">
                    {validNextStates.map((nextState) => (
                      <Button
                        key={nextState}
                        variant={nextState === 'rejected' ? 'destructive' : 'primary'}
                        size="md"
                        disabled={isTransitioning}
                        onClick={() => handleStatusTransition(nextState)}
                        rightIcon={<ArrowRight className="w-4 h-4" />}
                        className="w-full justify-between"
                      >
                        <span>{STATUS_LABELS[nextState]}</span>
                        <span className="font-mono text-[11px] opacity-80 uppercase tracking-wider">
                          ({nextState})
                        </span>
                      </Button>
                    ))}
                  </div>
                ) : (
                  <div className="p-3 rounded-sm bg-surface-raised border border-border text-center text-xs text-text-secondary">
                    Terminal State Reached ({incident.status}). No further transitions allowed.
                  </div>
                )}
              </div>

              {/* Quick dispatch re-assign link */}
              <div className="pt-3 border-t border-border flex items-center justify-between">
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => navigate('/deck/dispatch/new')}
                  leftIcon={<Send className="w-3.5 h-3.5" />}
                  className="w-full"
                >
                  Create Work Order Dispatch
                </Button>
              </div>
            </div>

            {/* ScoreBreakdown: Expanded by default on Incident Detail per SCREEN_SPECS.md §2.6 */}
            <div className="flex flex-col gap-2">
              <div className="flex items-center justify-between px-1">
                <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
                  Prioritization Mathematics
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => navigate(`/deck/prioritize/${incident.id}`)}
                  className="text-xs h-7 px-2"
                >
                  Re-run AHP Matrix
                </Button>
              </div>

              <ScoreBreakdown
                priority_score={incident.priority_score}
                raw_priority_score={incident.raw_priority_score}
                equity_boost={incident.equity_boost}
                confidence_score={incident.confidence_score}
                subscores={incident.subscores}
                weights_used={incident.weights_used}
                ward_name={incident.ward_name}
                defaultExpanded={true}
              />
            </div>

            {/* Observation Status Timeline */}
            <div className="p-5 bg-surface rounded-md border border-border flex flex-col gap-3">
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
                Multi-Department Lifecycle Progress
              </span>
              <StatusTimeline observations={incident.observations} />
            </div>

          </aside>
        </div>
      </main>
    </div>
  );
};
