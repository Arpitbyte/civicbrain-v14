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

const CitizenLayout: React.FC = () => {
  return (
    <CitizenShell bottomNavSlot={<NavTabBar />}>
      <Outlet />
    </CitizenShell>
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
