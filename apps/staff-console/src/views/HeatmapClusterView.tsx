import React from 'react';
import { useParams } from 'react-router-dom';

export const HeatmapClusterView: React.FC = () => {
  const params = useParams();
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-border">
        <div>
          <h1 className="font-ui text-xl font-semibold text-primary">Heatmap / Cluster View</h1>
          <p className="font-mono text-xs text-secondary mt-1">Route: /pulse</p>
        </div>
        <div className="flex gap-2">
          <span key="zonal_supervisor" className="font-mono text-xs px-2 py-0.5 bg-surface text-secondary border border-border rounded-sm">zonal_supervisor</span>
          <span key="admin" className="font-mono text-xs px-2 py-0.5 bg-surface text-secondary border border-border rounded-sm">admin</span>
        </div>
      </div>
      <div className="p-6 border border-dashed border-border rounded-md text-secondary font-mono text-sm">
        Screen scaffold for Heatmap / Cluster View ready for implementation in later prompts.
        {Object.keys(params).length > 0 && <div className="mt-2 text-primary font-mono text-xs">Params: {JSON.stringify(params)}</div>}
      </div>
    </div>
  );
};
