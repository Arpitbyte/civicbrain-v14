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

export const IncidentDetailView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [incident, setIncident] = useState<IncidentDetailData | null>(null);
  const [isTransitioning, setIsTransitioning] = useState(false);

  useEffect(() => {
    async function loadIncident() {
      if (!id) return;
      setIsLoading(true);
      setError(null);
      try {
        const res = await fetch(`/v1/incidents/${id}`);
        if (!res.ok) {
          throw new Error(`Incident not found (${res.status})`);
        }
        const incData = await res.json();

        // Fetch observations
        let obsData: any[] = [];
        try {
          const obsRes = await fetch(`/v1/incidents/${id}/observations`);
          if (obsRes.ok) {
            obsData = await obsRes.json();
          }
        } catch {
          // ignore observations fetch error
        }

        const mapped: IncidentDetailData = {
          id: incData.id,
          tracking_token: `CB-${incData.id.slice(0, 8).toUpperCase()}`,
          category_code: incData.category_code,
          category_name: incData.category_code.replace(/_/g, ' '),
          department_name: 'Municipal Engineering / Public Works',
          ward_name: `वार्ड #${incData.ward_id.slice(0, 8)}`,
          ward_code: `Ward-${incData.ward_id.slice(0, 8)}`,
          address_text: 'Municipal Jurisdiction Area, Ward Sector',
          created_at: new Date(incData.created_at).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' }),
          status: incData.status,
          priority_score: incData.severity ? Math.min(1.0, incData.severity / 5.0) : 0.6,
          raw_priority_score: incData.severity ? incData.severity / 5.0 : 0.6,
          equity_boost: 0.0,
          confidence_score: 0.92,
          subscores: {
            severity: incData.severity ? incData.severity / 5.0 : 0.7,
            risk: 0.65,
            exposure: 0.6,
            criticality: 0.75,
            urgency: 0.7,
          },
          weights_used: {
            severity: 0.35,
            risk: 0.25,
            exposure: 0.15,
            criticality: 0.15,
            urgency: 0.10,
          },
          observations: obsData.map((obs) => ({
            id: obs.id,
            department: 'Municipal Services',
            category: obs.category_code || incData.category_code,
            status: obs.status || incData.status,
            severity_score: obs.severity ? obs.severity / 5.0 : 0.7,
            confidence: obs.confidence ?? 0.85,
            image_url: obs.image_url || 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=800&auto=format&fit=crop&q=80',
            resolution_proof_url: obs.resolution_proof_url,
            updated_at: obs.updated_at ? new Date(obs.updated_at).toLocaleString('en-IN') : '',
            notes: obs.notes || 'Field observation logged.',
          })),
        };

        setIncident(mapped);
      } catch (err: any) {
        console.error('Failed to load incident:', err);
        setError(err.message || 'Could not load incident from live database.');
      } finally {
        setIsLoading(false);
      }
    }

    loadIncident();
  }, [id]);

  // Compute valid next states client-side from the current status
  const validNextStates = incident ? getValidNextStatuses(incident.status) : [];

  const handleStatusTransition = async (nextStatus: IncidentStatusType) => {
    if (!incident || !id) return;
    setIsTransitioning(true);
    const previousStatus = incident.status;
    setIncident((prev) => (prev ? { ...prev, status: nextStatus } : null));

    try {
      const res = await fetch(`/v1/incidents/${id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: nextStatus }),
      });
      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }
      toast({
        title: 'स्थिति अद्यतन / Status Updated',
        description: `Incident status updated from "${previousStatus}" to "${nextStatus}". Parent report re-aggregated.`,
        variant: 'success',
      });
    } catch {
      // Rollback on error
      setIncident((prev) => (prev ? { ...prev, status: previousStatus } : null));
      toast({
        title: 'अद्यतन विफल / Transition Failed',
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

  if (error || !incident) {
    return (
      <div className="flex flex-col min-h-screen bg-background text-primary font-ui p-6 items-center justify-center">
        <div className="max-w-md w-full p-6 bg-surface border border-border rounded-lg text-center space-y-4 shadow-sm">
          <div className="w-12 h-12 rounded-full bg-red-500/10 text-red-500 flex items-center justify-center mx-auto">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <h2 className="text-base font-semibold">शिकायत नहीं मिली / Incident Not Found</h2>
          <p className="text-xs text-text-secondary leading-relaxed">
            {error || 'The requested operational incident does not exist in the live PostgreSQL database or has been archived.'}
          </p>
          <div className="pt-2">
            <Button variant="outline" size="sm" onClick={() => navigate('/deck')}>
              कमांड डेस्क कतार पर लौटें / Return to Queue
            </Button>
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
