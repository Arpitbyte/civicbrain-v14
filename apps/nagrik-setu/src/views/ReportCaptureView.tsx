import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Button,
  Field,
  Textarea,
} from '@civicbrain/ui';
import {
  Camera,
  Mic,
  FileText,
  Upload,
  ArrowRight,
  AlertCircle,
  CheckCircle,
  RefreshCw,
  Sparkles,
} from 'lucide-react';
import { useReportDraft } from '../context/ReportDraftContext';
import { IntakeStepHeader } from '../components/IntakeStepHeader';

export const ReportCaptureView: React.FC = () => {
  const navigate = useNavigate();
  const { draft, updateDraft, isStep1Valid } = useReportDraft();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [activeTab, setActiveTab] = useState<'photo' | 'voice' | 'text'>(draft.mediaType || 'photo');
  const [isRecording, setIsRecording] = useState(false);

  // Sample authentic defect fixture (SVG data URI - 4:3 aspect ratio, 0 external images)
  const sampleDefectSvg = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600"><rect width="800" height="600" fill="%232b2622"/><path d="M 160 300 Q 240 220 380 250 T 620 320 Q 560 440 380 430 T 160 300 Z" fill="%23171412" stroke="%233f3833" stroke-width="4"/><ellipse cx="370" cy="330" rx="140" ry="70" fill="%230f0d0b"/><text x="40" y="560" fill="%23f97316" font-family="monospace" font-size="20" font-weight="bold">BBMP CITIZEN EVIDENCE • LAT: 12.9784 N, LNG: 77.6408 E</text></svg>`;

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (uploadEvent) => {
        const url = uploadEvent.target?.result as string;
        updateDraft({
          photoPreviewUrl: url,
          mediaType: 'photo',
          photoMetadata: {
            timestamp: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }),
            latitude: draft.latitude,
            longitude: draft.longitude,
          },
          cameraPermissionDenied: false,
        });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUseSamplePhoto = () => {
    updateDraft({
      photoPreviewUrl: sampleDefectSvg,
      mediaType: 'photo',
      photoMetadata: {
        timestamp: '11:42 AM IST',
        latitude: 12.9784,
        longitude: 77.6408,
      },
      cameraPermissionDenied: false,
    });
  };

  const handleSimulateCameraDenied = () => {
    updateDraft({
      cameraPermissionDenied: true,
      photoPreviewUrl: null,
    });
  };

  const handleRetryCamera = () => {
    updateDraft({ cameraPermissionDenied: false });
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleToggleRecord = () => {
    if (!isRecording) {
      setIsRecording(true);
      // Simulate live speech recognition
      setTimeout(() => {
        setIsRecording(false);
        updateDraft({
          voiceTranscript: 'There is a deep pothole on 12th Main Road Indiranagar near the signal causing severe traffic bottleneck.',
          description: draft.description || 'Deep pothole on 12th Main Road Indiranagar near the signal causing severe traffic bottleneck.',
        });
      }, 2500);
    } else {
      setIsRecording(false);
    }
  };

  return (
    <div className="w-full max-w-[640px] mx-auto flex flex-col gap-6 font-ui">
      {/* Field Notebook Header */}
      <IntakeStepHeader
        currentStep={1}
        title="Capture Issue Evidence"
        subtitle="Provide photographic proof, voice dictation, or a detailed text description."
        backUrl="/"
        backLabel="Return to home"
      />

      {/* Capture Mode Switcher */}
      <div
        role="tablist"
        aria-label="Capture mode selection"
        className="grid grid-cols-3 p-1 rounded-md bg-surface border border-border text-xs font-semibold"
      >
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'photo'}
          onClick={() => setActiveTab('photo')}
          className={`
            flex items-center justify-center gap-1.5 py-2.5 rounded transition-colors
            ${activeTab === 'photo' ? 'bg-surface-raised text-primary shadow-xs font-bold' : 'text-text-secondary hover:text-primary'}
          `}
        >
          <Camera className="w-4 h-4" />
          <span>Camera / Photo</span>
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'voice'}
          onClick={() => setActiveTab('voice')}
          className={`
            flex items-center justify-center gap-1.5 py-2.5 rounded transition-colors
            ${activeTab === 'voice' ? 'bg-surface-raised text-primary shadow-xs font-bold' : 'text-text-secondary hover:text-primary'}
          `}
        >
          <Mic className="w-4 h-4" />
          <span>Voice Dictation</span>
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'text'}
          onClick={() => setActiveTab('text')}
          className={`
            flex items-center justify-center gap-1.5 py-2.5 rounded transition-colors
            ${activeTab === 'text' ? 'bg-surface-raised text-primary shadow-xs font-bold' : 'text-text-secondary hover:text-primary'}
          `}
        >
          <FileText className="w-4 h-4" />
          <span>Text Notes</span>
        </button>
      </div>

      {/* Hidden File Input for Mobile Camera / Gallery */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleFileUpload}
        className="hidden"
        id="camera-input"
      />

      {/* Panel 1: Photo Capture */}
      {activeTab === 'photo' && (
        <div className="flex flex-col gap-4">
          {/* Permission Denied State (SCREEN_SPECS.md §2.2: explicit re-prompt UI, not silent failure) */}
          {draft.cameraPermissionDenied ? (
            <div className="p-6 rounded-md bg-status-danger/10 border border-status-danger text-status-danger flex flex-col gap-3">
              <div className="flex items-center gap-2 font-bold text-sm">
                <AlertCircle className="w-5 h-5 shrink-0" />
                <span>Camera Access Blocked</span>
              </div>
              <p className="text-xs text-text-primary leading-normal">
                Your browser or device has denied camera access for Nagrik Setu. Please enable camera permissions in browser site settings or upload a saved photo from your device storage.
              </p>
              <div className="flex items-center gap-3 pt-2">
                <Button
                  type="button"
                  variant="primary"
                  size="sm"
                  onClick={handleRetryCamera}
                  leftIcon={<RefreshCw className="w-4 h-4" />}
                >
                  Retry Camera Permissions
                </Button>
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="text-xs font-medium text-text-secondary hover:text-primary underline"
                >
                  Select from gallery
                </button>
              </div>
            </div>
          ) : draft.photoPreviewUrl ? (
            /* 4:3 Aspect Ratio Evidence Preview per DESIGN.md §7 */
            <div className="flex flex-col rounded-md border border-border bg-surface overflow-hidden shadow-flat">
              <div className="aspect-[4/3] w-full bg-station-950 relative overflow-hidden flex items-center justify-center">
                <img
                  src={draft.photoPreviewUrl}
                  alt="Captured citizen evidence"
                  className="w-full h-full object-cover"
                />
                <div className="absolute top-2 right-2 px-2 py-1 rounded bg-station-950/80 text-marker-500 font-mono text-[11px] border border-border">
                  4:3 Native Aspect Preserved
                </div>
              </div>

              {/* Mono Caption Strip */}
              <div className="p-3 bg-surface-raised border-t border-border flex items-center justify-between text-xs font-mono text-text-secondary">
                <span>TIMESTAMP: {draft.photoMetadata?.timestamp || '11:42 AM'}</span>
                <span>GPS: {draft.latitude.toFixed(4)}°N, {draft.longitude.toFixed(4)}°E</span>
              </div>

              <div className="p-3 flex items-center justify-between border-t border-border bg-surface">
                <div className="flex items-center gap-1.5 text-xs text-status-success font-medium">
                  <CheckCircle className="w-4 h-4" />
                  <span>Evidence photo attached</span>
                </div>
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="text-xs font-medium text-action-primary hover:underline"
                >
                  Retake / Change photo
                </button>
              </div>
            </div>
          ) : (
            /* Empty Photo Capture Prompt */
            <div className="p-8 sm:p-10 rounded-md border-2 border-dashed border-border bg-surface flex flex-col items-center justify-center text-center gap-4">
              <div className="w-16 h-16 rounded-full bg-marker-500/15 text-action-primary flex items-center justify-center">
                <Camera className="w-8 h-8 stroke-[2]" />
              </div>

              <div className="flex flex-col gap-1 max-w-sm">
                <h3 className="font-bold text-base text-primary">
                  Capture or Upload Photo
                </h3>
                <p className="text-xs text-text-secondary">
                  High-contrast photo of the issue helps municipal departments triage and dispatch the right equipment.
                </p>
              </div>

              <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
                <Button
                  type="button"
                  variant="primary"
                  size="md"
                  onClick={() => fileInputRef.current?.click()}
                  leftIcon={<Camera className="w-4 h-4" />}
                >
                  Take Photo / Browse
                </Button>

                <Button
                  type="button"
                  variant="outline"
                  size="md"
                  onClick={handleUseSamplePhoto}
                  leftIcon={<Sparkles className="w-4 h-4 text-action-primary" />}
                >
                  Use Sample Defect
                </Button>
              </div>

              <button
                type="button"
                onClick={handleSimulateCameraDenied}
                className="text-[11px] font-mono text-text-secondary hover:underline mt-2"
              >
                (Test Camera Permission Denied UI)
              </button>
            </div>
          )}
        </div>
      )}

      {/* Panel 2: Voice Dictation */}
      {activeTab === 'voice' && (
        <div className="p-6 rounded-md bg-surface border border-border flex flex-col items-center text-center gap-5 shadow-flat">
          <div className="flex flex-col gap-1 max-w-sm">
            <h3 className="font-bold text-base text-primary">
              Voice Dictation (जन सुनवाई)
            </h3>
            <p className="text-xs text-text-secondary">
              Tap the microphone and describe the civic issue in Kannada, Hindi, or English.
            </p>
          </div>

          <button
            type="button"
            onClick={handleToggleRecord}
            className={`
              w-20 h-20 rounded-full flex items-center justify-center transition-all duration-base
              ${isRecording
                ? 'bg-status-danger text-white animate-pulse ring-4 ring-status-danger/30'
                : 'bg-surface-raised border border-border text-primary hover:border-action-primary'}
            `}
            aria-label={isRecording ? 'Stop recording voice note' : 'Start recording voice note'}
          >
            <Mic className={`w-8 h-8 ${isRecording ? 'stroke-[2.5]' : 'stroke-2'}`} />
          </button>

          <span className="font-mono text-xs text-text-secondary">
            {isRecording ? 'Listening and transcribing...' : 'Tap to start speaking'}
          </span>

          {draft.voiceTranscript && (
            <div className="w-full text-left p-3.5 rounded-md bg-surface-raised border border-border flex flex-col gap-1 text-xs">
              <span className="font-mono font-semibold text-text-secondary uppercase text-[10px]">
                Recorded Voice Transcript
              </span>
              <p className="text-primary italic leading-relaxed">
                "{draft.voiceTranscript}"
              </p>
            </div>
          )}
        </div>
      )}

      {/* Panel 3: Text Notes */}
      {activeTab === 'text' && (
        <div className="p-5 rounded-md bg-surface border border-border flex flex-col gap-4 shadow-flat">
          <Field
            id="issue-description"
            label="Describe the civic issue"
            required
            helperText="Include noticeable landmarks, hazard level, or depth."
          >
            <Textarea
              id="issue-description"
              rows={4}
              value={draft.description}
              onChange={(e) => updateDraft({ description: e.target.value })}
              placeholder="e.g. Deep crater near pedestrian crossing causing two-wheelers to skid during rainfall."
              className="text-sm leading-relaxed"
            />
          </Field>
          <div className="flex justify-between items-center text-xs font-mono text-text-secondary">
            <span>Minimum 5 characters required</span>
            <span>{draft.description.length} chars</span>
          </div>
        </div>
      )}

      {/* Optional Description if Photo is attached */}
      {activeTab === 'photo' && draft.photoPreviewUrl && (
        <Field
          id="additional-notes"
          label="Optional details / Remarks"
          helperText="Add any specific context or safety risk (e.g. exposed live cables, near school gate)."
        >
          <Textarea
            id="additional-notes"
            rows={2}
            value={draft.description}
            onChange={(e) => updateDraft({ description: e.target.value })}
            placeholder="e.g. Located right next to the school bus stop."
            className="text-xs"
          />
        </Field>
      )}

      {/* Step Navigation Actions */}
      <div className="flex items-center justify-between pt-4 border-t border-border">
        <span className="text-xs text-text-secondary font-mono">
          {isStep1Valid ? '✓ Evidence attached' : '* Provide photo, voice, or text to proceed'}
        </span>

        <Button
          type="button"
          variant="primary"
          size="lg"
          disabled={!isStep1Valid}
          onClick={() => navigate('/report/new/location')}
          rightIcon={<ArrowRight className="w-4 h-4" />}
        >
          Next: Verify Location
        </Button>
      </div>
    </div>
  );
};
