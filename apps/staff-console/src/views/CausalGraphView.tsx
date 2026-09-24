import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  Button,
  Field,
  Input,
  Select,
  Badge,
  Skeleton,
  ConfidenceBadge,
  PriorityChip,
  Dialog,
} from '@civicbrain/ui';
import {
  GitMerge,
  ArrowRight,
  ArrowLeft,
  Search,
  Plus,
  Network,
  RefreshCw,
  Building2,
  AlertTriangle,
  Info,
  CheckCircle2,
  Share2,
} from 'lucide-react';

interface CausalNode {
  id: string;
  token: string;
  category: string;
  categoryHi: string;
  department: string;
  ward: string;
  status: string;
  priorityScore: number;
  confidence: number;
}

interface CausalEdge {
  id: string;
  fromId: string;
  toId: string;
  relationType: string;
  couplingCoefficient: number;
  confidence: number;
  notes?: string;
}

const SAMPLE_CAUSAL_NETWORK: {
  nodes: CausalNode[];
  edges: CausalEdge[];
} = {
  nodes: [
    {
      id: 'INC-7011',
      token: 'CB-2026-W14-7011',
      category: 'Blocked Stormwater Culvert',
      categoryHi: 'अवरुद्ध बरसाती नाला',
      department: 'SWD',
      ward: 'Ward 14 (Indiranagar)',
      status: 'in_progress',
      priorityScore: 0.88,
      confidence: 0.94,
    },
    {
      id: 'INC-8892',
      token: 'CB-2026-W14-8892',
      category: 'Arterial Road Waterlogging & Potholes',
      categoryHi: 'मुख्य मार्ग जलभराव एवं गड्ढे',
      department: 'ROADS',
      ward: 'Ward 14 (Indiranagar)',
      status: 'in_progress',
      priorityScore: 0.82,
      confidence: 0.91,
    },
    {
      id: 'INC-9102',
      token: 'CB-2026-W14-9102',
      category: 'Foundation Asphalt Erosion',
      categoryHi: 'सड़क आधार कटाव',
      department: 'ROADS',
      ward: 'Ward 14 (Indiranagar)',
      status: 'triaged',
      priorityScore: 0.74,
      confidence: 0.86,
    },
    {
      id: 'INC-9440',
      token: 'CB-2026-W14-9440',
      category: 'Sub-surface Electrical Conduit Short',
      categoryHi: 'भूमिगत बिजली केबल शॉर्ट',
      department: 'LIGHTING',
      ward: 'Ward 14 (Indiranagar)',
      status: 'reported',
      priorityScore: 0.69,
      confidence: 0.78,
    },
  ],
  edges: [
    {
      id: 'EDGE-1',
      fromId: 'INC-7011',
      toId: 'INC-8892',
      relationType: 'INFRASTRUCTURE_FAILURE',
      couplingCoefficient: 0.85,
      confidence: 0.92,
      notes: 'Culvert overflow during monsoon saturated sub-base gravel, creating deep roadway craters.',
    },
    {
      id: 'EDGE-2',
      fromId: 'INC-8892',
      toId: 'INC-9102',
      relationType: 'CASCADE_EROSION',
      couplingCoefficient: 0.76,
      confidence: 0.89,
      notes: 'Vehicle impact on water-filled craters accelerated bituminous stripping.',
    },
    {
      id: 'EDGE-3',
      fromId: 'INC-8892',
      toId: 'INC-9440',
      relationType: 'SECONDARY_HAZARD',
      couplingCoefficient: 0.62,
      confidence: 0.82,
      notes: 'Road surface subsidence pinched underground cable ducting.',
    },
  ],
};

