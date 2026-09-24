import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Button,
  Field,
  Input,
  EvidencePhotoCard,
  TrackingTokenDisplay,
  SealMark,
} from '@civicbrain/ui';
import {
  ArrowRight,
  ShieldCheck,
  CheckCircle,
  AlertCircle,
  Building2,
  Tag,
  Phone,
  FileText,
  RotateCw,
  PlusCircle,
} from 'lucide-react';
import { useReportDraft } from '../context/ReportDraftContext';
import { IntakeStepHeader } from '../components/IntakeStepHeader';

export const ReportReviewView: React.FC = () => {
  const navigate = useNavigate();
  const { draft, updateDraft, submitDraft, resetDraft } = useReportDraft();

  const [hasSubmitted, setHasSubmitted] = useState(Boolean(draft.submittedToken));
  const [createdToken, setCreatedToken] = useState<string | null>(draft.submittedToken);

  const handleSubmit = async () => {
    try {
      const token = await submitDraft();
      setCreatedToken(token);
      setHasSubmitted(true);
    } catch {
      // Handled in context
    }
  };

  const handleStartNewReport = () => {
    resetDraft();
    navigate('/');
  };

  // SUCCESS STATE: Expressive confirmation with SealMark & TrackingTokenDisplay
  if (hasSubmitted && createdToken) {
    return (
      <div className="w-full max-w-[640px] mx-auto flex flex-col gap-6 font-ui animate-in fade-in duration-deliberate">
        {/* Verification Audit Stamp */}
        <SealMark
          authority="BRUHAT BENGALURU MAHANAGARA PALIKE"
          label={draft.isOffline ? "REPORT QUEUED IN LOCAL STORAGE (OFFLINE)" : "REPORT REGISTERED IN MUNICIPAL INTAKE"}
          hash={`0x${Math.random().toString(16).substring(2, 10).toUpperCase()}...${createdToken.slice(-4)}`}
          timestamp={new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}
          size="lg"
        />

        <div className="flex flex-col gap-2 text-center items-center">
          <h2 className="text-2xl font-bold text-primary tracking-tight">
            {draft.isOffline ? "Saved Offline — Will Auto-Sync" : "Report Filed Successfully"}
          </h2>
          <p className="text-sm text-text-secondary max-w-md leading-relaxed">
            {draft.isOffline
              ? "Your report has been securely saved to this device. It will automatically submit to the municipal intake pipeline as soon as network connectivity is restored."
              : "Your report has been assigned an immutable waybill tracking token. Save or copy this token to monitor per-observation repair progress and department resolution proofs."}
          </p>
        </div>

        {/* The Tracking Token is the Artifact per SCREEN_SPECS.md §2.1 & §2.2 */}
        <TrackingTokenDisplay
          token={createdToken}
          timestamp={new Date().toLocaleDateString('en-IN', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
          })}
          summary={`${draft.wardName} · ${draft.categoryName}`}
          size="lg"
        />

        {/* Next Actions */}
        <div className="flex flex-col sm:flex-row items-center gap-3 pt-4 border-t border-border">
          <Button
            type="button"
            variant="primary"
            size="lg"
            className="w-full sm:flex-1"
            onClick={() => navigate(`/track/${encodeURIComponent(createdToken)}`)}
            rightIcon={<ArrowRight className="w-4 h-4" />}
          >
            Track Report Status
          </Button>

          <Button
            type="button"
            variant="outline"
            size="lg"
            className="w-full sm:flex-1"
            onClick={handleStartNewReport}
            leftIcon={<PlusCircle className="w-4 h-4" />}
          >
            Submit Another Report
          </Button>
        </div>
      </div>
    );
  }

  // REVIEW & SUBMIT STATE
  const progressPercent = Math.round((draft.uploadProgressBytes / draft.totalBytes) * 100);

  return (
    <div className="w-full max-w-[640px] mx-auto flex flex-col gap-6 font-ui">
      {/* Field Notebook Header */}
      <IntakeStepHeader
        currentStep={4}
        title="Review & Submit Report"
        subtitle="Review the assembled defect evidence before committing to the municipal intake registry."
        backUrl="/report/new/category"
        backLabel="Back to category"
      />

      {/* Summary Review Cards */}
      <div className="flex flex-col gap-4">
        {/* Evidence Card */}
        {draft.photoPreviewUrl ? (
          <div className="flex flex-col gap-1.5">
            <span className="text-xs font-semibold uppercase tracking-wider text-text-secondary font-mono">
              Photographic Evidence
            </span>
            <EvidencePhotoCard
              src={draft.photoPreviewUrl}
              alt={`Evidence for ${draft.categoryName || 'civic issue'} in ${draft.wardName}`}
              coordinates={`${draft.latitude.toFixed(4)}° N, ${draft.longitude.toFixed(4)}° E`}
              timestamp={draft.photoMetadata?.timestamp || 'Just now'}
              caption="Citizen Ingest Evidence (4:3 Native Aspect)"
              isRedacted={false}
            />
          </div>
        ) : (
          <div className="p-4 rounded-md bg-surface border border-border flex items-start gap-3">
            <FileText className="w-5 h-5 text-action-primary shrink-0 mt-0.5" />
            <div className="flex flex-col gap-1 text-xs">
              <span className="font-semibold text-primary">Text Description</span>
              <p className="text-text-secondary leading-relaxed">
                "{draft.description || draft.voiceTranscript}"
              </p>
            </div>
          </div>
        )}

        {/* Location & Routing Summary */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div className="p-3.5 rounded-md bg-surface border border-border flex items-start gap-3">
            <Building2 className="w-4 h-4 text-action-primary shrink-0 mt-0.5" />
            <div className="flex flex-col gap-0.5 text-xs">
              <span className="font-semibold text-primary">Ward & Address</span>
              <span className="font-mono text-text-secondary font-medium">{draft.wardName}</span>
              <span className="text-text-secondary truncate mt-0.5">{draft.addressText}</span>
            </div>
          </div>

          <div className="p-3.5 rounded-md bg-surface border border-border flex items-start gap-3">
            <Tag className="w-4 h-4 text-action-primary shrink-0 mt-0.5" />
            <div className="flex flex-col gap-0.5 text-xs">
              <span className="font-semibold text-primary">Citizen Category</span>
              <span className="font-medium text-primary">{draft.categoryName || 'General Defect'}</span>
              <span className="font-mono text-text-secondary text-[11px] mt-0.5">
                Dept: {draft.departmentCode || 'ROADS'}
              </span>
            </div>
          </div>
        </div>

        {/* Contact Phone for SMS Updates (Optional) */}
        <div className="p-4 rounded-md bg-surface border border-border flex flex-col gap-3 shadow-flat">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-text-secondary font-mono">
            <Phone className="w-4 h-4 text-action-primary" />
            <span>SMS Status Notifications (Optional)</span>
          </div>

          <Field
            id="citizen-phone"
            label="Mobile Number"
            helperText="Enter 10-digit mobile number to receive resolution SMS updates and waybill token copy."
          >
            <Input
              id="citizen-phone"
              type="tel"
              value={draft.contactPhone}
              onChange={(e) => updateDraft({ contactPhone: e.target.value })}
              placeholder="e.g. 9876543210"
              className="font-mono text-sm"
              maxLength={10}
            />
          </Field>
        </div>
      </div>

      {/* Upload in Progress: Byte Progress Bar per DESIGN.md §10 */}
      {draft.isSubmitting && (
        <div
          role="status"
          aria-live="polite"
          className="p-4 rounded-md bg-surface border border-action-primary flex flex-col gap-2 shadow-flat"
        >
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="font-semibold text-primary">
              {draft.isOffline ? 'Saving draft to local storage...' : 'Uploading evidence bytes...'}
            </span>
            <span className="text-action-primary font-bold">
              {draft.isOffline
                ? 'Queued'
                : `${(draft.uploadProgressBytes / 1024).toFixed(0)} KB / ${(draft.totalBytes / 1024).toFixed(0)} KB (${progressPercent}%)`}
            </span>
          </div>

          {/* Real Byte Progress Bar */}
          <div className="w-full h-2 rounded-full bg-surface-raised overflow-hidden border border-border">
            <div
              className="h-full bg-action-primary transition-all duration-base ease-standard"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
        </div>
      )}

      {/* Error State with Retry Affordance (SCREEN_SPECS.md §2.2: retry, draft preserved) */}
      {draft.submitError && (
        <div className="p-4 rounded-md bg-status-danger/10 border border-status-danger text-status-danger flex items-start gap-3">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
          <div className="flex flex-col gap-1 text-xs">
            <span className="font-bold">Submission Encountered an Error</span>
            <p className="text-text-primary leading-normal">
              {draft.submitError}. Your field notebook draft is preserved locally. Please click retry below.
            </p>
          </div>
        </div>
      )}

      {/* Submit Action */}
      <div className="flex items-center justify-between pt-4 border-t border-border">
        <span className="text-xs text-text-secondary font-mono">
          {draft.isOffline ? 'Offline — Will queue locally' : 'Ready to commit to intake'}
        </span>

        <Button
          type="button"
          variant="primary"
          size="lg"
          disabled={draft.isSubmitting}
          onClick={handleSubmit}
          leftIcon={draft.submitError ? <RotateCw className="w-4 h-4" /> : <ShieldCheck className="w-4 h-4" />}
        >
          {draft.isSubmitting
            ? 'Transmitting...'
            : draft.submitError
            ? 'Retry Submission'
            : draft.isOffline
            ? 'Save Draft Offline'
            : 'Submit Official Report'}
        </Button>
      </div>
    </div>
  );
};
