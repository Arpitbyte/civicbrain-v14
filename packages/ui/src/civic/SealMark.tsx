import React from 'react';
import { Award, CheckCircle } from 'lucide-react';

export interface SealMarkProps {
  /**
   * Authority label (e.g. "Bruhat Bengaluru Mahanagara Palike" or "Municipal Corporation")
   */
  authority?: string;
  /**
   * Verification status text
   */
  label?: string;
  /**
   * Cryptographic verification hash or ledger ID
   */
  hash?: string;
  /**
   * Verified timestamp
   */
  timestamp?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

/**
 * SealMark
 * Conforms to DESIGN.md §8 & SCREEN_SPECS.md Tier 1:
 * - "A Seal-styled confirmation for verified/committed actions, distinct from a generic success toast"
 * - Deep Seal color palette (--color-verified-seal / --seal-600)
 * - Cryptographic ledger verification stamp aesthetic
 */
export const SealMark: React.FC<SealMarkProps> = ({
  authority = 'MUNICIPAL CORPORATION AUDIT SEAL',
  label = 'OFFICIALLY VERIFIED & COMMITTED',
  hash,
  timestamp,
  size = 'md',
  className = '',
}) => {
  const sizeClasses = {
    sm: 'p-2.5 text-xs',
    md: 'p-4 text-sm',
    lg: 'p-6 text-base',
  }[size];

  return (
    <div
      role="status"
      aria-label={`Official Seal: ${label}, Authority: ${authority}`}
      className={`
        relative flex flex-col items-center justify-center text-center rounded-md border-2 border-dashed
        border-verified-seal/40 bg-verified-seal/5 text-primary font-ui overflow-hidden
        ${sizeClasses}
        ${className}
      `}
    >
      {/* Outer Stamp Motif */}
      <div className="flex items-center justify-center p-2 rounded-full bg-verified-seal/15 text-verified-seal mb-2">
        <Award className="w-6 h-6 stroke-[2]" aria-hidden="true" />
      </div>

      <div className="text-[10px] font-mono tracking-widest text-text-secondary uppercase mb-0.5">
        {authority}
      </div>

      <div className="font-bold tracking-tight text-verified-seal uppercase flex items-center gap-1.5">
        <CheckCircle className="w-4 h-4 text-verified-seal" aria-hidden="true" />
        <span>{label}</span>
      </div>

      {(hash || timestamp) && (
        <div className="mt-2 pt-2 border-t border-verified-seal/20 flex flex-col sm:flex-row items-center gap-2 sm:gap-4 text-[10px] font-mono text-text-secondary">
          {hash && (
            <span title="Jan Sunwai Cryptographic Ledger Hash">
              Ledger: <strong className="text-primary">{hash.substring(0, 16)}...</strong>
            </span>
          )}
          {timestamp && <span>Date: {timestamp}</span>}
        </div>
      )}
    </div>
  );
};
