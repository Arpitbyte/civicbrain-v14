import React from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  NavLink,
  Outlet,
} from 'react-router-dom';
import { EditorialShell } from '@civicbrain/ui';

import { CityFeedView } from './views/CityFeedView';
import { PublicLedgerView } from './views/PublicLedgerView';
import { CaseProvenanceChainView } from './views/CaseProvenanceChainView';
import { WardReportCardView } from './views/WardReportCardView';
import { CouncilorDigestView } from './views/CouncilorDigestView';
import { CivicAssistantView } from './views/CivicAssistantView';

const EditorialLayout: React.FC = () => {
  return (
    <EditorialShell
      topNavSlot={
        <div className="flex items-center gap-4 text-xs font-ui">
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              isActive ? 'font-semibold text-primary' : 'text-secondary hover:text-primary'
            }
          >
            City Feed
          </NavLink>
          <NavLink
            to="/ledger"
            className={({ isActive }) =>
              isActive ? 'font-semibold text-primary' : 'text-secondary hover:text-primary'
            }
          >
            Ledger
          </NavLink>
          <NavLink
            to="/assistant"
            className={({ isActive }) =>
              isActive ? 'font-semibold text-primary' : 'text-secondary hover:text-primary'
            }
          >
            Assistant
          </NavLink>
          <NavLink
            to="/corporator/digest"
            className={({ isActive }) =>
              isActive ? 'font-semibold text-primary' : 'text-secondary hover:text-primary'
            }
          >
            Digest
          </NavLink>
        </div>
      }
    >
      <Outlet />
    </EditorialShell>
  );
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<EditorialLayout />}>
          <Route index element={<CityFeedView />} />
          <Route path="ledger" element={<PublicLedgerView />} />
          <Route path="ledger/:incidentId" element={<CaseProvenanceChainView />} />
          <Route path="wards/:wardId/report-card" element={<WardReportCardView />} />
          <Route path="corporator/digest" element={<CouncilorDigestView />} />
          <Route path="assistant" element={<CivicAssistantView />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};
