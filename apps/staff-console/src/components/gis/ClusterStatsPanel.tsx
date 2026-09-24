import React from 'react';
import { ConfidenceBadge, Button, IconButton } from '@civicbrain/ui';
import { X, ExternalLink, MapPin, Layers, AlertTriangle, ArrowRight } from 'lucide-react';

export interface ClusterData {
  cluster_id: number;
  incident_count: number;
  centroid: {
    type: string;
    coordinates: [number, number]; // [lon, lat]
  };
  incident_ids: string[];
  confidence_score: number;
  dominant_category: string;
  category_breakdown: { category: string; count: number; percentage: number }[];
  severity_breakdown: { critical: number; major: number; minor: number };
  ward_name?: string;
  ward_number?: number;
}

export interface ClusterStatsPanelProps {
  cluster: ClusterData | null;
  onClose: () => void;
  onInspectIncidents?: (cluster: ClusterData) => void;
  className?: string;
}

/**
 * ClusterStatsPanel
 * Per SCREEN_SPECS.md §2.12:
 * "A floating panel (top-right, not a modal) shows the selected cluster's stats
 * (ConfidenceBadge, sample size, category mix) when a cluster is clicked.
 * Mobile: cluster stats appear as a bottom sheet on selection."
 */
export const ClusterStatsPanel: React.FC<ClusterStatsPanelProps> = ({
  cluster,
  onClose,
  onInspectIncidents,
  className = '',
}) => {
  if (!cluster) return null;

  const [lon, lat] = cluster.centroid.coordinates;

  return (
    <div
      role="region"
      aria-label={`Spatial cluster details for Cluster #${cluster.cluster_id}`}
      className={`bg-surface/95 backdrop-blur-md border border-border rounded-md shadow-lifted p-4 sm:p-5 text-primary flex flex-col gap-4 font-ui max-w-full sm:w-88 transition-all ${className}`}
      data-testid="cluster-stats-panel"
    >
      {/* Panel Header */}
      <div className="flex items-start justify-between border-b border-border pb-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="inline-block w-2.5 h-2.5 rounded-full bg-status-danger" />
            <h2 className="font-ui font-semibold text-base text-primary">
              Cluster #{cluster.cluster_id}
            </h2>
          </div>
          <div className="flex items-center gap-1.5 mt-1 font-mono text-xs text-secondary">
            <MapPin className="w-3 h-3 text-secondary shrink-0" />
            <span>
              {lat.toFixed(4)}° N, {lon.toFixed(4)}° E
            </span>
          </div>
          {cluster.ward_name && (
            <p className="font-ui text-xs text-secondary mt-0.5">
              Ward {cluster.ward_number ?? ''} — {cluster.ward_name}
            </p>
          )}
        </div>
        <IconButton
          variant="ghost"
          size="sm"
          label="Close cluster panel"
          icon={<X className="w-4 h-4" />}
          onClick={onClose}
        />
      </div>

      {/* Primary Metrics: Count & Confidence */}
      <div className="grid grid-cols-2 gap-3 p-3 bg-field-50/70 border border-border rounded-sm">
        <div>
          <div className="font-mono text-[11px] text-secondary uppercase tracking-wider">
            Point Count
          </div>
          <div className="font-mono text-2xl font-bold text-primary mt-0.5">
            {cluster.incident_count}
            <span className="text-xs font-normal text-secondary ml-1">incidents</span>
          </div>
        </div>
        <div>
          <div className="font-mono text-[11px] text-secondary uppercase tracking-wider mb-1">
            Confidence
          </div>
          <ConfidenceBadge
            score={cluster.confidence_score}
            sampleSize={cluster.incident_count}
            compact
          />
        </div>
      </div>

      {/* Severity Breakdown */}
      <div className="space-y-1.5">
        <div className="flex items-center justify-between text-xs font-medium text-secondary">
          <span>Severity Distribution</span>
          <span className="font-mono text-[11px] text-secondary">
            {cluster.severity_breakdown.critical} Crit / {cluster.severity_breakdown.major} Maj
          </span>
        </div>
        <div className="flex h-2 w-full rounded-sm overflow-hidden bg-field-200">
          <div
            style={{
              width: `${(cluster.severity_breakdown.critical / cluster.incident_count) * 100}%`,
            }}
            className="bg-status-danger"
            title={`Critical: ${cluster.severity_breakdown.critical}`}
          />
          <div
            style={{
              width: `${(cluster.severity_breakdown.major / cluster.incident_count) * 100}%`,
            }}
            className="bg-status-warning"
            title={`Major: ${cluster.severity_breakdown.major}`}
          />
          <div
            style={{
              width: `${(cluster.severity_breakdown.minor / cluster.incident_count) * 100}%`,
            }}
            className="bg-channel-500"
            title={`Minor: ${cluster.severity_breakdown.minor}`}
          />
        </div>
      </div>

      {/* Category Mix */}
      <div className="space-y-2">
        <div className="text-xs font-medium text-secondary">Category Mix</div>
        <div className="space-y-1.5">
          {cluster.category_breakdown.map((item, idx) => (
            <div key={idx} className="space-y-0.5">
              <div className="flex justify-between text-xs font-mono">
                <span className="text-primary truncate max-w-[180px]">{item.category}</span>
                <span className="text-secondary">{item.percentage}% ({item.count})</span>
              </div>
              <div className="w-full bg-field-200 h-1.5 rounded-sm overflow-hidden">
                <div
                  className="bg-channel-600 h-full rounded-sm transition-all duration-300"
                  style={{ width: `${item.percentage}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Action Footer */}
      <div className="pt-2 border-t border-border flex items-center justify-end gap-2">
        <Button
          variant="primary"
          size="sm"
          className="w-full justify-center text-xs"
          onClick={() => onInspectIncidents?.(cluster)}
        >
          <span>View {cluster.incident_count} Incidents in Queue</span>
          <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
        </Button>
      </div>
    </div>
  );
};