export const CausalGraphView: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const [activeCenterId, setActiveCenterId] = useState<string>('INC-8892');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [isLinkDialogOpen, setIsLinkDialogOpen] = useState<boolean>(false);
  const [newRootId, setNewRootId] = useState<string>('');
  const [newRelationType, setNewRelationType] = useState<string>('INFRASTRUCTURE_FAILURE');
  const [newConfidence, setNewConfidence] = useState<number>(0.85);
  const [newNotes, setNewNotes] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Read URL query parameter
  useEffect(() => {
    const centerParam = searchParams.get('center');
    if (centerParam) {
      setActiveCenterId(centerParam);
    }
  }, [searchParams]);

  const centerNode =
    SAMPLE_CAUSAL_NETWORK.nodes.find((n) => n.id === activeCenterId) ||
    SAMPLE_CAUSAL_NETWORK.nodes[1];

  // Upstream causes: edges where toId === activeCenterId
  const upstreamEdges = SAMPLE_CAUSAL_NETWORK.edges.filter((e) => e.toId === activeCenterId);
  const upstreamNodes = upstreamEdges
    .map((e) => SAMPLE_CAUSAL_NETWORK.nodes.find((n) => n.id === e.fromId))
    .filter(Boolean) as CausalNode[];

  // Downstream symptoms: edges where fromId === activeCenterId
  const downstreamEdges = SAMPLE_CAUSAL_NETWORK.edges.filter((e) => e.fromId === activeCenterId);
  const downstreamNodes = downstreamEdges
    .map((e) => SAMPLE_CAUSAL_NETWORK.nodes.find((n) => n.id === e.toId))
    .filter(Boolean) as CausalNode[];

  const handleSelectCenter = (nodeId: string) => {
    setActiveCenterId(nodeId);
    setSearchParams({ center: nodeId });
  };

  const handleCreateLink = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newRootId) return;

    // Simulate link addition
    setIsLinkDialogOpen(false);
    setNewRootId('');
    setNewNotes('');
  };

  return (
    <div
      data-workspace="city-pulse"
      className="flex flex-col lg:flex-row min-h-screen bg-background text-primary font-ui"
    >
      {/* 280px Left Rail (SCREEN_SPECS.md §2.13) */}
      <aside className="w-full lg:w-72 border-r border-border bg-surface p-5 flex flex-col gap-5 shrink-0 shadow-flat">
        <div className="flex items-center justify-between pb-2 border-b border-border">
          <div className="flex items-center gap-2">
            <Network className="w-5 h-5 text-action-primary" />
            <h2 className="text-sm font-bold text-primary uppercase font-mono tracking-wider">
              Causal Graph
            </h2>
          </div>
          <Badge variant="neutral" size="sm">
            City Pulse
          </Badge>
        </div>

        {/* Incident Quick Search */}
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider font-mono">
            Focus Incident
          </label>
          <div className="relative">
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search token (e.g. W14-8892)..."
              leftIcon={<Search className="w-3.5 h-3.5 text-text-secondary" />}
              size="sm"
            />
          </div>
        </div>

        {/* Incident List in Network */}
        <div className="flex flex-col gap-2">
          <span className="text-[11px] font-mono text-text-secondary uppercase">
            Incidents in Local Topology ({SAMPLE_CAUSAL_NETWORK.nodes.length})
          </span>

          <div className="flex flex-col gap-1.5">
            {SAMPLE_CAUSAL_NETWORK.nodes
              .filter(
                (n) =>
                  n.token.toLowerCase().includes(searchQuery.toLowerCase()) ||
                  n.category.toLowerCase().includes(searchQuery.toLowerCase())
              )
              .map((node) => {
                const isSelected = node.id === activeCenterId;
                return (
                  <button
                    key={node.id}
                    type="button"
                    onClick={() => handleSelectCenter(node.id)}
                    className={`
                      p-2.5 rounded-md border text-left flex flex-col gap-1 transition-all text-xs
                      ${isSelected
                        ? 'bg-action-primary/10 border-action-primary text-primary font-medium shadow-xs'
                        : 'bg-surface hover:bg-surface-raised border-border text-text-secondary'}
                    `}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-mono font-bold">{node.token}</span>
                      <span className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-surface border border-border">
                        {node.department}
                      </span>
                    </div>
                    <span className="text-primary truncate">{node.category}</span>
                  </button>
                );
              })}
          </div>
        </div>

        {/* Causal Impact Metrics Card */}
        <div className="p-3.5 rounded-md bg-surface-raised border border-border flex flex-col gap-2.5 text-xs font-mono">
          <span className="text-text-secondary uppercase text-[11px] font-semibold">
            Causal Topological Impact
          </span>

          <div className="flex items-center justify-between">
            <span className="text-text-secondary">Downstream Symptoms:</span>
            <span className="font-bold text-primary">{downstreamNodes.length} Cases</span>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-text-secondary">Root Cause Priority Boost:</span>
            <span className="font-bold text-action-primary">+{(downstreamNodes.length * 0.12).toFixed(2)}</span>
          </div>

          <p className="text-[11px] text-text-secondary font-sans leading-normal pt-1 border-t border-border">
            Resolving the upstream root cause eliminates cascade pressure across connected symptom incidents.
          </p>
        </div>

        {/* Action: Link New Cause */}
        <div className="pt-2">
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => setIsLinkDialogOpen(true)}
            leftIcon={<Plus className="w-3.5 h-3.5" />}
            className="w-full justify-center"
          >
            Link New Root Cause
          </Button>
        </div>
      </aside>

      {/* Main Directed Graph Canvas (SVG Canvas per SCREEN_SPECS.md §2.13) */}
      <main className="flex-1 p-6 flex flex-col gap-6 overflow-x-auto">
        {/* Canvas Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-border gap-3">
          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-semibold text-action-primary uppercase tracking-wider">
                TOPOLOGICAL CAUSAL GRAPH
              </span>
              <span className="text-text-secondary text-xs">•</span>
              <span className="text-xs text-text-secondary font-mono">
                Directed Acyclic Ingestion
              </span>
            </div>
            <h1 className="text-xl font-bold text-primary tracking-tight">
              Root-Cause & Downstream Symptom Graph
            </h1>
          </div>

          <div className="flex items-center gap-2">
            <Badge variant="neutral" size="sm">
              Upstream: {upstreamNodes.length}
            </Badge>
            <Badge variant="neutral" size="sm">
              Downstream: {downstreamNodes.length}
            </Badge>
          </div>
        </div>

        {/* Directed Graph Container */}
        <div className="relative min-h-[480px] w-full rounded-md border border-border bg-station-950 p-6 flex items-center justify-between gap-8 overflow-x-auto shadow-flat select-none">
          {/* Subtle Grid Background */}
          <div
            className="absolute inset-0 opacity-15 pointer-events-none"
            style={{
              backgroundImage: 'radial-gradient(var(--border) 1px, transparent 1px)',
              backgroundSize: '24px 24px',
            }}
          />

          {/* LEFT COLUMN: Upstream Root Causes */}
          <div className="flex flex-col gap-6 z-10 w-72 shrink-0">
            <div className="flex items-center gap-1.5 text-xs font-mono font-semibold uppercase tracking-wider text-text-secondary border-b border-border pb-1">
              <ArrowLeft className="w-3.5 h-3.5 text-status-warning" />
              <span>Upstream Causes (कारण)</span>
            </div>

            {upstreamNodes.length === 0 ? (
              <div className="p-4 rounded-md border border-dashed border-border text-center text-xs text-text-secondary">
                No upstream causes linked. This incident is currently classified as a root-level event.
              </div>
            ) : (
              upstreamNodes.map((node) => (
                <div
                  key={node.id}
                  onClick={() => handleSelectCenter(node.id)}
                  className="
                    p-4 rounded-md bg-surface border-2 border-status-warning/40 hover:border-status-warning
                    shadow-flat cursor-pointer transition-all duration-fast flex flex-col gap-2
                    hover:translate-x-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus
                  "
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleSelectCenter(node.id);
                  }}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold text-primary">{node.token}</span>
                    <Badge variant="warning" size="sm">{node.department}</Badge>
                  </div>
                  <span className="text-xs font-semibold text-primary">{node.category}</span>
                  <div className="flex items-center justify-between text-[11px] font-mono text-text-secondary pt-1 border-t border-border">
                    <span>Priority: {node.priorityScore.toFixed(2)}</span>
                    <span className="text-action-primary">Coupling: 85%</span>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* CENTER: Selected Incident (Focus Node) */}
          <div className="flex flex-col items-center justify-center z-10 w-80 shrink-0">
            <div className="w-full p-5 rounded-lg bg-surface border-2 border-action-primary shadow-lifted flex flex-col gap-3 ring-4 ring-action-primary/10">
              <div className="flex items-center justify-between border-b border-border pb-2">
                <span className="text-[11px] font-mono font-bold text-action-primary uppercase tracking-wider">
                  CURRENT FOCAL INCIDENT
                </span>
                <PriorityChip level={4} score={centerNode.priorityScore} size="sm" />
              </div>

              <div className="flex flex-col gap-1">
                <span className="font-mono font-bold text-sm text-primary">{centerNode.token}</span>
                <h3 className="font-semibold text-sm text-primary leading-tight">{centerNode.category}</h3>
                <span className="text-xs text-text-secondary">{centerNode.categoryHi}</span>
              </div>

              <div className="p-2.5 rounded bg-surface-raised border border-border flex items-center justify-between text-xs font-mono">
                <span className="text-text-secondary">{centerNode.ward}</span>
                <span className="text-primary font-bold">{centerNode.department}</span>
              </div>

              <div className="flex items-center justify-between pt-1 text-xs">
                <ConfidenceBadge confidence_score={centerNode.confidence} size="sm" />
                <button
                  type="button"
                  onClick={() => navigate(`/deck/incidents/${centerNode.id}`)}
                  className="inline-flex items-center gap-1 font-mono text-[11px] text-action-primary hover:underline"
                >
                  <span>Open Full Case</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            </div>
          </div>

          {/* RIGHT COLUMN: Downstream Symptoms */}
          <div className="flex flex-col gap-6 z-10 w-72 shrink-0">
            <div className="flex items-center gap-1.5 text-xs font-mono font-semibold uppercase tracking-wider text-text-secondary border-b border-border pb-1">
              <span>Downstream Symptoms (लक्षण)</span>
              <ArrowRight className="w-3.5 h-3.5 text-action-primary" />
            </div>

            {downstreamNodes.length === 0 ? (
              <div className="p-4 rounded-md border border-dashed border-border text-center text-xs text-text-secondary">
                No downstream symptoms registered for this case.
              </div>
            ) : (
              downstreamNodes.map((node) => (
                <div
                  key={node.id}
                  onClick={() => handleSelectCenter(node.id)}
                  className="
                    p-4 rounded-md bg-surface border border-border hover:border-action-primary
                    shadow-flat cursor-pointer transition-all duration-fast flex flex-col gap-2
                    hover:-translate-x-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus
                  "
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleSelectCenter(node.id);
                  }}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold text-primary">{node.token}</span>
                    <Badge variant="neutral" size="sm">{node.department}</Badge>
                  </div>
                  <span className="text-xs font-semibold text-primary">{node.category}</span>
                  <div className="flex items-center justify-between text-[11px] font-mono text-text-secondary pt-1 border-t border-border">
                    <span>Priority: {node.priorityScore.toFixed(2)}</span>
                    <span className="text-action-primary">Impact Link</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </main>

      {/* Dialog for Manual Causal Link Creation (SCREEN_SPECS.md §2.13) */}
      <Dialog
        open={isLinkDialogOpen}
        onOpenChange={setIsLinkDialogOpen}
        title="Establish Causal Relationship"
        description="Link an upstream root cause defect to this incident to calibrate priority propagation."
      >
        <form onSubmit={handleCreateLink} className="flex flex-col gap-4 pt-2 font-ui">
          <Field
            id="upstream-select"
            label="Upstream Root Cause Incident"
            required
            helperText="The physical defect responsible for creating or compounding the symptom."
          >
            <select
              id="upstream-select"
              value={newRootId}
              onChange={(e) => setNewRootId(e.target.value)}
              className="w-full p-2 bg-surface border border-border rounded text-sm text-primary outline-none focus:ring-1 focus:ring-focus"
            >
              <option value="">Select an upstream incident...</option>
              <option value="INC-7011">CB-2026-W14-7011 · Blocked Stormwater Culvert (SWD)</option>
              <option value="INC-6120">CB-2026-W14-6120 · High-Pressure Water Leak (BWSSB)</option>
            </select>
          </Field>

          <Field
            id="relation-type"
            label="Causal Relation Classification"
            required
          >
            <select
              id="relation-type"
              value={newRelationType}
              onChange={(e) => setNewRelationType(e.target.value)}
              className="w-full p-2 bg-surface border border-border rounded text-sm text-primary outline-none focus:ring-1 focus:ring-focus"
            >
              <option value="INFRASTRUCTURE_FAILURE">Direct Infrastructure Failure</option>
              <option value="CASCADE_EROSION">Cascade Erosion & Subsidence</option>
              <option value="SECONDARY_HAZARD">Secondary Utility Hazard</option>
            </select>
          </Field>

          <Field
            id="causal-notes"
            label="Supervisory Causal Mechanism Notes"
            helperText="Document physical evidence supporting the causal connection."
          >
            <Input
              id="causal-notes"
              value={newNotes}
              onChange={(e) => setNewNotes(e.target.value)}
              placeholder="e.g. Chronic culvert overflow breached the sub-base layer under the roadway."
              className="text-sm"
            />
          </Field>

          <div className="flex justify-end gap-3 pt-3 border-t border-border">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setIsLinkDialogOpen(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              size="sm"
              disabled={!newRootId}
            >
              Establish Link
            </Button>
          </div>
        </form>
      </Dialog>
    </div>
  );
};
