import React, { useEffect, useState } from 'react';

export interface WardBoundaryMapLayerProps {
  /**
   * Ward boundary GeoJSON feature collection or single Polygon
   */
  data?: any;
  /**
   * Source and layer ID prefix
   */
  layerId?: string;
  /**
   * Whether the layer is visible
   */
  visible?: boolean;
}

export interface IncidentPointLayerProps {
  /**
   * Incident GeoJSON point feature collection
   */
  data?: any;
  layerId?: string;
  onPointClick?: (feature: any) => void;
  visible?: boolean;
}

export interface ClusterLayerProps {
  /**
   * Cluster GeoJSON feature collection (e.g. DBSCAN clusters)
   */
  data?: any;
  layerId?: string;
  onClusterClick?: (feature: any) => void;
  visible?: boolean;
}

/**
 * Dynamic MapLibre Engine Loader
 * Conforms to UI_ARCHITECTURE.md §13 & DESIGN.md §13:
 * - MapLibre is dynamically imported, NEVER bundled into the shared main package bundle!
 * - Loads map styling and canvas context asynchronously.
 */
export const useMapLibre = () => {
  const [maplibre, setMaplibre] = useState<any>(null);
  const [isSupported, setIsSupported] = useState<boolean>(true);

  useEffect(() => {
    let mounted = true;
    const pkg = 'maplibre-gl';
    // Dynamic import evaluated at runtime on map-bearing routes only (UI_ARCHITECTURE.md §13 & DESIGN.md §13)
    import(/* @vite-ignore */ pkg)
      .then((mod) => {
        if (mounted) setMaplibre(mod);
      })
      .catch((err) => {
        console.warn('[MapLibre Dynamic Import] WebGL or library not loaded:', err);
        if (mounted) setIsSupported(false);
      });
    return () => {
      mounted = false;
    };
  }, []);

  return { maplibre, isSupported };
};

/**
 * WardBoundaryMapLayer
 * Tokens from DESIGN.md §3.4:
 * --map-line-ward-boundary: 1.5px dashed var(--color-gis-ward-boundary)
 */
export const WardBoundaryMapLayer: React.FC<WardBoundaryMapLayerProps> = ({
  data,
  layerId = 'ward-boundary-layer',
  visible = true,
}) => {
  return (
    <div
      data-layer-type="ward-boundary"
      data-layer-id={layerId}
      className="hidden"
      aria-hidden="true"
    >
      {/* Declarative configuration wrapper for dynamic map canvas integration */}
      {JSON.stringify({
        id: layerId,
        type: 'line',
        paint: {
          'line-color': 'var(--color-gis-ward-boundary)',
          'line-width': 1.5,
          'line-dasharray': [2, 2],
        },
        layout: { visibility: visible ? 'visible' : 'none' },
        hasData: Boolean(data),
      })}
    </div>
  );
};

/**
 * IncidentPointLayer
 * Tokens from DESIGN.md §3.4:
 * --map-point-radius-incident: 6px
 * --color-gis-incident-point: var(--marker-500)
 */
export const IncidentPointLayer: React.FC<IncidentPointLayerProps> = ({
  data,
  layerId = 'incident-point-layer',
  visible = true,
}) => {
  return (
    <div
      data-layer-type="incident-point"
      data-layer-id={layerId}
      className="hidden"
      aria-hidden="true"
    >
      {JSON.stringify({
        id: layerId,
        type: 'circle',
        paint: {
          'circle-radius': 6,
          'circle-color': 'var(--color-gis-incident-point)',
          'circle-stroke-width': 1.5,
          'circle-stroke-color': 'var(--color-surface)',
        },
        layout: { visibility: visible ? 'visible' : 'none' },
        hasData: Boolean(data),
      })}
    </div>
  );
};

/**
 * ClusterLayer
 * Tokens from DESIGN.md §3.4:
 * --map-point-radius-cluster: clamp(8px, calc(8px + sqrt(var(--cluster-count)) * 1.5px), 28px)
 * --color-gis-cluster-fill: var(--marker-500)
 */
export const ClusterLayer: React.FC<ClusterLayerProps> = ({
  data,
  layerId = 'cluster-layer',
  visible = true,
}) => {
  return (
    <div
      data-layer-type="cluster"
      data-layer-id={layerId}
      className="hidden"
      aria-hidden="true"
    >
      {JSON.stringify({
        id: layerId,
        type: 'circle',
        paint: {
          'circle-radius': [
            'interpolate',
            ['linear'],
            ['get', 'point_count'],
            2,
            8,
            50,
            28,
          ],
          'circle-color': 'var(--color-gis-cluster-fill)',
          'circle-opacity': 0.75,
          'circle-stroke-width': 2,
          'circle-stroke-color': 'var(--color-gis-selected-ring)',
        },
        layout: { visibility: visible ? 'visible' : 'none' },
        hasData: Boolean(data),
      })}
    </div>
  );
};
