import React from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  Outlet,
} from 'react-router-dom';
import { CitizenShell, NavTabBar } from '@civicbrain/ui';

import { HomeReportView } from './views/HomeReportView';
import { ReportCaptureView } from './views/ReportCaptureView';
import { ReportLocationView } from './views/ReportLocationView';
import { ReportCategoryView } from './views/ReportCategoryView';
import { ReportReviewView } from './views/ReportReviewView';
import { TrackLookupView } from './views/TrackLookupView';
import { TrackDetailView } from './views/TrackDetailView';
import { ResolutionConfirmView } from './views/ResolutionConfirmView';
import { ResolutionDisputeView } from './views/ResolutionDisputeView';
import { ReportDraftProvider } from './context/ReportDraftContext';

const LanguageSwitcher: React.FC = () => {
  const [lang, setLang] = React.useState<'en' | 'hi' | 'kn'>('en');
  return (
    <div
      role="group"
      aria-label="Select portal language"
      className="flex items-center gap-1 bg-surface-raised p-0.5 rounded border border-border text-xs font-medium"
    >
      <button
        type="button"
        onClick={() => setLang('en')}
        className={`px-2 py-0.5 rounded-sm transition-colors ${
          lang === 'en' ? 'bg-surface text-primary font-semibold shadow-xs' : 'text-text-secondary hover:text-primary'
        }`}
        aria-label="Switch to English"
        aria-pressed={lang === 'en'}
      >
        EN
      </button>
      <button
        type="button"
        onClick={() => setLang('hi')}
        className={`px-2 py-0.5 rounded-sm transition-colors ${
          lang === 'hi' ? 'bg-surface text-primary font-semibold shadow-xs' : 'text-text-secondary hover:text-primary'
        }`}
        aria-label="Switch to Hindi"
        aria-pressed={lang === 'hi'}
      >
        हिन्दी
      </button>
      <button
        type="button"
        onClick={() => setLang('kn')}
        className={`px-2 py-0.5 rounded-sm transition-colors ${
          lang === 'kn' ? 'bg-surface text-primary font-semibold shadow-xs' : 'text-text-secondary hover:text-primary'
        }`}
        aria-label="Switch to Kannada"
        aria-pressed={lang === 'kn'}
      >
        ಕನ್ನಡ
      </button>
    </div>
  );
};

const CitizenLayout: React.FC = () => {
  return (
    <ReportDraftProvider>
      <CitizenShell
        headerSlot={<LanguageSwitcher />}
        bottomNavSlot={<NavTabBar />}
      >
        <Outlet />
      </CitizenShell>
    </ReportDraftProvider>
  );
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CitizenLayout />}>
          <Route index element={<HomeReportView />} />
          <Route path="report/new/capture" element={<ReportCaptureView />} />
          <Route path="report/new/location" element={<ReportLocationView />} />
          <Route path="report/new/category" element={<ReportCategoryView />} />
          <Route path="report/new/review" element={<ReportReviewView />} />
          <Route path="track" element={<TrackLookupView />} />
          <Route path="track/:token" element={<TrackDetailView />} />
          <Route path="track/:token/confirm" element={<ResolutionConfirmView />} />
          <Route path="track/:token/dispute" element={<ResolutionDisputeView />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};
