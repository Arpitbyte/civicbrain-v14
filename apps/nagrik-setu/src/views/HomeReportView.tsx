import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  TrackingTokenDisplay,
  Skeleton,
} from '@civicbrain/ui';
import { Camera, Search, ArrowRight, Clock, ShieldCheck, PlusCircle } from 'lucide-react';
import { getRecentReports, saveRecentReport, clearHistoryIfEmpty, CitizenRecentReport } from '../services/citizenStorage';

export const HomeReportView: React.FC = () => {
  const navigate = useNavigate();
  const [recentReports, setRecentReports] = useState<CitizenRecentReport[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    getRecentReports()
      .then((reports) => {
        if (isMounted) {
          setRecentReports(reports.slice(0, 2)); // strictly up to 2 recent per SCREEN_SPECS.md §2.1
          setIsLoading(false);
        }
      })
      .catch(() => {
        // Cache read fails -> CTA-only, silent per SCREEN_SPECS.md §2.1
        if (isMounted) {
          setRecentReports([]);
          setIsLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const handleAddSampleToken = async () => {
    const sample: CitizenRecentReport = {
      token: 'CB-2026-W14-8892',
      submittedAt: new Date().toLocaleDateString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
      }),
      summary: 'Ward 14 · Indiranagar (Roads & Drains split)',
      ward: 'Ward 14',
      category: 'Roads / Pothole',
    };
    await saveRecentReport(sample);
    const updated = await getRecentReports();
    setRecentReports(updated.slice(0, 2));
  };

  return (
    <div className="w-full max-w-[640px] mx-auto flex flex-col gap-6 font-ui">
      {/* Visual Header & Civic Context */}
      <div className="flex flex-col gap-1.5 pt-2">
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 text-xs font-mono font-medium text-text-secondary uppercase tracking-wider">
            <ShieldCheck className="w-3.5 h-3.5 text-action-primary" />
            <span>MUNICIPAL PUBLIC SERVICE PORTAL</span>
          </span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-primary">
          नागरिक सेवा पोर्टल
        </h1>
        <p className="text-sm text-text-secondary leading-relaxed">
          Report municipal issues directly to your ward office or track field work orders with live, verifiable waybill tokens.
        </p>
      </div>

      {/* Primary Fork CTAs */}
      <div className="flex flex-col gap-4 mt-2">
        {/* Primary Action Card: Report an Issue */}
        <button
          type="button"
          onClick={() => navigate('/report/new/capture')}
          aria-label="Report an issue to your ward office"
          className="
            group relative w-full text-left p-6 sm:p-7 rounded-lg
            bg-surface border-2 border-action-primary shadow-flat
            cursor-pointer select-none
            transition-transform duration-base ease-standard
            active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus
          "
        >
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-md bg-marker-500 text-station-950 flex items-center justify-center shrink-0 shadow-sm">
                <Camera className="w-6 h-6 stroke-[2.2]" />
              </div>
              <div className="flex flex-col">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-lg text-primary tracking-tight">
                    Report an Issue
                  </span>
                  <span className="text-xs font-medium px-2 py-0.5 rounded bg-surface-raised border border-border text-text-secondary">
                    समस्या दर्ज करें
                  </span>
                </div>
                <p className="text-sm text-text-secondary mt-1 leading-normal">
                  Photograph, dictate, or describe a civic defect in your area. GPS and ward routing are automated.
                </p>
              </div>
            </div>

            <div className="hidden sm:flex items-center justify-center w-8 h-8 rounded-full bg-surface-raised border border-border text-primary group-hover:translate-x-0.5 transition-transform">
              <ArrowRight className="w-4 h-4" />
            </div>
          </div>
        </button>

        {/* Secondary Action Card: Track My Report */}
        <button
          type="button"
          onClick={() => navigate('/track')}
          aria-label="Track an existing report using a waybill token"
          className="
            group relative w-full text-left p-5 sm:p-6 rounded-lg
            bg-surface border border-border hover:border-action-primary shadow-flat
            cursor-pointer select-none
            transition-all duration-base ease-standard
            active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus
          "
        >
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-md bg-surface-raised border border-border text-primary flex items-center justify-center shrink-0">
                <Search className="w-5 h-5 stroke-[2]" />
              </div>
              <div className="flex flex-col">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-base text-primary">
                    Track My Report
                  </span>
                  <span className="text-xs text-text-secondary">
                    स्थिति जांचें
                  </span>
                </div>
                <p className="text-xs sm:text-sm text-text-secondary mt-0.5">
                  Enter your tracking token or registered phone number to verify progress.
                </p>
              </div>
            </div>

            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-surface-raised text-text-secondary group-hover:text-primary group-hover:translate-x-0.5 transition-all">
              <ArrowRight className="w-4 h-4" />
            </div>
          </div>
        </button>
      </div>

      {/* Recent Field Waybills Section (SCREEN_SPECS.md §2.1: up to 2 recent stubs inline, real data only) */}
      <div className="flex flex-col gap-3 mt-4 pt-4 border-t border-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-semibold text-text-secondary uppercase tracking-wider font-mono">
            <Clock className="w-3.5 h-3.5 text-action-primary" />
            <span>Recent Device Waybills</span>
          </div>

          {recentReports.length > 0 && (
            <span className="text-xs text-text-secondary font-mono">
              Local cache ({recentReports.length}/2)
            </span>
          )}
        </div>

        {/* State: Loading */}
        {isLoading && (
          <div className="flex flex-col gap-3">
            <Skeleton className="w-full h-24 rounded-md" />
          </div>
        )}

        {/* State: Empty (No past reports -> CTA-only per SCREEN_SPECS.md §2.1) */}
        {!isLoading && recentReports.length === 0 && (
          <div className="p-4 rounded-md bg-surface border border-dashed border-border flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-text-secondary">
            <span>No reports filed on this device yet. Tokens from submitted reports will appear here as quick-access stubs.</span>
            <button
              type="button"
              onClick={handleAddSampleToken}
              className="inline-flex items-center gap-1 font-mono text-xs font-semibold text-action-primary hover:underline shrink-0"
            >
              <PlusCircle className="w-3.5 h-3.5" />
              <span>Load sample stub</span>
            </button>
          </div>
        )}

        {/* State: Populated with up to 2 recent stubs */}
        {!isLoading && recentReports.length > 0 && (
          <div className="flex flex-col gap-3">
            {recentReports.map((report) => (
              <div
                key={report.token}
                onClick={() => navigate(`/track/${encodeURIComponent(report.token)}`)}
                className="cursor-pointer group"
                role="link"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    navigate(`/track/${encodeURIComponent(report.token)}`);
                  }
                }}
              >
                <TrackingTokenDisplay
                  token={report.token}
                  timestamp={report.submittedAt}
                  summary={report.summary || report.ward}
                  size="sm"
                  className="group-hover:border-action-primary transition-colors"
                />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
