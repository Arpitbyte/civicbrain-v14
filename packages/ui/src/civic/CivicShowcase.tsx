import React, { useState } from 'react';
import {
  ConfidenceBadge,
  ScoreBreakdown,
  EvidencePhotoCard,
  BeforeAfterPair,
  StatusTimeline,
  TrackingTokenDisplay,
  OfflineSyncBadge,
  PriorityChip,
  SealMark,
  WardBoundaryMapLayer,
  IncidentPointLayer,
  ClusterLayer,
} from './index';
import { ToastProvider } from '../primitives/Toast';

const WORKSPACES = [
  { id: 'nagrik-setu', name: 'Nagrik Setu (Citizen)' },
  { id: 'command-deck', name: 'Command Deck (Triage)' },
  { id: 'ops-board', name: 'Ops Board (Dept)' },
  { id: 'city-pulse', name: 'City Pulse (Supervisor)' },
  { id: 'karmi-sahayak', name: 'Karmi Sahayak (Field)' },
  { id: 'control-room', name: 'Control Room (Admin)' },
  { id: 'transparency-board', name: 'Transparency Board (Public)' },
] as const;

export const CivicShowcaseInner: React.FC = () => {
  const [currentWorkspace, setCurrentWorkspace] = useState<string>('command-deck');
  const [isOnline, setIsOnline] = useState(true);
  const [pendingSyncCount, setPendingSyncCount] = useState(3);

  // Sample real API response fixture for Prioritization Engine
  const sampleApiResponse = {
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
    raw_priority_score: 0.84,
    equity_boost: 0.18,
    final_priority_score: 0.99,
    confidence_score: 0.72,
    requires_human_review: false,
    review_reason: null,
    target_status: 'prioritized',
  };

  // Sample real multi-issue observations fixture (e.g. Roads + Stormwater Drains split)
  const sampleObservations = [
    {
      id: 'obs-001',
      department: 'Roads & Infrastructure',
      category: 'Pothole (Arterial Roadway)',
      status: 'resolved' as const,
      updated_at: '2026-09-24 09:30',
      notes: 'Cold-mix asphalt patch completed and compacted by crew.',
    },
    {
      id: 'obs-002',
      department: 'Stormwater Drains',
      category: 'Blocked Culvert / Waterlogging',
      status: 'in_progress' as const,
      updated_at: '2026-09-24 10:15',
      notes: 'Excavation team on-site clearing silt blockage.',
    },
  ];

  return (
    <div
      data-workspace={currentWorkspace}
      className="min-h-screen bg-background text-primary p-6 md:p-10 font-ui transition-colors duration-fast"
    >
      {/* Header bar with workspace switcher */}
      <header className="mb-10 pb-6 border-b border-border flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-primary">
              CivicBrain Civic Components Showcase
            </h1>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-action-primary/15 text-primary border border-action-primary/30 font-semibold">
              Tier 1 Civic Vocabulary
            </span>
          </div>
          <p className="text-sm text-text-secondary mt-1 max-w-2xl">
            Isolated demo showing CivicBrain's high-leverage civic components: Bühlmann credibility badges,
            itemized AHP score breakdown, physical waybill token, least-advanced child timeline, before/after evidence,
            and offline sync badges.
          </p>
        </div>

        <div className="flex items-center gap-3 bg-surface p-2 rounded-md border border-border">
          <label htmlFor="civic-workspace-select" className="text-xs font-semibold text-text-secondary whitespace-nowrap">
            Theme Context:
          </label>
          <select
            id="civic-workspace-select"
            value={currentWorkspace}
            onChange={(e) => setCurrentWorkspace(e.target.value)}
            className="text-xs bg-surface-raised border border-border rounded-sm py-1.5 px-2.5 font-medium text-primary outline-none focus:ring-2 focus:ring-focus"
          >
            {WORKSPACES.map((w) => (
              <option key={w.id} value={w.id}>
                {w.name}
              </option>
            ))}
          </select>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        {/* 1. CONFIDENCE BADGES (BÜHLMANN CREDIBILITY) */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">ConfidenceBadge (Credibility Z)</h2>
            <span className="text-xs font-mono text-text-secondary">FRONTEND_CONTEXT §7.1</span>
          </div>

          <div className="space-y-4">
            <p className="text-xs text-text-secondary">
              Strict Bootstrap Principle: If confidence_score is null/cold-start, component honestly displays
              "Citizen Declared" or "Pending Automated Triage" — never a fabricated percentage.
            </p>

            <div className="flex flex-col gap-3">
              <div className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
                Honest Cold-Start States (null / uncalculated)
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <ConfidenceBadge confidence_score={null} coldStartLabel="Citizen Declared" />
                <ConfidenceBadge confidence_score={null} coldStartLabel="Pending Automated Triage" />
              </div>

              <div className="text-xs font-semibold text-text-secondary uppercase tracking-wider mt-2">
                Empirical Credibility Bands (Z = n / [n + K])
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <ConfidenceBadge confidence_score={0.25} />
                <ConfidenceBadge confidence_score={0.58} />
                <ConfidenceBadge confidence_score={0.92} />
              </div>
            </div>
          </div>
        </section>

        {/* 2. PRIORITY CHIP & OFFLINE SYNC BADGE */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">Priority Chips & Offline Sync</h2>
            <span className="text-xs font-mono text-text-secondary">Single-Hue Marker / PWA Sync</span>
          </div>

          <div className="space-y-4">
            <div className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              Priority Chips (Text + Number + Marker Scale, never traffic lights)
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <PriorityChip level={1} score={0.24} />
              <PriorityChip level={2} score={0.48} />
              <PriorityChip level={3} score={0.78} />
              <PriorityChip level={4} score={0.96} />
            </div>

            <div className="pt-2 border-t border-border flex flex-col gap-3">
              <div className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
                OfflineSyncBadge (Interactive)
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <OfflineSyncBadge
                  isOnline={isOnline}
                  pendingCount={pendingSyncCount}
                  onClick={() => setIsOnline(!isOnline)}
                />
                <OfflineSyncBadge isOnline={true} pendingCount={0} />
                <OfflineSyncBadge isOnline={true} isSyncing={true} pendingCount={5} />
                <OfflineSyncBadge isOnline={true} disputeCount={2} />
              </div>
              <span className="text-[11px] text-text-secondary">
                Click badge above to toggle online/offline state.
              </span>
            </div>
          </div>
        </section>

        {/* 3. TRACKING TOKEN WAYBILL & SEAL MARK */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">Waybill Stub & Official Seal</h2>
            <span className="text-xs font-mono text-text-secondary">Evidentiary Artifacts</span>
          </div>

          <div className="space-y-6">
            <div>
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider block mb-2">
                TrackingTokenDisplay (Tactile Waybill Stub)
              </span>
              <TrackingTokenDisplay
                token="CB-2026-W14-8892"
                timestamp="2026-09-24 08:45 IST"
                summary="Ward 14 (Indiranagar) · 2 Observation Defects"
              />
            </div>

            <div>
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider block mb-2">
                SealMark (Committed / Cryptographic Audit Confirmation)
              </span>
              <SealMark
                authority="BBMP MUNICIPAL JURISDICTION"
                label="OFFICIALLY VERIFIED & COMMITTED"
                hash="7f8a9b2c3d4e5f6a1b2c3d4e5f6a7b8c"
                timestamp="2026-09-24"
              />
            </div>
          </div>
        </section>

        {/* 4. SCORE BREAKDOWN (GLASS-BOX FORMULA) */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">ScoreBreakdown (AHP Glass-Box)</h2>
            <span className="text-xs font-mono text-text-secondary">Real API Response Fixture</span>
          </div>

          <div className="space-y-4">
            <p className="text-xs text-text-secondary">
              Renders exact formula: raw_priority_score * (1 + equity_boost).
              Itemized 5 orthogonal criteria (Severity, Risk, Exposure, Criticality, Urgency).
            </p>

            <ScoreBreakdown
              priority_score={sampleApiResponse.final_priority_score}
              raw_priority_score={sampleApiResponse.raw_priority_score}
              equity_boost={sampleApiResponse.equity_boost}
              confidence_score={sampleApiResponse.confidence_score}
              subscores={sampleApiResponse.subscores}
              weights_used={sampleApiResponse.weights_used}
              ward_name="Ward 14 (Indiranagar)"
              defaultExpanded={true}
            />
          </div>
        </section>

        {/* 5. STATUS TIMELINE (LEAST-ADVANCED-CHILD RULE) */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6 lg:col-span-2">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">StatusTimeline (Least-Advanced-Child Rule)</h2>
            <span className="text-xs font-mono text-text-secondary">FRONTEND_CONTEXT §4 & §7.2</span>
          </div>

          <div className="space-y-4">
            <p className="text-xs text-text-secondary">
              Multi-issue report with 1 Resolved child (Roads) and 1 In-Progress child (Drains).
              The parent report remains strictly in <strong>Partially Resolved / In Progress</strong>, never premature Resolved!
            </p>

            <StatusTimeline observations={sampleObservations} />
          </div>
        </section>

        {/* 6. EVIDENCE PHOTO CARD & BEFORE/AFTER PAIR */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6 lg:col-span-2">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">EvidencePhotoCard & Before/After Pair</h2>
            <span className="text-xs font-mono text-text-secondary">DESIGN.md §7 Photography Grammar</span>
          </div>

          <div className="space-y-4">
            <p className="text-xs text-text-secondary">
              Real 4:3 aspect ratio preserved (never cropped square), mono caption strip below (never overlaid),
              and official redaction badge when PII blurring is applied.
            </p>

            <BeforeAfterPair
              before={{
                src: 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=800&auto=format&fit=crop&q=80',
                alt: 'Deep roadway trench and fractured pavers on 80ft Road',
                coordinates: '12.9716° N, 77.5946° E',
                timestamp: '2026-09-22 14:22 IST',
                caption: 'Defect Report #OBS-001',
                isRedacted: true,
              }}
              after={{
                src: 'https://images.unsplash.com/photo-1584467735871-8e85353a8413?w=800&auto=format&fit=crop&q=80',
                alt: 'Asphalt resurfacing and compacted curb clearance',
                coordinates: '12.9716° N, 77.5946° E',
                timestamp: '2026-09-24 11:05 IST',
                caption: 'Resolution Audit #WO-8912',
                isRedacted: true,
              }}
            />
          </div>
        </section>

        {/* 7. MAPLIBRE LAYER WRAPPERS */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-4 lg:col-span-2">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">MapLibre GIS Layer Wrappers</h2>
            <span className="text-xs font-mono text-text-secondary">DESIGN.md §3.4 & §13</span>
          </div>

          <p className="text-xs text-text-secondary">
            MapLibre layers consume tokens --map-point-radius-incident (6px), --map-point-radius-cluster,
            and --map-line-ward-boundary. Dynamically imported at route level to keep main bundles lean.
          </p>

          <div className="p-4 bg-surface-raised rounded-md border border-border flex items-center justify-between text-xs font-mono">
            <span>WardBoundaryMapLayer · IncidentPointLayer · ClusterLayer</span>
            <span className="text-status-success font-semibold">Active & Dynamically Ready</span>
          </div>

          <WardBoundaryMapLayer layerId="preview-ward" />
          <IncidentPointLayer layerId="preview-incident" />
          <ClusterLayer layerId="preview-cluster" />
        </section>
      </div>
    </div>
  );
};

export const CivicShowcase: React.FC = () => {
  return (
    <ToastProvider>
      <CivicShowcaseInner />
    </ToastProvider>
  );
};
