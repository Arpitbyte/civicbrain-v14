import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  EvidencePhotoCard,
  PriorityChip,
  Badge,
  Button,
  SealMark,
} from '@civicbrain/ui';
import {
  ArrowLeft,
  ArrowRight,
  Clock,
  UserCheck,
  Phone,
  Building2,
  MapPin,
  CheckCircle,
  AlertTriangle,
  FileText,
  RotateCw,
  ExternalLink,
} from 'lucide-react';

export type WorkOrderStatus = 'dispatched' | 'accepted' | 'in_progress' | 'completed' | 'cancelled';

const WO_STEPS: { status: WorkOrderStatus; label: string; labelHi: string }[] = [
  { status: 'dispatched', label: 'Dispatched', labelHi: 'प्रेषित' },
  { status: 'accepted', label: 'Accepted', labelHi: 'स्वीकृत' },
  { status: 'in_progress', label: 'In Progress', labelHi: 'कार्य जारी' },
  { status: 'completed', label: 'Completed', labelHi: 'पूर्ण' },
];

export const WorkOrderDetailView: React.FC = () => {
  const { id = 'WO-2026-8492' } = useParams<{ id: string }>();
  const navigate = useNavigate();

  // Work Order State (5-state lifecycle per SCREEN_SPECS.md §2.11)
  const [status, setStatus] = useState<WorkOrderStatus>('in_progress');
  const [isTransitioning, setIsTransitioning] = useState<boolean>(false);

  // Authentic defect SVG fixtures (4:3 aspect ratio, 0 external photos)
  const ingestPhotoSvg = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600"><rect width="800" height="600" fill="%232b2622"/><path d="M 160 300 Q 240 220 380 250 T 620 320 Q 560 440 380 430 T 160 300 Z" fill="%23171412" stroke="%233f3833" stroke-width="4"/><ellipse cx="370" cy="330" rx="140" ry="70" fill="%230f0d0b"/><text x="40" y="560" fill="%23f97316" font-family="monospace" font-size="20" font-weight="bold">BBMP DEFECT INGEST • WARD 14 INDIRANAGAR</text></svg>`;
  const completedPhotoSvg = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600"><rect width="800" height="600" fill="%231c1917"/><path d="M 140 280 Q 260 210 400 240 T 640 310 Q 580 450 390 440 T 140 280 Z" fill="%23292524" stroke="%2344403c" stroke-width="4"/><polygon points="120,480 680,480 620,530 180,530" fill="%23eab308" opacity="0.3"/><text x="40" y="560" fill="%2322c55e" font-family="monospace" font-size="20" font-weight="bold">COMPLETED COLD-MIX ASPHALT • CREW 04</text></svg>`;

  const handleStatusTransition = async (nextStatus: WorkOrderStatus) => {
    setIsTransitioning(true);
    await new Promise((r) => setTimeout(r, 400));
    setStatus(nextStatus);
    setIsTransitioning(false);
  };

  const getStepState = (stepStatus: WorkOrderStatus) => {
    if (status === 'cancelled') return 'cancelled';
    const stepOrder: WorkOrderStatus[] = ['dispatched', 'accepted', 'in_progress', 'completed'];
    const currentIndex = stepOrder.indexOf(status);
    const stepIndex = stepOrder.indexOf(stepStatus);

    if (stepIndex < currentIndex) return 'completed';
    if (stepIndex === currentIndex) return 'current';
    return 'upcoming';
  };

  return (
    <div
      data-workspace="ops-board"
      className="flex flex-col min-h-screen bg-background text-primary font-ui"
    >
      {/* Top Sticky 64px Context Strip (Same case-file grammar as Incident Detail §2.6 / §2.11) */}
      <header className="sticky top-0 z-sticky h-16 bg-surface border-b-2 border-b-station-600 px-6 flex items-center justify-between shadow-flat">
        <div className="flex items-center gap-4 min-w-0">
          <Link
            to="/ops"
            className="p-2 text-text-secondary hover:text-primary rounded-sm transition-colors"
            title="Return to department queue"
            aria-label="Return to department queue"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>

          <div className="flex items-center gap-2.5 truncate">
            <span className="font-mono text-sm font-bold text-primary tracking-wide">
              {id}
            </span>
            <span className="text-text-secondary text-xs">/</span>
            <span className="text-xs font-semibold text-primary truncate">
              Roads & Infrastructure (PWD)
            </span>
            <Badge variant="neutral" size="sm">
              वार्ड 14 (Indiranagar)
            </Badge>
            <PriorityChip level={3} score={0.78} size="sm" />
          </div>
        </div>

        {/* SLA Countdown Timer (Dominant on Ops Board per SCREEN_SPECS.md §2.10 & §2.11) */}
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded bg-status-warning/15 border border-status-warning/40 text-station-900 font-mono text-xs font-bold">
            <Clock className="w-4 h-4 text-status-warning" />
            <span>SLA REMAINING: 14.5h / 24.0h</span>
          </div>

          <Link
            to="/deck/incidents/INC-8892"
            className="inline-flex items-center gap-1.5 text-xs text-action-primary hover:underline font-mono"
          >
            <span>Linked Case: INC-8892</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </Link>
        </div>
      </header>

      {/* Main 60/40 Evidence/Meta Split Layout (SCREEN_SPECS.md §2.11 & §2.6) */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left 60% = Evidence Photos Stack + Defect Location */}
          <section className="lg:col-span-7 flex flex-col gap-6 order-1">
            <div className="flex items-center justify-between pb-2 border-b border-border">
              <h2 className="text-sm font-bold text-primary uppercase tracking-wider font-mono">
                Field Evidence Documentation
              </h2>
              <span className="text-xs text-text-secondary font-mono">
                2 Observations Attached
              </span>
            </div>

            {/* Ingest Defect Photo Card */}
            <div className="flex flex-col gap-2">
              <span className="text-xs font-semibold uppercase text-status-warning tracking-wider font-mono">
                Observation 1: Citizen Defect Ingest Proof
              </span>
              <EvidencePhotoCard
                src={ingestPhotoSvg}
                alt="Original citizen evidence showing crater in Indiranagar"
                coordinates="12.9784° N, 77.6408° E"
                timestamp="22 Sep, 10:14 AM IST"
                caption="Citizen Waybill Proof (Native 4:3 Aspect)"
                isRedacted={false}
              />
            </div>

            {/* Field Remediation Proof Card (if in_progress or completed) */}
            <div className="flex flex-col gap-2">
              <span className="text-xs font-semibold uppercase text-status-success tracking-wider font-mono">
                Observation 2: Field Worker Remediation Proof
              </span>
              <EvidencePhotoCard
                src={completedPhotoSvg}
                alt="Field remediation proof showing compacted cold-mix asphalt"
                coordinates="12.9785° N, 77.6407° E"
                timestamp="23 Sep, 11:18 AM IST"
                caption="Karmi Sahayak Completion Verification"
                isRedacted={false}
              />
            </div>

            {/* Location & Instructions Card */}
            <div className="p-5 rounded-md bg-surface border border-border shadow-flat flex flex-col gap-3 text-xs">
              <div className="flex items-center gap-2 font-semibold text-primary">
                <MapPin className="w-4 h-4 text-action-primary" />
                <span>Dispatched Location & Landmark</span>
              </div>
              <p className="text-text-secondary font-mono">
                100 Feet Road, 12th Main Junction, near Metro Pillar 42, Indiranagar, Ward 14.
              </p>
              <div className="p-3 bg-surface-raised rounded border border-border flex flex-col gap-1">
                <span className="font-semibold text-primary">Supervisor Dispatch Order:</span>
                <p className="text-text-secondary italic">
                  "Deploy cold-mix asphalt, level crater to road grade, and capture 4:3 completion photo proof."
                </p>
              </div>
            </div>
          </section>

          {/* Right 40% = Meta Side: 5-State Work Order Lifecycle + SLA Timer + Assigned Worker */}
          <aside className="lg:col-span-5 flex flex-col gap-6 order-2">
            {/* 5-State Work Order Timeline (STRICT DO NOT: NEVER REUSE 11-STATE INCIDENT TIMELINE) */}
            <div className="p-5 rounded-md bg-surface border-2 border-border shadow-flat flex flex-col gap-4">
              <div className="flex items-center justify-between pb-2 border-b border-border">
                <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider font-mono">
                  Work Order Lifecycle (5-State Machine)
                </span>
                <Badge
                  variant={status === 'completed' ? 'success' : status === 'cancelled' ? 'destructive' : 'warning'}
                  size="sm"
                >
                  {status.toUpperCase()}
                </Badge>
              </div>

              {/* 5-State Stepper */}
              <div className="flex flex-col gap-3 py-2">
                {WO_STEPS.map((step, idx) => {
                  const stepState = getStepState(step.status);
                  return (
                    <div key={step.status} className="flex items-center gap-3">
                      <div
                        className={`
                          w-6 h-6 rounded-full flex items-center justify-center font-mono text-xs font-bold shrink-0
                          ${stepState === 'completed'
                            ? 'bg-status-success text-white'
                            : stepState === 'current'
                            ? 'bg-action-primary text-station-950 ring-2 ring-action-primary/30'
                            : 'bg-surface-raised border border-border text-text-secondary'}
                        `}
                      >
                        {stepState === 'completed' ? '✓' : idx + 1}
                      </div>

                      <div className="flex flex-col">
                        <span className={`text-xs ${stepState === 'current' ? 'font-bold text-primary' : 'text-text-secondary'}`}>
                          {step.label}
                        </span>
                        <span className="text-[10px] text-text-secondary font-mono">
                          {step.labelHi}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Transition Control Buttons */}
              <div className="flex flex-col gap-2 pt-3 border-t border-border">
                <span className="text-xs font-medium text-text-secondary">
                  Supervisor State Control:
                </span>

                {status === 'dispatched' && (
                  <Button
                    variant="primary"
                    size="md"
                    disabled={isTransitioning}
                    onClick={() => handleStatusTransition('accepted')}
                    className="w-full justify-between"
                    rightIcon={<ArrowRight className="w-4 h-4" />}
                  >
                    <span>Accept Task (स्वीकृत करें)</span>
                  </Button>
                )}

                {status === 'accepted' && (
                  <Button
                    variant="primary"
                    size="md"
                    disabled={isTransitioning}
                    onClick={() => handleStatusTransition('in_progress')}
                    className="w-full justify-between"
                    rightIcon={<ArrowRight className="w-4 h-4" />}
                  >
                    <span>Commence Field Work (कार्य शुरू करें)</span>
                  </Button>
                )}

                {status === 'in_progress' && (
                  <Button
                    variant="primary"
                    size="md"
                    disabled={isTransitioning}
                    onClick={() => handleStatusTransition('completed')}
                    className="w-full justify-between bg-status-success hover:bg-status-success/90 text-white"
                    rightIcon={<CheckCircle className="w-4 h-4" />}
                  >
                    <span>Confirm Completion (कार्य पूर्ण)</span>
                  </Button>
                )}

                {status !== 'completed' && status !== 'cancelled' && (
                  <Button
                    variant="outline"
                    size="sm"
                    disabled={isTransitioning}
                    onClick={() => handleStatusTransition('cancelled')}
                    className="w-full text-status-danger border-status-danger/40 hover:bg-status-danger/10"
                  >
                    <span>Cancel Work Order</span>
                  </Button>
                )}

                {status === 'completed' && (
                  <div className="p-3 rounded bg-status-success/10 border border-status-success text-status-success text-center text-xs font-medium">
                    ✓ Physical repair completed and verified by departmental supervisor.
                  </div>
                )}
              </div>
            </div>

            {/* Assigned Field Personnel Card */}
            <div className="p-5 rounded-md bg-surface border border-border shadow-flat flex flex-col gap-3 text-xs">
              <div className="flex items-center justify-between border-b border-border pb-2">
                <span className="font-semibold text-primary uppercase font-mono text-[11px]">
                  Assigned Karmi Sahayak Personnel
                </span>
                <Badge variant="success" size="sm">
                  Active On-Shift
                </Badge>
              </div>

              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-surface-raised border border-border flex items-center justify-center text-primary font-mono font-bold text-sm">
                  RK
                </div>
                <div className="flex flex-col">
                  <span className="font-bold text-primary text-sm">Ramesh Kumar</span>
                  <span className="text-text-secondary font-mono">PWD Roads Crew 04</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded bg-surface-raised border border-border font-mono text-[11px]">
                <span className="text-text-secondary flex items-center gap-1.5">
                  <Phone className="w-3.5 h-3.5 text-action-primary" />
                  <span>+91 98450 12345</span>
                </span>
                <span className="text-status-success font-semibold">Online Syncing</span>
              </div>
            </div>

            {/* SealMark Official Committal Notice */}
            {status === 'completed' && (
              <SealMark
                authority="BRUHAT BENGALURU MAHANAGARA PALIKE"
                label="WORK ORDER COMPLETION VERIFIED BY SUPERVISOR"
                hash={`0xRESOLVE_${id}`}
                timestamp={new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}
                size="md"
              />
            )}
          </aside>
        </div>
      </main>
    </div>
  );
};
