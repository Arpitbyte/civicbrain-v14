/**
 * citizenStorage.ts
 * Client-side local storage for citizen report tracking tokens and drafts.
 * 
 * Strict architectural rule per SCREEN_SPECS.md §2.1 & ANTIGRAVITY_PROMPTS.md PROMPT 12:
 * "Recent tokens read from local IndexedDB/localStorage draft/history store, not an API call —
 *  no endpoint for 'my reports list' exists (citizen auth is OTP/token-based, not session-listing) —
 *  DO NOT build a 'my reports' list backed by an API call that doesn't exist."
 */

export interface CitizenRecentReport {
  token: string;
  submittedAt?: string;
  summary?: string;
  ward?: string;
  category?: string;
}

const STORAGE_KEY = 'civicbrain_citizen_recent_reports_v1';

export const getRecentReports = async (): Promise<CitizenRecentReport[]> => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      return parsed.slice(0, 5); // Most recent items
    }
    return [];
  } catch {
    // On cache read failure, fail silently and return empty array per SCREEN_SPECS.md §2.1
    return [];
  }
};

export const saveRecentReport = async (report: CitizenRecentReport): Promise<void> => {
  try {
    const existing = await getRecentReports();
    const filtered = existing.filter(r => r.token !== report.token);
    filtered.unshift({
      ...report,
      submittedAt: report.submittedAt || new Date().toISOString(),
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered.slice(0, 10)));
  } catch {
    // Gracefully handle storage quota or private browsing exceptions
  }
};

export const removeRecentReport = async (token: string): Promise<void> => {
  try {
    const existing = await getRecentReports();
    const filtered = existing.filter(r => r.token !== token);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
  } catch {
    // Gracefully ignore
  }
};
