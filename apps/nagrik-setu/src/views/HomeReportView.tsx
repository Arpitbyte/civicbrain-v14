import React from 'react';
import { useParams, Link } from 'react-router-dom';

export const HomeReportView: React.FC = () => {
  const params = useParams();
  return (
    <div className="space-y-4">
      <div className="pb-3 border-b border-border">
        <h1 className="font-ui text-xl font-semibold text-primary">Home / Report an Issue</h1>
        <p className="font-mono text-xs text-secondary mt-1">Route: /</p>
      </div>
      <div className="p-6 border border-dashed border-border rounded-md text-secondary font-mono text-sm bg-surface">
        Citizen screen scaffold ready for Prompt implementation.
        {Object.keys(params).length > 0 && (
          <div className="mt-2 text-primary font-mono text-xs">
            Token / Params: {JSON.stringify(params)}
          </div>
        )}
      </div>
    </div>
  );
};
