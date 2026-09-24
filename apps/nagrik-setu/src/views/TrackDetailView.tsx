import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  TrackingTokenDisplay,
  StatusTimeline,
  EvidencePhotoCard,
  Button,
  Badge,
  Skeleton,
  ErrorState,
  ConfidenceBadge,
  computeLeastAdvancedChildStatus,
  ObservationItem,
  IncidentStatusType,
} from '@civicbrain/ui';
import {
  ArrowLeft,
  CheckCircle2,
  AlertTriangle,
  Layers,
  MapPin,
  Calendar,
  ExternalLink,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';

export interface ReportTrackData {
  report_id: string;
  tracking_token: string;
  created_at: string;
  address_text?: string;
  channel: string;
  observations: Array<{
    id: string;
    department: string;
    category: string;
    status: IncidentStatusType;
    severity_score?: number;
    confidence?: number | null;
    image_url?: string;
    updated_at?: string;
    notes?: string;
    resolution_proof_url?: string;
  }>;
}

// Built-in mock fixtures for development & test verification
const MOCK_FIXTURES: Record<string, ReportTrackData> = {
  // Core test case: 2 observations in different departments at different statuses
  // Roads is RESOLVED, Drains is IN_PROGRESS -> Parent is PARTIALLY RESOLVED / IN_PROGRESS
  'CB-2026-W14-8892': {
    report_id: 'a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d',
    tracking_token: 'CB-2026-W14-8892',
    created_at: '2026-09-22 14:20 IST',
    address_text: 'Near Indiranagar Metro Station, 100ft Road, Ward 14',
    channel: 'pwa',
    observations: [
      {
        id: 'obs-roads-01',
        department: 'Roads & Infrastructure',
        category: 'Pothole (Arterial Roadway)',
        status: 'resolved',
        severity_score: 0.82,
        confidence: 0.88,
        image_url: 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=800&auto=format&fit=crop&q=80',
        resolution_proof_url: 'https://images.unsplash.com/photo-1584467735871-8e85353a8413?w=800&auto=format&fit=crop&q=80',
        updated_at: '2026-09-24 09:30 IST',
        notes: 'Bitumen patch compacted by road gang #4. Surface levelled.',
      },
      {
        id: 'obs-drains-02',
        department: 'Stormwater Drains',
        category: 'Culvert Blockage / Waterlogging',
        status: 'in_progress',
        severity_score: 0.90,
        confidence: 0.74,
        image_url: 'https://images.unsplash.com/photo-1541888946425-d0fbb186c5f9?w=800&auto=format&fit=crop&q=80',
        updated_at: '2026-09-24 10:15 IST',
        notes: 'Excavation team on-site clearing silt and broken pavers.',
      },
    ],
  },
  // All resolved fixture (ready for confirmation)
  'CB-2026-W11-4012': {
    report_id: 'f9e8d7c6-b5a4-4321-8765-fedcba987654',
    tracking_token: 'CB-2026-W11-4012',
    created_at: '2026-09-20 11:00 IST',
    address_text: '8th Cross, Malleshwaram, Ward 11',
    channel: 'whatsapp',
    observations: [
      {
        id: 'obs-swm-01',
        department: 'Solid Waste Management',
        category: 'Garbage Blackspot Clearing',
        status: 'resolved',
        severity_score: 0.75,
        confidence: 0.91,
        image_url: 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800&auto=format&fit=crop&q=80',
        resolution_proof_url: 'https://images.unsplash.com/photo-1584467735871-8e85353a8413?w=800&auto=format&fit=crop&q=80',
        updated_at: '2026-09-23 16:45 IST',
        notes: 'Dump cleared, area disinfected with bleaching powder.',
      },
    ],
  },
};

export const TrackDetailView: React.FC = () => {
  const { token } = useParams<{ token: string }>();
  const navigate = useNavigate();

  const [isLoading, setIsLoading] = useState(true);
  const [report, setReport] = useState<ReportTrackData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expandedObservations, setExpandedObservations] = useState<Record<string, boolean>>({});

  useEffect(() => {
    if (!token) {
      setError('No tracking token provided in URL.');
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setError(null);

    // Simulate network fetch with live fallback to API or mock fixture
    const timeout = setTimeout(async () => {
      try {
        // Attempt backend endpoint if reachable
        const res = await fetch(`/v1/intake/reports/track?token=${encodeURIComponent(token)}`);
        if (res.ok) {
          const data = await res.json();
          // Map backend response shape to ReportTrackData
          const mappedObservations = (data.observations || []).map((o: any) => ({
            id: o.id || `obs-${Math.random().toString(36).substring(2, 7)}`,
            department: o.department || o.department_id || 'Municipal Services',
            category: o.category_code || o.category || 'Civic Defect',
            status: (o.status || 'reported').toLowerCase() as IncidentStatusType,
            severity_score: o.severity_score,
            confidence: o.confidence,
            image_url: o.image_url || o.source_media_url,
            updated_at: o.updated_at || data.updated_at,
            notes: o.notes,
          }));

          setReport({
            report_id: data.report_id || data.id,
            tracking_token: token,
            created_at: data.created_at || 'Recently submitted',
            address_text: data.address_text,
            channel: data.channel || 'pwa',
            observations: mappedObservations,
          });
          setIsLoading(false);
          return;
        }
      } catch {
        // Fall back to local fixtures
      }

      // Check local mock fixture
      const fixture = MOCK_FIXTURES[token];
      if (fixture) {
        setReport(fixture);
        setIsLoading(false);
      } else {
        setError(`No intake report found for tracking token "${token}".`);
        setIsLoading(false);
      }
    }, 400);

    return () => clearTimeout(timeout);
  }, [token]);

  const toggleObservationGallery = (id: string) => {
    setExpandedObservations((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  // 1. Loading State (Skeleton matching real timeline structure)
  if (isLoading) {
    return (
      <div className="w-full max-w-[720px] mx-auto py-6 sm:py-10 px-4 flex flex-col gap-6 font-ui">
        <Skeleton variant="rect" height={80} className="w-full rounded-md" />
        <Skeleton variant="rect" height={60} className="w-full rounded-md" />
        <div className="space-y-4">
          <Skeleton variant="rect" height={220} className="w-full rounded-md" />
          <Skeleton variant="rect" height={220} className="w-full rounded-md" />
        </div>
      </div>
    );
  }

  // 2. Token Not Found / Error State
  if (error || !report) {
    return (
      <div className="w-full max-w-[720px] mx-auto py-8 sm:py-12 px-4 flex flex-col gap-6 font-ui">
        <Link
          to="/track"
          className="inline-flex items-center gap-1.5 text-xs font-medium text-text-secondary hover:text-primary transition-colors duration-fast w-fit"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Track Lookup</span>
        </Link>

        <ErrorState
          title="Tracking Token Not Found"
          message={error || 'The requested tracking token does not match any active or closed record.'}
          nextStep="Double-check the reference token on your submission waybill stub or search using your registered phone number."
          onRetry={() => navigate('/track')}
          retryLabel="Search Another Token"
        />
      </div>
    );
  }

  // Compute least-advanced child status dynamically on the client
  // NEVER trust pre-collapsed status (FRONTEND_CONTEXT.md §4 & SCREEN_SPECS.md §2.3)
  const observationItems: ObservationItem[] = report.observations.map((o) => ({
    id: o.id,
    department: o.department,
    category: o.category,
    status: o.status,
    updated_at: o.updated_at,
    notes: o.notes,
  }));

  const { parentStatus, isPartiallyResolved, minStatus } =
    computeLeastAdvancedChildStatus(observationItems);

  // Check if all observations are resolved (qualifying for resolution confirm/dispute)
  const allResolvedOrConfirmed = report.observations.every(
    (o) => o.status === 'resolved' || o.status === 'confirmed'
  );
  const anyResolved = report.observations.some(
    (o) => o.status === 'resolved' || o.status === 'confirmed'
  );

  // Plain language status text
  const totalCount = report.observations.length;
  const resolvedCount = report.observations.filter(
    (o) => o.status === 'resolved' || o.status === 'confirmed'
  ).length;

  let plainStatusBannerText = '';
  if (allResolvedOrConfirmed) {
    plainStatusBannerText = `All ${totalCount} issue${totalCount > 1 ? 's' : ''} resolved. Please review and confirm satisfactory work.`;
  } else if (isPartiallyResolved) {
    plainStatusBannerText = `Still in progress — ${resolvedCount} of ${totalCount} issues resolved.`;
  } else {
    plainStatusBannerText = `Currently in progress (${minStatus.replace('_', ' ')}). Zero issues prematurely marked closed.`;
  }

  return (
    <div className="w-full max-w-[720px] mx-auto py-6 sm:py-10 px-4 flex flex-col gap-6 font-ui">
      {/* Top Navigation */}
      <div className="flex items-center justify-between">
        <Link
          to="/track"
          className="inline-flex items-center gap-1.5 text-xs font-medium text-text-secondary hover:text-primary transition-colors duration-fast"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Lookup Another Report</span>
        </Link>

        <span className="text-xs font-mono text-text-secondary">
          Nagrik Setu · Public Tracking Ledger
        </span>
      </div>

      {/* 1. Tracking Token Waybill Stub at top */}
      <TrackingTokenDisplay
        token={report.tracking_token}
        timestamp={report.created_at}
        summary={report.address_text}
        size="md"
      />

      {/* 2. Parent-Level Plain Language Status Banner */}
      <div
        role="status"
        aria-live="polite"
        className={`
          p-4 sm:p-5 rounded-md border flex flex-col gap-2 transition-colors duration-fast
          ${
            allResolvedOrConfirmed
              ? 'bg-status-success/10 border-status-success/30 text-primary'
              : isPartiallyResolved
              ? 'bg-action-primary/10 border-action-primary/30 text-primary'
              : 'bg-surface border-border text-primary'
          }
        `}
      >
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
            Report Aggregate Progress (Honest Invariant)
          </span>
          <Badge
            variant={
              allResolvedOrConfirmed
                ? 'success'
                : isPartiallyResolved
                ? 'warning'
                : 'default'
            }
          >
            {isPartiallyResolved ? 'Partially Resolved' : parentStatus.replace('_', ' ')}
          </Badge>
        </div>

        <p className="text-sm font-semibold text-primary leading-snug">
          {plainStatusBannerText}
        </p>

        <p className="text-xs text-text-secondary">
          CivicBrain enforces the least-advanced-child invariant: reports remain active until
          every department completes physical remediation.
        </p>
      </div>

      {/* 3. Action Banner if Resolved: Confirm or Dispute CTA */}
      {allResolvedOrConfirmed && (
        <div className="p-4 sm:p-5 bg-surface-raised rounded-md border-2 border-action-primary/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex flex-col gap-1">
            <span className="text-sm font-semibold text-primary">
              Ready for Citizen Verification
            </span>
            <span className="text-xs text-text-secondary">
              Review before/after evidence photos submitted by municipal field crew.
            </span>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="primary"
              size="sm"
              onClick={() => navigate(`/track/${report.tracking_token}/confirm`)}
            >
              Verify Resolution
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => navigate(`/track/${report.tracking_token}/dispute`)}
            >
              Dispute Closure
            </Button>
          </div>
        </div>
      )}

      {/* 4. One StatusTimeline per Observation — NEVER MERGED INTO ONE BAR */}
      <div className="flex flex-col gap-6">
        <div className="flex items-center justify-between pb-1 border-b border-border">
          <h2 className="text-sm font-semibold text-primary uppercase tracking-wider">
            Issue Observations ({report.observations.length})
          </h2>
          <span className="text-xs font-mono text-text-secondary">
            Per-Observation Timelines
          </span>
        </div>

        {report.observations.map((obs, idx) => {
          const isExpanded = Boolean(expandedObservations[obs.id]);

          return (
            <div
              key={obs.id}
              className="bg-surface rounded-md border border-border overflow-hidden flex flex-col"
            >
              {/* Timeline Header with Department & Category */}
              <div className="p-4 border-b border-border flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2.5">
                  <span className="w-6 h-6 rounded-full bg-surface-raised border border-border text-xs font-mono font-bold flex items-center justify-center">
                    {idx + 1}
                  </span>
                  <div>
                    <h3 className="font-semibold text-base text-primary">
                      {obs.category}
                    </h3>
                    <div className="text-xs font-mono text-text-secondary">
                      Department: <strong>{obs.department}</strong>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 self-start sm:self-auto">
                  <ConfidenceBadge confidence_score={obs.confidence} size="sm" />
                  <Badge
                    variant={
                      obs.status === 'resolved' || obs.status === 'confirmed'
                        ? 'success'
                        : 'neutral'
                    }
                  >
                    {obs.status.replace('_', ' ')}
                  </Badge>
                </div>
              </div>

              {/* Render the individual observation StatusTimeline */}
              <div className="p-4 sm:p-5">
                <StatusTimeline
                  observations={[
                    {
                      id: obs.id,
                      department: obs.department,
                      category: obs.category,
                      status: obs.status,
                      updated_at: obs.updated_at,
                      notes: obs.notes,
                    },
                  ]}
                />
              </div>

              {/* Evidence Section (Citizen Photo + Resolution Proof) */}
              <div className="px-4 pb-4">
                <button
                  type="button"
                  onClick={() => toggleObservationGallery(obs.id)}
                  aria-expanded={isExpanded}
                  className="
                    w-full py-2.5 px-3 rounded-sm bg-surface-raised hover:bg-surface border border-border
                    text-xs font-medium text-primary flex items-center justify-between transition-colors
                    outline-none focus-visible:ring-2 focus-visible:ring-focus
                  "
                >
                  <span className="flex items-center gap-2">
                    <Layers className="w-3.5 h-3.5 text-text-secondary" />
                    <span>Evidence Photos & Field Proofs</span>
                  </span>
                  {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </button>

                {isExpanded && (
                  <div className="mt-3 pt-3 border-t border-border grid grid-cols-1 sm:grid-cols-2 gap-4 animate-in fade-in-50 duration-fast">
                    {obs.image_url ? (
                      <div className="flex flex-col gap-1.5">
                        <span className="text-[11px] font-semibold text-text-secondary uppercase tracking-wider">
                          Citizen Ingest Photo
                        </span>
                        <EvidencePhotoCard
                          src={obs.image_url}
                          alt={`${obs.category} reported at ${report.address_text || 'site'}`}
                          coordinates="12.9716° N, 77.5946° E"
                          timestamp={report.created_at}
                          isRedacted={true}
                          caption="Reported Defect"
                        />
                      </div>
                    ) : (
                      <div className="p-4 rounded-sm border border-dashed border-border text-center text-xs text-text-secondary">
                        No citizen photo submitted with this defect.
                      </div>
                    )}

                    {obs.resolution_proof_url ? (
                      <div className="flex flex-col gap-1.5">
                        <span className="text-[11px] font-semibold text-status-success uppercase tracking-wider">
                          Department Resolution Proof
                        </span>
                        <EvidencePhotoCard
                          src={obs.resolution_proof_url}
                          alt={`Resolution completed for ${obs.category}`}
                          coordinates="12.9716° N, 77.5946° E"
                          timestamp={obs.updated_at || 'Recent'}
                          isRedacted={true}
                          caption="Field Verification"
                        />
                      </div>
                    ) : (
                      <div className="p-4 rounded-sm border border-dashed border-border text-center text-xs text-text-secondary flex flex-col items-center justify-center">
                        <span className="font-medium text-primary mb-1">Resolution Pending</span>
                        <span>Field work order actively in progress. Photo proof will be uploaded upon completion.</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
