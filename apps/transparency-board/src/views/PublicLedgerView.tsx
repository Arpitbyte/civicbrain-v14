import React from 'react';
import { useParams } from 'react-router-dom';

export const PublicLedgerView: React.FC = () => {
  const params = useParams();
  return (
    <div className="space-y-4">
      <div className="pb-3 border-b border-border">
        <h1 className="font-display text-2xl font-semibold text-primary">Public Ledger</h1>
        <p className="font-mono text-xs text-secondary mt-1">Route: /ledger</p>
      </div>
      <div className="p-6 border border-dashed border-border rounded-md text-secondary font-mono text-sm bg-surface">
        Transparency Board editorial scaffold.
        {Object.keys(params).length > 0 && (
          <div className="mt-2 text-primary font-mono text-xs">
            Params: {JSON.stringify(params)}
          </div>
        )}
      </div>
    </div>
  );
};
