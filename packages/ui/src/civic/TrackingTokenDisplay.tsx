import React, { useState } from 'react';
import { Copy, Check, QrCode } from 'lucide-react';
import { useToast } from '../primitives/Toast';

export interface TrackingTokenDisplayProps {
  /**
   * Authoritative alphanumeric tracking token (e.g. "CB-2026-W14-8892")
   */
  token: string;
  /**
   * Optional submitted date or timestamp
   */
  timestamp?: string;
  /**
   * Optional short summary (e.g. "Ward 14 · Roads & Stormwater")
   */
  summary?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

/**
 * TrackingTokenDisplay
 * Conforms to SCREEN_SPECS.md §2.1 & Tier 1:
 * - "The tracking token IS the artifact — a field waybill stub sits visually at the center"
 * - Mono numerals, copy-to-clipboard with toast confirmation
 * - Tactile physical ticket/waybill aesthetic (dashed perforations, mono typography)
 */
export const TrackingTokenDisplay: React.FC<TrackingTokenDisplayProps> = ({
  token,
  timestamp,
  summary,
  size = 'md',
  className = '',
}) => {
  const [copied, setCopied] = useState(false);
  const toastContext = useToast();

  const handleCopy = async () => {
    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(token);
      }
      setCopied(true);
      toastContext.toast({
        title: 'Tracking Token Copied',
        description: `Token ${token} copied to clipboard for tracking lookup.`,
        variant: 'success',
        duration: 3000,
      });
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const sizeClasses = {
    sm: 'p-3 text-sm',
    md: 'p-4 sm:p-5 text-base',
    lg: 'p-6 sm:p-8 text-xl',
  }[size];

  return (
    <div
      className={`
        relative flex flex-col bg-surface rounded-md border border-border overflow-hidden
        shadow-flat font-ui transition-colors duration-fast ${className}
      `}
    >
      {/* Waybill Header Stub */}
      <div className="flex items-center justify-between px-4 py-2 bg-surface-raised border-b border-border text-[11px] font-mono text-text-secondary">
        <div className="flex items-center gap-1.5 font-semibold text-primary">
          <QrCode className="w-3.5 h-3.5 text-action-primary" />
          <span>CIVICBRAIN FIELD WAYBILL</span>
        </div>
        {timestamp && <span>{timestamp}</span>}
      </div>

      {/* Main Stub Content */}
      <div className={`flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${sizeClasses}`}>
        <div className="flex flex-col gap-1">
          <span className="text-[11px] font-semibold text-text-secondary uppercase tracking-wider">
            Report Reference Token
          </span>
          <span className="font-mono font-bold tracking-wider text-primary select-all">
            {token}
          </span>
          {summary && <span className="text-xs text-text-secondary mt-0.5">{summary}</span>}
        </div>

        {/* Copy Button */}
        <button
          type="button"
          onClick={handleCopy}
          aria-label={`Copy tracking token ${token}`}
          className="
            inline-flex items-center justify-center gap-2 px-3 py-2 rounded-sm
            bg-surface-raised hover:bg-surface border border-border text-primary
            text-xs font-medium cursor-pointer transition-transform duration-fast active:scale-[0.98]
            outline-none focus-visible:ring-2 focus-visible:ring-focus self-start sm:self-auto
          "
        >
          {copied ? (
            <>
              <Check className="w-4 h-4 text-status-success" />
              <span className="text-status-success font-medium">Copied</span>
            </>
          ) : (
            <>
              <Copy className="w-4 h-4 text-text-secondary" />
              <span>Copy Token</span>
            </>
          )}
        </button>
      </div>

      {/* Dashed perforation stub footer */}
      <div className="relative h-2 bg-field-100 border-t border-dashed border-border" aria-hidden="true" />
    </div>
  );
};
