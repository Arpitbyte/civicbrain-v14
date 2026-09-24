import React from 'react';
import { Link } from 'react-router-dom';
import { WifiOff, ArrowLeft, BookOpen } from 'lucide-react';
import { useReportDraft } from '../context/ReportDraftContext';

export interface IntakeStepHeaderProps {
  currentStep: 1 | 2 | 3 | 4;
  title: string;
  subtitle: string;
  backUrl?: string;
  backLabel?: string;
}

export const IntakeStepHeader: React.FC<IntakeStepHeaderProps> = ({
  currentStep,
  title,
  subtitle,
  backUrl,
  backLabel = 'Back to previous step',
}) => {
  const { draft } = useReportDraft();

  return (
    <div className="flex flex-col gap-3 font-ui mb-2">
      {/* Offline Status Banner */}
      {draft.isOffline && (
        <div
          role="status"
          aria-live="polite"
          className="flex items-center gap-2 px-3 py-2 bg-marker-500/15 border border-marker-500 text-primary text-xs rounded-md font-mono"
        >
          <WifiOff className="w-4 h-4 text-action-primary shrink-0" />
          <span>Offline mode active — Draft is saved locally and will submit once reconnected.</span>
        </div>
      )}

      {/* Field Notebook Page Header */}
      <div className="flex items-center justify-between border-b border-border pb-2.5">
        {backUrl ? (
          <Link
            to={backUrl}
            className="inline-flex items-center gap-1.5 text-xs font-medium text-text-secondary hover:text-primary transition-colors focus-visible:outline-none focus-visible:underline"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>{backLabel}</span>
          </Link>
        ) : (
          <Link
            to="/"
            className="inline-flex items-center gap-1.5 text-xs font-medium text-text-secondary hover:text-primary transition-colors focus-visible:outline-none focus-visible:underline"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Cancel report</span>
          </Link>
        )}

        {/* Notebook Page-Count Badge */}
        <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-surface-raised border border-border text-xs font-mono text-text-secondary">
          <BookOpen className="w-3 h-3 text-action-primary" />
          <span className="font-semibold text-primary">Page {currentStep}</span>
          <span>of 4</span>
        </div>
      </div>

      {/* Title & Framing Subtitle */}
      <div className="flex flex-col gap-1">
        <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-primary">
          {title}
        </h1>
        <p className="text-xs sm:text-sm text-text-secondary leading-normal">
          {subtitle}
        </p>
      </div>
    </div>
  );
};
