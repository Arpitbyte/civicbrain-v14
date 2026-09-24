import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import {
  Button,
  Field,
  Input,
  Textarea,
  Badge,
  PriorityChip,
  SealMark,
} from '@civicbrain/ui';
import {
  Send,
  ArrowLeft,
  ArrowRight,
  Clock,
  UserCheck,
  UserX,
  Building2,
  FileText,
  ShieldCheck,
  RotateCw,
} from 'lucide-react';

interface FieldWorker {
  id: string;
  name: string;
  phone: string;
  status: 'available' | 'on_shift' | 'offline';
  crew: string;
}

const DEPARTMENT_WORKERS: Record<string, FieldWorker[]> = {
  ROADS: [
    { id: 'wkr-04', name: 'Ramesh Kumar', phone: '+91 98450 12345', status: 'available', crew: 'Roads Crew 04 (Cold-Mix Patching)' },
    { id: 'wkr-02', name: 'Suresh Gowda', phone: '+91 98450 67890', status: 'on_shift', crew: 'Roads Crew 02 (Roller Team)' },
  ],
  SWM: [
    { id: 'wkr-swm-1', name: 'Manjunath B.', phone: '+91 98450 23456', status: 'available', crew: 'SWM Ward 14 Tipper Crew' },
  ],
  SWD: [], // Deliberately empty department to test the mandatory empty-worker non-dead-end UI!
  LIGHTING: [
    { id: 'wkr-lt-1', name: 'Anand Prakash', phone: '+91 98450 34567', status: 'available', crew: 'BESCOM / BBMP Lighting Van 1' },
  ],
  WATER: [
    { id: 'wkr-wtr-1', name: 'Venkatesh R.', phone: '+91 98450 45678', status: 'available', crew: 'BWSSB Rapid Repair Crew' },
  ],
};

const SERVICE_TIME_PRIORS: Record<string, { targetHours: number; confidence: number }> = {
  ROADS: { targetHours: 24.0, confidence: 0.92 },
  SWM: { targetHours: 8.0, confidence: 0.95 },
  SWD: { targetHours: 12.0, confidence: 0.88 },
  LIGHTING: { targetHours: 16.0, confidence: 0.90 },
  WATER: { targetHours: 6.0, confidence: 0.94 },
};

