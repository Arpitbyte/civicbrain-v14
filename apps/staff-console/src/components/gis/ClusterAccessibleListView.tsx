import React from 'react';
import { ConfidenceBadge, Button } from '@civicbrain/ui';
import { ClusterData } from './ClusterStatsPanel';
import { MapPin, ArrowRight } from 'lucide-react';

export interface ClusterAccessibleListViewProps {
  clusters: ClusterData[];
  selectedClusterId: number | null;
  onSelectCluster: (cluster: ClusterData) => void;
  calculateRadius: (count: number) => number;
}

/**
 * ClusterAccessibleListView
 * Accessible alternative to canvas/WebGL map visualization per SCREEN_SPECS.md §2.12:
 * "cluster stats panel content is available to screen readers independent of the map canvas
 * (map itself is inherently limited for a11y — the data must be reachable another way,
 * e.g. a toggleable list view of the same cluster data)."
 */
export const ClusterAccessibleListView: React.FC<ClusterAccessibleListViewProps> = ({
  clusters,
  selectedClusterId,
  onSelectCluster,
  calculateRadius,
}) => {
  return (
    <div
      role="region"
      aria-label="Detected spatial clusters accessible list view"
      className="p-4 sm:p-6 space-y-4 max-w-5xl mx-auto font-ui text-primary"
    >
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-border">
        <div>
          <h2 className="text-lg font-semibold tracking-tight text-primary">
            Detected Hotspot Clusters ({clusters.length})
          </h2>
          <p className="text-xs text-secondary font-mono mt-0.5">
            DBSCAN density clusters (ε=100m, min_pts=3)
          </p>
        </div>
        <div className="text-xs font-mono text-secondary bg-surface px-2.5 py-1 border border-border rounded-sm">
          A11Y_MODE: SCREEN_READER_PARITY_ACTIVE
        </div>
      </div>

      <div className="overflow-x-auto border border-border rounded-md bg-surface">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-border bg-field-100/70 text-secondary font-mono uppercase tracking-wider">
              <th scope="col" className="p-3 font-medium">Cluster ID</th>
              <th scope="col" className="p-3 font-medium">Centroid (Lat, Lon)</th>
              <th scope="col" className="p-3 font-medium">Points</th>
              <th scope="col" className="p-3 font-medium">Calc. Radius</th>
              <th scope="col" className="p-3 font-medium">Dominant Category</th>
              <th scope="col" className="p-3 font-medium">Confidence Score</th>
              <th scope="col" className="p-3 font-medium text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {clusters.map((cluster) => {
              const isSelected = selectedClusterId === cluster.cluster_id;
              const radius = calculateRadius(cluster.incident_count);
              const [lon, lat] = cluster.centroid.coordinates;

              return (
                <tr
                  key={cluster.cluster_id}
                  className={`transition-colors hover:bg-field-50/50 ${
                    isSelected ? 'bg-channel-500/10 font-medium' : ''
                  }`}
                  aria-selected={isSelected}
                >
                  <td className="p-3 font-mono font-semibold text-primary">
                    <div className="flex items-center gap-1.5">
                      <span
                        className="inline-block w-2 h-2 rounded-full bg-status-danger shrink-0"
                        aria-hidden="true"
                      />
                      <span>Cluster #{cluster.cluster_id}</span>
                    </div>
                  </td>
                  <td className="p-3 font-mono text-secondary whitespace-nowrap">
                    <span className="flex items-center gap-1">
                      <MapPin className="w-3 h-3 text-secondary" aria-hidden="true" />
                      <span>{lat.toFixed(4)}° N, {lon.toFixed(4)}° E</span>
                    </span>
                  </td>
                  <td className="p-3 font-mono text-primary font-bold">
                    {cluster.incident_count}
                  </td>
                  <td className="p-3 font-mono text-secondary">
                    {radius.toFixed(1)}px
                  </td>
                  <td className="p-3 text-primary">
                    <span className="inline-block px-2 py-0.5 bg-field-100 border border-border rounded-sm text-[11px]">
                      {cluster.dominant_category}
                    </span>
                  </td>
                  <td className="p-3">
                    <ConfidenceBadge
                      score={cluster.confidence_score}
                      sampleSize={cluster.incident_count}
                      compact
                    />
                  </td>
                  <td className="p-3 text-right">
                    <Button
                      variant={isSelected ? 'primary' : 'outline'}
                      size="sm"
                      onClick={() => onSelectCluster(cluster)}
                      aria-label={`Inspect Cluster #${cluster.cluster_id} details`}
                    >
                      <span>{isSelected ? 'Selected' : 'Inspect'}</span>
                      <ArrowRight className="w-3 h-3 ml-1" aria-hidden="true" />
                    </Button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
