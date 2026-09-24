import React from 'react';
import { useParams, Link } from 'react-router-dom';

export const SyncStatusView: React.FC = () => {
  const params = useParams();
  return (
    <div className="space-y-4">
      <div className="pb-3 border-b border-border flex items-center justify-between">
        <div>
          <h1 className="font-ui text-xl font-bold text-primary">Sync Status</h1>
          <p className="font-mono text-xs text-secondary mt-1">Route: /sync</p>
        </div>
      </div>
      <div className="p-4 border border-dashed border-border rounded-md text-secondary font-mono text-sm bg-surface">
        Karmi Sahayak field screen scaffold.
        {Object.keys(params).length > 0 && (
          <div className="mt-2 text-primary font-mono text-xs">
            Params: {JSON.stringify(params)}
          </div>
        )}
      </div>
    </div>
  );
};