export const WorkOrderDispatchView: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const incidentId = searchParams.get('incidentId') || 'INC-8892';
  const defaultDept = searchParams.get('department') || 'ROADS';

  const [selectedDept, setSelectedDept] = useState<string>(defaultDept);
  const [selectedWorkerId, setSelectedWorkerId] = useState<string>('');
  const [dispatchNotes, setDispatchNotes] = useState<string>(
    'Deploy cold-mix asphalt, level crater to road grade, and capture 4:3 completion photo proof.'
  );
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [submittedOrder, setSubmittedOrder] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const availableWorkers = DEPARTMENT_WORKERS[selectedDept] || [];
  const prior = SERVICE_TIME_PRIORS[selectedDept] || { targetHours: 24.0, confidence: 0.90 };

  useEffect(() => {
    // Select first available worker if present
    if (availableWorkers.length > 0) {
      setSelectedWorkerId(availableWorkers[0].id);
    } else {
      setSelectedWorkerId('');
    }
  }, [selectedDept]);

  const handleDispatch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedWorkerId && availableWorkers.length > 0) return;

    setIsSubmitting(true);
    setError(null);

    try {
      // Simulate real POST /v1/dispatch/work-orders
      await new Promise((resolve) => setTimeout(resolve, 500));
      const newWoId = `WO-2026-${Math.floor(1000 + Math.random() * 9000)}`;
      setSubmittedOrder(newWoId);
      setIsSubmitting(false);
    } catch (err: any) {
      setError(err?.message || 'Failed to dispatch work order');
      setIsSubmitting(false);
    }
  };

  // SUCCESS STATE: Verification SealMark & Work Order Waybill
  if (submittedOrder) {
    return (
      <div
        data-workspace="command-deck"
        className="w-full max-w-[640px] mx-auto py-8 px-4 flex flex-col gap-6 font-ui animate-in fade-in duration-deliberate"
      >
        <SealMark
          authority="BRUHAT BENGALURU MAHANAGARA PALIKE"
          label="OFFICIAL WORK ORDER DISPATCH AUTHORIZED"
          hash={`0xDISPATCH_${submittedOrder}`}
          timestamp={new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}
          size="lg"
        />

        <div className="flex flex-col gap-2 text-center items-center">
          <h2 className="text-2xl font-bold text-primary tracking-tight">
            Work Order Dispatched
          </h2>
          <p className="text-sm text-text-secondary max-w-md leading-relaxed">
            The task has been dispatched to Karmi Sahayak field personnel. The field crew will receive the order and GPS coordinates in their offline queue.
          </p>
        </div>

        <div className="p-5 rounded-md bg-surface border border-border shadow-flat flex flex-col gap-3 font-mono text-xs">
          <div className="flex items-center justify-between border-b border-border pb-2">
            <span className="text-text-secondary uppercase">Work Order Number</span>
            <span className="font-bold text-primary text-sm">{submittedOrder}</span>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-text-secondary">Assigned Personnel</span>
            <span className="text-primary font-semibold">
              {availableWorkers.find((w) => w.id === selectedWorkerId)?.name || 'Unassigned Queue'}
            </span>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-text-secondary">SLA Target Completion</span>
            <span className="text-action-primary font-bold">{prior.targetHours} Hours</span>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center gap-3 pt-2">
          <Button
            type="button"
            variant="primary"
            size="lg"
            className="w-full sm:flex-1"
            onClick={() => navigate('/deck')}
            rightIcon={<ArrowRight className="w-4 h-4" />}
          >
            Return to Command Queue
          </Button>

          <Button
            type="button"
            variant="outline"
            size="lg"
            className="w-full sm:flex-1"
            onClick={() => navigate(`/ops`)}
          >
            View Department Queue
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div
      data-workspace="command-deck"
      className="w-full max-w-[640px] mx-auto py-6 px-4 flex flex-col gap-6 font-ui"
    >
      {/* Top Header */}
      <div className="flex flex-col gap-2 border-b border-border pb-3">
        <Link
          to="/deck"
          className="inline-flex items-center gap-1.5 text-xs font-medium text-text-secondary hover:text-primary transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Cancel & return to incident queue</span>
        </Link>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Send className="w-5 h-5 text-action-primary" />
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-primary">
              Work Order Dispatch Slip (कार्य आदेश प्रेषण)
            </h1>
          </div>
          <Badge variant="neutral" size="sm">
            Case #{incidentId}
          </Badge>
        </div>

        <p className="text-xs sm:text-sm text-text-secondary leading-normal">
          Assign physical field remediation orders to active municipal crews with SLA targets.
        </p>
      </div>

      {/* Dispatch Slip Form (SCREEN_SPECS.md §2.9: simple, fast form, not a wizard) */}
      <form onSubmit={handleDispatch} className="p-5 sm:p-6 rounded-md bg-surface border border-border shadow-flat flex flex-col gap-5">
        {/* Incident Summary Box */}
        <div className="p-3.5 rounded bg-surface-raised border border-border flex items-center justify-between">
          <div className="flex flex-col gap-0.5 text-xs">
            <span className="font-semibold text-primary">Arterial Road Pothole (Ward 14)</span>
            <span className="text-text-secondary font-mono text-[11px]">Token: CB-2026-W14-8892 · Indiranagar 100ft Rd</span>
          </div>
          <PriorityChip level={3} score={0.78} size="sm" />
        </div>

        {/* Department Selector */}
        <Field
          id="dept-select"
          label="Responsible Municipal Department"
          required
          helperText="Determines crew jurisdictional scope and SLA repair baselines."
        >
          <select
            id="dept-select"
            value={selectedDept}
            onChange={(e) => setSelectedDept(e.target.value)}
            className="w-full text-sm bg-surface border border-border rounded-sm py-2 px-3 font-medium text-primary outline-none focus:ring-1 focus:ring-focus font-ui"
          >
            <option value="ROADS">Roads & Infrastructure (PWD)</option>
            <option value="SWM">Solid Waste Management (SWM)</option>
            <option value="SWD">Stormwater Drains (SWD)</option>
            <option value="LIGHTING">Electrical & Street Lighting</option>
            <option value="WATER">Water Supply & Sewerage Board</option>
          </select>
        </Field>

        {/* SLA Target (Read-Only from Service-Time Priors per SCREEN_SPECS.md §2.9) */}
        <div className="p-3.5 rounded bg-surface-raised border border-border flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-action-primary" />
            <div className="flex flex-col">
              <span className="text-xs font-semibold text-primary">SLA Target Resolution Time</span>
              <span className="text-[11px] font-mono text-text-secondary">
                Calibrated from municipal historical priors (Confidence: {(prior.confidence * 100).toFixed(0)}%)
              </span>
            </div>
          </div>
          <span className="font-mono font-bold text-sm text-action-primary">
            {prior.targetHours} Hours
          </span>
        </div>

        {/* Field Worker Selection with STRICT EMPTY-STATE NEXT STEP (SCREEN_SPECS.md §2.9) */}
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-medium text-primary">
            Assigned Field Worker (कर्मी चयन)
          </label>

          {availableWorkers.length === 0 ? (
            /* CRITICAL RULE: Empty field-worker list needs a real next step, not a dead end */
            <div className="p-4 rounded-md bg-status-warning/10 border border-status-warning text-status-warning flex flex-col gap-3">
              <div className="flex items-center gap-2 text-xs font-bold">
                <UserX className="w-4 h-4 shrink-0" />
                <span>No Available Field Workers in {selectedDept}</span>
              </div>
              <p className="text-xs text-text-primary leading-normal">
                There are currently zero active field personnel registered on shift for this department. Dispatch cannot proceed until field workers are allocated.
              </p>
              <div className="pt-1">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('/control/staff')}
                  leftIcon={<Building2 className="w-3.5 h-3.5" />}
                  className="bg-surface text-primary border-border"
                >
                  Open Staff Directory & Onboard Personnel →
                </Button>
              </div>
            </div>
          ) : (
            <div className="flex flex-col gap-2">
              {availableWorkers.map((worker) => {
                const isSelected = selectedWorkerId === worker.id;
                return (
                  <button
                    key={worker.id}
                    type="button"
                    onClick={() => setSelectedWorkerId(worker.id)}
                    className={`
                      p-3 rounded-md border text-left flex items-center justify-between transition-colors
                      ${isSelected
                        ? 'bg-action-primary/10 border-action-primary text-primary font-medium'
                        : 'bg-surface hover:bg-surface-raised border-border text-text-secondary'}
                    `}
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-7 h-7 rounded-full bg-surface-raised border border-border flex items-center justify-center text-primary font-mono text-xs font-bold">
                        {worker.name.charAt(0)}
                      </div>
                      <div className="flex flex-col">
                        <span className="text-xs font-semibold text-primary">{worker.name}</span>
                        <span className="text-[11px] text-text-secondary font-mono">{worker.crew}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <Badge variant={worker.status === 'available' ? 'success' : 'neutral'} size="sm">
                        {worker.status}
                      </Badge>
                      {isSelected && <UserCheck className="w-4 h-4 text-action-primary" />}
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Dispatch Order Instructions */}
        <Field
          id="dispatch-notes"
          label="Field Operations Instructions & Safety Orders"
          helperText="Delivered to Karmi Sahayak mobile app along with navigation coordinates."
        >
          <Textarea
            id="dispatch-notes"
            rows={3}
            value={dispatchNotes}
            onChange={(e) => setDispatchNotes(e.target.value)}
            className="text-xs leading-relaxed"
          />
        </Field>

        {/* Error notice */}
        {error && (
          <div className="p-3 bg-status-danger/10 border border-status-danger text-status-danger text-xs rounded-md">
            {error}
          </div>
        )}

        {/* Submit Actions */}
        <div className="flex items-center justify-between pt-3 border-t border-border">
          <Button
            type="button"
            variant="outline"
            size="md"
            onClick={() => navigate('/deck')}
          >
            Cancel
          </Button>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            disabled={isSubmitting || availableWorkers.length === 0}
            leftIcon={isSubmitting ? <RotateCw className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          >
            {isSubmitting ? 'Issuing Dispatch...' : 'Issue Dispatch Order'}
          </Button>
        </div>
      </form>
    </div>
  );
};
