import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  BeforeAfterPair,
  Button,
  Field,
  Textarea,
  SealMark,
  TrackingTokenDisplay,
} from '@civicbrain/ui';
import {
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
  ShieldAlert,
  RotateCw,
} from 'lucide-react';

export const ResolutionDisputeView: React.FC = () => {
  const { token = 'CB-2026-W14-8892' } = useParams<{ token: string }>();
  const navigate = useNavigate();

  const [disputeReason, setDisputeReason] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);
  const [status, setStatus] = useState<'idle' | 'submitting' | 'disputed' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Authentic defect SVG before/after fixtures (4:3 aspect ratio, 0 external photos)
  const beforePhotoSvg = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600"><rect width="800" height="600" fill="%232b2622"/><path d="M 160 300 Q 240 220 380 250 T 620 320 Q 560 440 380 430 T 160 300 Z" fill="%23171412" stroke="%233f3833" stroke-width="4"/><ellipse cx="370" cy="330" rx="140" ry="70" fill="%230f0d0b"/><text x="40" y="560" fill="%23f97316" font-family="monospace" font-size="20" font-weight="bold">INGEST DEFECT • WARD 14 INDIRANAGAR</text></svg>`;
  const afterPhotoSvg = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600"><rect width="800" height="600" fill="%231c1917"/><path d="M 140 280 Q 260 210 400 240 T 640 310 Q 580 450 390 440 T 140 280 Z" fill="%23292524" stroke="%2344403c" stroke-width="4"/><polygon points="120,480 680,480 620,530 180,530" fill="%23eab308" opacity="0.3"/><text x="40" y="560" fill="%2322c55e" font-family="monospace" font-size="20" font-weight="bold">REPAIRED & COMPACTED • PWD CREW 04</text></svg>`;

  const handleSubmitDispute = async (e: React.FormEvent) => {
    e.preventDefault();
    const cleanReason = disputeReason.trim();
    if (!cleanReason || cleanReason.length < 10) {
      setValidationError('Please explain specifically why the work is unsatisfactory (minimum 10 characters).');
      return;
    }
    setValidationError(null);
    setStatus('submitting');
    setErrorMessage(null);

    try {
      // Simulate real POST /v1/intake/reports/{tracking_token}/dispute with payload { reason }
      await new Promise((resolve) => setTimeout(resolve, 600));
      setStatus('disputed');
    } catch (err: any) {
      setStatus('error');
      setErrorMessage(err?.message || 'Failed to submit dispute. Please retry.');
    }
  };

  // SUCCESS / APPEALED STATE
  if (status === 'disputed') {
    return (
      <div className="w-full max-w-[640px] mx-auto py-6 sm:py-8 flex flex-col gap-6 font-ui animate-in fade-in duration-deliberate">
        {/* Expressive SealMark Moment */}
        <SealMark
          authority="MUNICIPAL OMBUDSMAN & ZONAL SUPERVISION"
          label="DISPUTE REGISTERED • CASE STATUS: APPEALED"
          hash={`0x${Math.random().toString(16).substring(2, 10).toUpperCase()}...APPEALED`}
          timestamp={new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}
          size="lg"
        />

        <div className="flex flex-col gap-2 text-center items-center">
          <h2 className="text-2xl font-bold text-primary tracking-tight">
            Dispute Escalated for Review
          </h2>
          <p className="text-sm text-text-secondary max-w-md leading-relaxed">
            Your dispute has been logged. Per municipal operational rules, this case has been moved back from resolved to <strong className="text-status-danger font-mono">APPEALED</strong>. A senior zonal supervisor will perform a field reinspection.
          </p>
        </div>

        <TrackingTokenDisplay
          token={token}
          timestamp={new Date().toLocaleDateString('en-IN', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
          })}
          summary="Ward 14 · Escalated to Zonal Supervisor"
          size="md"
        />

        <div className="flex justify-center pt-2">
          <Button
            type="button"
            variant="primary"
            size="lg"
            onClick={() => navigate(`/track/${encodeURIComponent(token)}`)}
            rightIcon={<ArrowRight className="w-4 h-4" />}
          >
            Return to Case Timeline
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-[720px] mx-auto py-4 sm:py-6 flex flex-col gap-6 font-ui">
      {/* Top Header Strip */}
      <div className="flex flex-col gap-2 border-b border-border pb-3">
        <Link
          to={`/track/${encodeURIComponent(token)}/confirm`}
          className="inline-flex items-center gap-1.5 text-xs font-medium text-text-secondary hover:text-primary transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to resolution review</span>
        </Link>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-status-danger" />
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-primary">
              Dispute Resolution (विवाद दर्ज करें)
            </h1>
          </div>
          <span className="font-mono text-xs px-2.5 py-1 rounded bg-surface-raised border border-border text-primary font-semibold">
            {token}
          </span>
        </div>

        <p className="text-xs sm:text-sm text-text-secondary leading-normal">
          If the defect was not resolved, only partially fixed, or substandard materials were used, document your dispute below. This immediately re-opens the case for supervisory audit.
        </p>
      </div>

      {/* Side-by-Side Before / After Pair */}
      <div className="bg-surface p-4 sm:p-5 rounded-md border border-border shadow-flat">
        <BeforeAfterPair
          title="Field Remediation Proof of Work"
          before={{
            src: beforePhotoSvg,
            alt: "Original reported pothole defect",
            coordinates: "12.9784° N, 77.6408° E",
            timestamp: "22 Sep, 10:14 AM",
            caption: "Citizen Ingest Proof",
            isRedacted: false,
          }}
          after={{
            src: afterPhotoSvg,
            alt: "Completed roadway asphalt repair by field crew",
            coordinates: "12.9785° N, 77.6407° E",
            timestamp: "23 Sep, 04:30 PM",
            caption: "Field Worker Completion Proof",
            isRedacted: false,
          }}
        />
      </div>

      {/* Dispute Reason Form */}
      <form onSubmit={handleSubmitDispute} className="flex flex-col gap-4 p-5 rounded-md bg-surface border border-border shadow-flat">
        <Field
          id="dispute-reason"
          label="Why is this resolution unsatisfactory?"
          required
          helperText="Please be specific. E.g. Pothole filled with loose uncompacted gravel, sidewalk still blocked, debris left behind."
          errorMessage={validationError ?? undefined}
        >
          <Textarea
            id="dispute-reason"
            rows={4}
            value={disputeReason}
            onChange={(e) => {
              setDisputeReason(e.target.value);
              if (validationError) setValidationError(null);
            }}
            placeholder="e.g. The field worker only filled the center of the crater with loose gravel without asphalt binding. The edges are broken and hazardous."
            className="text-sm leading-relaxed"
            autoFocus
          />
        </Field>

        <div className="flex items-center justify-between text-xs font-mono text-text-secondary">
          <span>Minimum 10 characters</span>
          <span>{disputeReason.length} characters</span>
        </div>

        {/* Error state */}
        {status === 'error' && (
          <div className="p-3.5 rounded-md bg-status-danger/10 border border-status-danger text-status-danger text-xs">
            {errorMessage}
          </div>
        )}

        <div className="flex flex-col sm:flex-row items-center gap-3 pt-3 border-t border-border">
          <Button
            type="submit"
            variant="primary"
            size="lg"
            className="w-full sm:flex-1 bg-status-danger hover:bg-status-danger/90 text-white"
            disabled={status === 'submitting'}
            leftIcon={status === 'submitting' ? <RotateCw className="w-4 h-4 animate-spin" /> : <AlertTriangle className="w-4 h-4" />}
          >
            {status === 'submitting' ? 'Submitting Dispute...' : 'Escalate Dispute to Supervisor'}
          </Button>

          <Button
            type="button"
            variant="outline"
            size="lg"
            className="w-full sm:flex-1"
            onClick={() => navigate(`/track/${encodeURIComponent(token)}/confirm`)}
          >
            Cancel & Return
          </Button>
        </div>
      </form>
    </div>
  );
};
