import React from 'react';
import { EvidencePhotoCard, EvidencePhotoCardProps } from './EvidencePhotoCard';

export interface BeforeAfterPairProps {
  before: EvidencePhotoCardProps;
  after: EvidencePhotoCardProps;
  title?: string;
  className?: string;
}

/**
 * BeforeAfterPair
 * Conforms to DESIGN.md §7 & SCREEN_SPECS.md Tier 1:
 * - Two EvidencePhotoCards shown at equal size
 * - Side by side on tablet+ (grid-cols-2), stacked on mobile (grid-cols-1)
 * - Clear "Before (Reported Defect)" vs "After (Completed Resolution)" headers
 */
export const BeforeAfterPair: React.FC<BeforeAfterPairProps> = ({
  before,
  after,
  title = 'Work Order Photographic Resolution Verification',
  className = '',
}) => {
  return (
    <div className={`flex flex-col gap-3 w-full ${className}`}>
      {title && (
        <div className="flex items-center justify-between pb-2 border-b border-border">
          <h3 className="text-sm font-ui font-semibold text-primary">{title}</h3>
          <span className="text-xs font-mono text-text-secondary">Side-by-Side Audit</span>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
        {/* Before Card */}
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center justify-between px-1">
            <span className="text-xs font-ui font-semibold text-status-warning uppercase tracking-wider">
              Before (Defect Ingest)
            </span>
          </div>
          <EvidencePhotoCard {...before} />
        </div>

        {/* After Card */}
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center justify-between px-1">
            <span className="text-xs font-ui font-semibold text-status-success uppercase tracking-wider">
              After (Field Remediation)
            </span>
          </div>
          <EvidencePhotoCard {...after} />
        </div>
      </div>
    </div>
  );
};
