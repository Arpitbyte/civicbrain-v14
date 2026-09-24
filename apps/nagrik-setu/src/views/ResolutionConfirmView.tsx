import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  BeforeAfterPair,
  Button,
  SealMark,
  TrackingTokenDisplay,
} from '@civicbrain/ui';
import {
  CheckCircle,
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
  ShieldCheck,
  RotateCw,
} from 'lucide-react';

export const ResolutionConfirmView: React.FC = () => {
  const { token = 'CB-2026-W14-8892' } = useParams<{ token: string }>();
  const navigate = useNavigate();

  const [status, setStatus] = useState<'idle' | 'submitting' | 'confirmed' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Authentic defect SVG before/after fixtures (4:3 aspect ratio, 0 external photos)
  const beforePhotoSvg = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600"><rect width="800" height="600" fill="%232b2622"/><path d="M 160 300 Q 240 220 380 250 T 620 320 Q 560 440 380 430 T 160 300 Z" fill="%23171412" stroke="%233f3833" stroke-width="4"/><ellipse cx="370" cy="330" rx="140" ry="70" fill="%230f0d0b"/><text x="40" y="560" fill="%23f97316" font-family="monospace" font-size="20" font-weight="bold">INGEST DEFECT • WARD 14 INDIRANAGAR</text></svg>`;
  const afterPhotoSvg = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600"><rect width="800" height="600" fill="%231c1917"/><path d="M 140 280 Q 260 210 400 240 T 640 310 Q 580 450 390 440 T 140 280 Z" fill="%23292524" stroke="%2344403c" stroke-width="4"/><polygon points="120,480 680,480 620,530 180,530" fill="%23eab308" opacity="0.3"/><text x="40" y="560" fill="%2322c55e" font-family="monospace" font-size="20" font-weight="bold">REPAIRED & COMPACTED • PWD CREW 04</text></svg>`;

  const handleConfirm = async () => {
    setStatus('submitting');
    setErrorMessage(null);
    try {
      // Simulate real POST /v1/intake/reports/{tracking_token}/confirm call
      await new Promise((resolve) => setTimeout(resolve, 600));
      setStatus('confirmed');
    } catch (err: any) {
      setStatus('error');
      setErrorMessage(err?.message || 'Failed to submit confirmation. Please retry.');
    }
  };

  // SUCCESS / CONFIRMED STATE
  if (status === 'confirmed') {
    return (
      <div className="w-full max-w-[640px] mx-auto py-6 sm:py-8 flex flex-col gap-6 font-ui animate-in fade-in duration-deliberate">
        {/* Expressive SealMark Moment */}
        <SealMark
          authority="BRUHAT BENGALURU MAHANAGARA PALIKE"
          label="CITIZEN SATISFACTION CONFIRMED • CASE CLOSED"
          hash={`0x${Math.random().toString(16).substring(2, 10).toUpperCase()}...CONFIRMED`}
          timestamp={new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}
          size="lg"
        />

        <div className="flex flex-col gap-2 text-center items-center">
          <h2 className="text-2xl font-bold text-primary tracking-tight">
            Resolution Confirmed
          </h2>
          <p className="text-sm text-text-secondary max-w-md leading-relaxed">
            Thank you for verifying the remediation work. Your confirmation has been committed to the municipal public ledger and the work order is formally concluded.
          </p>
        </div>

        <TrackingTokenDisplay
          token={token}
          timestamp={new Date().toLocaleDateString('en-IN', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
          })}
          summary="Ward 14 · Roads & Drains (Verified Resolved)"
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
            Back to Case Timeline
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
          to={`/track/${encodeURIComponent(token)}`}
          className="inline-flex items-center gap-1.5 text-xs font-medium text-text-secondary hover:text-primary transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to report details</span>
        </Link>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-action-primary" />
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-primary">
              Verification Desk (सत्यापन)
            </h1>
          </div>
          <span className="font-mono text-xs px-2.5 py-1 rounded bg-surface-raised border border-border text-primary font-semibold">
            {token}
          </span>
        </div>

        <p className="text-xs sm:text-sm text-text-secondary leading-normal">
          Review the field worker's photographic proof of completion. As the filing citizen, your judgment determines whether this case can be formally closed.
        </p>
      </div>

      {/* Side-by-Side Before / After Pair per SCREEN_SPECS.md §2.4 & DESIGN.md §7 */}
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

      {/* Field Worker Remarks Strip */}
      <div className="p-4 rounded-md bg-surface-raised border border-border flex flex-col gap-1 text-xs">
        <span className="font-mono font-semibold text-text-secondary uppercase text-[11px]">
          PWD Crew 04 Resolution Notes:
        </span>
        <p className="text-primary italic">
          "Asphalt cold-mix patched and roller-compacted across 2.4m x 1.8m crater. Surface level restored to grade."
        </p>
      </div>

      {/* Error state if submission failed */}
      {status === 'error' && (
        <div className="p-4 rounded-md bg-status-danger/10 border border-status-danger text-status-danger flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5" />
          <div className="flex flex-col gap-1 text-xs">
            <span className="font-bold">Confirmation Failed</span>
            <p className="text-text-primary">
              {errorMessage}. Please click below to retry.
            </p>
          </div>
        </div>
      )}

      {/* Decision Buttons (SCREEN_SPECS.md §2.4: "the decision is the only action on the page") */}
      <div className="flex flex-col sm:flex-row items-center gap-3 pt-2">
        <Button
          type="button"
          variant="primary"
          size="lg"
          className="w-full sm:flex-1"
          disabled={status === 'submitting'}
          onClick={handleConfirm}
          leftIcon={status === 'submitting' ? <RotateCw className="w-4 h-4 animate-spin" /> : <CheckCircle className="w-4 h-4" />}
        >
          {status === 'submitting' ? 'Confirming...' : 'Confirm Resolved (संतोषजनक)'}
        </Button>

        <Button
          type="button"
          variant="outline"
          size="lg"
          className="w-full sm:flex-1 border-status-danger text-status-danger hover:bg-status-danger/10"
          disabled={status === 'submitting'}
          onClick={() => navigate(`/track/${encodeURIComponent(token)}/dispute`)}
          leftIcon={<AlertTriangle className="w-4 h-4" />}
        >
          Dispute Closure (असंतोषजनक)
        </Button>
      </div>
    </div>
  );
};
