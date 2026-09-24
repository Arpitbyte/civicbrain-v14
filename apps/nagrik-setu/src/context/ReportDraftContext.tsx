import React, { createContext, useContext, useState, useEffect } from 'react';
import { saveRecentReport } from '../services/citizenStorage';

export interface ReportDraft {
  // Step 1: Capture
  mediaType: 'photo' | 'voice' | 'text';
  photoPreviewUrl: string | null;
  photoMetadata: {
    timestamp: string;
    latitude?: number;
    longitude?: number;
  } | null;
  voiceTranscript: string;
  description: string;
  cameraPermissionDenied: boolean;

  // Step 2: Location
  latitude: number;
  longitude: number;
  addressText: string;
  wardCode: string;
  wardName: string;

  // Step 3: Category (strictly citizen-declared)
  categoryCode: string;
  categoryName: string;
  departmentCode: string;
  departmentName: string;

  // Step 4: Contact & Verification
  contactPhone: string;

  // Lifecycle
  isOffline: boolean;
  isSubmitting: boolean;
  uploadProgressBytes: number;
  totalBytes: number;
  submitError: string | null;
  submittedToken: string | null;
}

export interface ReportDraftContextValue {
  draft: ReportDraft;
  updateDraft: (updates: Partial<ReportDraft>) => void;
  resetDraft: () => void;
  isStep1Valid: boolean;
  isStep2Valid: boolean;
  isStep3Valid: boolean;
  submitDraft: () => Promise<string>;
}

const DRAFT_STORAGE_KEY = 'civicbrain_nagrik_draft_v1';

// Default realistic Bangalore municipal coordinates (Ward 14 · Indiranagar)
const INITIAL_DRAFT: ReportDraft = {
  mediaType: 'photo',
  photoPreviewUrl: null,
  photoMetadata: null,
  voiceTranscript: '',
  description: '',
  cameraPermissionDenied: false,

  latitude: 12.9784,
  longitude: 77.6408,
  addressText: '100 Feet Road, 12th Main Junction, Indiranagar',
  wardCode: 'W14',
  wardName: 'Ward 14 (Indiranagar)',

  categoryCode: '',
  categoryName: '',
  departmentCode: '',
  departmentName: '',

  contactPhone: '',

  isOffline: typeof navigator !== 'undefined' ? !navigator.onLine : false,
  isSubmitting: false,
  uploadProgressBytes: 0,
  totalBytes: 2450000, // ~2.45 MB photo byte simulation
  submitError: null,
  submittedToken: null,
};

const ReportDraftContext = createContext<ReportDraftContextValue | undefined>(undefined);

export const ReportDraftProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [draft, setDraft] = useState<ReportDraft>(() => {
    try {
      const saved = localStorage.getItem(DRAFT_STORAGE_KEY);
      if (saved) {
        return {
          ...INITIAL_DRAFT,
          ...JSON.parse(saved),
          isSubmitting: false,
          submitError: null,
          submittedToken: null,
        };
      }
    } catch {
      // Fallback
    }
    return INITIAL_DRAFT;
  });

  // Online / Offline tracking
  useEffect(() => {
    const handleOnline = () => setDraft((d) => ({ ...d, isOffline: false }));
    const handleOffline = () => setDraft((d) => ({ ...d, isOffline: true }));
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Persist draft to local storage on edits
  useEffect(() => {
    try {
      localStorage.setItem(DRAFT_STORAGE_KEY, JSON.stringify(draft));
    } catch {
      // Ignore quota exceptions
    }
  }, [draft]);

  const updateDraft = (updates: Partial<ReportDraft>) => {
    setDraft((prev) => ({ ...prev, ...updates }));
  };

  const resetDraft = () => {
    try {
      localStorage.removeItem(DRAFT_STORAGE_KEY);
    } catch {
      // Ignore
    }
    setDraft({ ...INITIAL_DRAFT, isOffline: !navigator.onLine });
  };

  // Step Validations
  const isStep1Valid = Boolean(
    draft.photoPreviewUrl ||
    draft.voiceTranscript.trim().length > 0 ||
    draft.description.trim().length >= 5
  );

  const isStep2Valid = Boolean(
    draft.latitude &&
    draft.longitude &&
    draft.wardCode &&
    draft.addressText.trim().length > 3
  );

  const isStep3Valid = Boolean(
    draft.categoryCode &&
    draft.departmentCode
  );

  // Submit Draft
  const submitDraft = async (): Promise<string> => {
    updateDraft({ isSubmitting: true, submitError: null, uploadProgressBytes: 0 });

    try {
      // If citizen is offline, queue mutation locally
      if (!navigator.onLine || draft.isOffline) {
        const offlineToken = `CB-OFFLINE-${Date.now().toString().slice(-6)}`;
        await saveRecentReport({
          token: offlineToken,
          submittedAt: new Date().toLocaleDateString('en-IN', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
          }),
          summary: `${draft.wardName} · ${draft.categoryName} (Saved offline — will sync)`,
          ward: draft.wardName,
          category: draft.categoryName,
        });

        updateDraft({
          isSubmitting: false,
          submittedToken: offlineToken,
          uploadProgressBytes: draft.totalBytes,
        });
        return offlineToken;
      }

      // Simulate real byte upload progress for evidence
      const stepBytes = Math.floor(draft.totalBytes / 4);
      for (let i = 1; i <= 4; i++) {
        await new Promise((r) => setTimeout(r, 120));
        updateDraft({ uploadProgressBytes: Math.min(stepBytes * i, draft.totalBytes) });
      }

      // Generate authentic tracking token matching backend format: CB-YYYY-WXX-XXXX
      const randomSuffix = Math.floor(1000 + Math.random() * 9000);
      const generatedToken = `CB-2026-${draft.wardCode}-${randomSuffix}`;

      // Save to client-side recent reports storage
      await saveRecentReport({
        token: generatedToken,
        submittedAt: new Date().toLocaleDateString('en-IN', {
          day: '2-digit',
          month: 'short',
          year: 'numeric',
        }),
        summary: `${draft.wardName} · ${draft.categoryName}`,
        ward: draft.wardName,
        category: draft.categoryName,
      });

      updateDraft({
        isSubmitting: false,
        submittedToken: generatedToken,
        uploadProgressBytes: draft.totalBytes,
      });

      // Clear draft after successful commit
      try {
        localStorage.removeItem(DRAFT_STORAGE_KEY);
      } catch {
        // Ignore
      }

      return generatedToken;
    } catch (err: any) {
      updateDraft({
        isSubmitting: false,
        submitError: err?.message || 'Unable to submit report to municipal intake. Please retry.',
      });
      throw err;
    }
  };

  return (
    <ReportDraftContext.Provider
      value={{
        draft,
        updateDraft,
        resetDraft,
        isStep1Valid,
        isStep2Valid,
        isStep3Valid,
        submitDraft,
      }}
    >
      {children}
    </ReportDraftContext.Provider>
  );
};

export const useReportDraft = (): ReportDraftContextValue => {
  const context = useContext(ReportDraftContext);
  if (!context) {
    throw new Error('useReportDraft must be used within a ReportDraftProvider');
  }
  return context;
};
