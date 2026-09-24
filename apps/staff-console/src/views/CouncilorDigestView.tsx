import React from 'react';
import { useParams } from 'react-router-dom';

export const CouncilorDigestView: React.FC = () => {
  const params = useParams();
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-border">
        <div>
          <h1 className="font-ui text-xl font-semibold text-primary">Councilor Digest</h1>
          <p className="font-mono text-xs text-secondary mt-1">Route: /corporator/digest</p>
        </div>
        <div className="flex gap-2">
          <span key="corporator" className="font-mono text-xs px-2 py-0.5 bg-surface text-secondary border border-border rounded-sm">corporator</span>
          <span key="admin" className="font-mono text-xs px-2 py-0.5 bg-surface text-secondary border border-border rounded-sm">admin</span>
        </div>
      </div>
      <div className="p-6 border border-dashed border-border rounded-md text-secondary font-mono text-sm">
        Screen scaffold for Councilor Digest ready for implementation in later prompts.
        {Object.keys(params).length > 0 && <div className="mt-2 text-primary font-mono text-xs">Params: {JSON.stringify(params)}</div>}
      </div>
    </div>
  );
};
