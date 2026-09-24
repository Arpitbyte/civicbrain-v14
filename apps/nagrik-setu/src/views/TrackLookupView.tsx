import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Field,
  Input,
  Button,
  TrackingTokenDisplay,
} from '@civicbrain/ui';
import { Search, ShieldAlert, ArrowRight, History } from 'lucide-react';

export const TrackLookupView: React.FC = () => {
  const [tokenInput, setTokenInput] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);
  const navigate = useNavigate();

  // Quick-access past reports sample or from localStorage
  const sampleRecentTokens = [
    { token: 'CB-2026-W14-8892', label: 'Ward 14 · Indiranagar (Multi-issue split: Roads + Drains)' },
    { token: 'CB-2026-W11-4012', label: 'Ward 11 · Malleshwaram (All resolved)' },
  ];

  const handleLookup = (e: React.FormEvent) => {
    e.preventDefault();
    const cleanToken = tokenInput.trim();
    if (!cleanToken) {
      setValidationError('Please enter a valid tracking token or registered phone number.');
      return;
    }
    if (cleanToken.length < 6) {
      setValidationError('Tracking tokens must be at least 6 characters in length.');
      return;
    }
    setValidationError(null);
    navigate(`/track/${encodeURIComponent(cleanToken)}`);
  };

  return (
    <div className="w-full max-w-[560px] mx-auto py-6 sm:py-10 px-4 flex flex-col gap-8 font-ui">
      {/* Title & Introduction */}
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold tracking-tight text-primary">
          Track Your Report
        </h1>
        <p className="text-sm text-text-secondary leading-relaxed">
          CivicBrain provides a glass-box audit trail for every submitted civic defect.
          Enter your unique waybill tracking token to check per-observation progress and department resolution proofs.
        </p>
      </div>

      {/* Lookup Form */}
      <form
        onSubmit={handleLookup}
        className="p-5 sm:p-6 bg-surface rounded-md border border-border flex flex-col gap-5 shadow-flat"
      >
        <Field
          id="tracking-token-field"
          label="Waybill Tracking Token"
          required
          helperText="Format: CB-YYYY-WXX-XXXX or the mobile number used during submission."
          errorMessage={validationError ?? undefined}
        >
          <Input
            id="tracking-token-field"
            value={tokenInput}
            onChange={(e) => {
              setTokenInput(e.target.value);
              if (validationError) setValidationError(null);
            }}
            placeholder="e.g. CB-2026-W14-8892"
            leftIcon={<Search className="w-4 h-4" />}
            size="lg"
            className="font-mono text-sm tracking-wide"
            autoFocus
          />
        </Field>

        <Button
          type="submit"
          variant="primary"
          size="lg"
          rightIcon={<ArrowRight className="w-4 h-4" />}
          className="w-full"
        >
          Track Report Status
        </Button>
      </form>

      {/* Recent Submissions / Quick-Access Stubs */}
      <div className="flex flex-col gap-3 pt-4 border-t border-border">
        <div className="flex items-center gap-2 text-xs font-semibold text-text-secondary uppercase tracking-wider">
          <History className="w-3.5 h-3.5" />
          <span>Recent Field Waybills (Quick Access)</span>
        </div>

        <div className="flex flex-col gap-3">
          {sampleRecentTokens.map(({ token, label }) => (
            <div
              key={token}
              onClick={() => navigate(`/track/${token}`)}
              className="
                p-3.5 bg-surface hover:bg-surface-raised rounded-md border border-border
                cursor-pointer transition-all duration-fast flex items-center justify-between gap-4
                outline-none focus-visible:ring-2 focus-visible:ring-focus
              "
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  navigate(`/track/${token}`);
                }
              }}
            >
              <div className="flex flex-col min-w-0">
                <span className="font-mono font-bold text-primary text-sm tracking-wide">
                  {token}
                </span>
                <span className="text-xs text-text-secondary truncate mt-0.5">
                  {label}
                </span>
              </div>

              <ArrowRight className="w-4 h-4 text-text-secondary flex-shrink-0" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
