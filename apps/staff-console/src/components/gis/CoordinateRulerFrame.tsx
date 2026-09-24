import React from 'react';

export interface CoordinateRulerFrameProps {
  children: React.ReactNode;
  center?: [number, number]; // [lon, lat]
  zoom?: number;
  className?: string;
}

/**
 * CoordinateRulerFrame
 * City Pulse's signature surveyed map frame motif per DESIGN.md §2 & SCREEN_SPECS.md §2.12:
 * "The coordinate-ruler map frame — City Pulse's signature: tick marks along the map edges
 * reinforce 'this is a surveyed space,' not a generic map widget. Channel-teal chrome
 * around a Field-paper map frame."
 */
export const CoordinateRulerFrame: React.FC<CoordinateRulerFrameProps> = ({
  children,
  center = [77.5946, 12.9716],
  zoom = 13,
  className = '',
}) => {
  // Generate dynamic surveyed coordinate marks based on current center
  const lon = center[0];
  const lat = center[1];

  const topTicks = [
    `${(lon - 0.03).toFixed(4)}° E`,
    `${(lon - 0.015).toFixed(4)}° E`,
    `${lon.toFixed(4)}° E [DATUM]`,
    `${(lon + 0.015).toFixed(4)}° E`,
    `${(lon + 0.03).toFixed(4)}° E`,
  ];

  const leftTicks = [
    `${(lat + 0.02).toFixed(4)}° N`,
    `${(lat + 0.01).toFixed(4)}° N`,
    `${lat.toFixed(4)}° N [CENTER]`,
    `${(lat - 0.01).toFixed(4)}° N`,
    `${(lat - 0.02).toFixed(4)}° N`,
  ];

  return (
    <div
      className={`relative flex flex-col w-full h-full bg-field-50 border-2 border-channel-600/40 rounded-none overflow-hidden select-none ${className}`}
      data-testid="coordinate-ruler-frame"
    >
      {/* Top Coordinate Ruler */}
      <div className="h-6 w-full bg-field-100/90 border-b border-channel-600/30 flex items-center justify-between px-6 text-[10px] font-mono text-channel-700 shrink-0 z-20">
        <div className="flex items-center gap-1.5 font-semibold tracking-wider text-channel-800">
          <span className="inline-block w-2 h-2 border border-channel-600 bg-channel-500/20" />
          <span>SURVEY_GRID // WGS-84</span>
        </div>
        <div className="hidden sm:flex items-center gap-6 text-[10px]">
          {topTicks.map((tick, i) => (
            <div key={i} className="flex flex-col items-center">
              <span>{tick}</span>
              <span className="w-px h-1.5 bg-channel-600/40" />
            </div>
          ))}
        </div>
        <div className="font-mono text-[10px] text-secondary">
          SCALE: 1:{Math.round(25000 / Math.pow(1.2, zoom - 10))}
        </div>
      </div>

      <div className="relative flex flex-1 w-full overflow-hidden">
        {/* Left Coordinate Ruler */}
        <div className="hidden md:flex w-7 bg-field-100/90 border-r border-channel-600/30 flex-col items-center justify-between py-6 text-[9px] font-mono text-channel-700 shrink-0 z-20">
          {leftTicks.map((tick, i) => (
            <div key={i} className="flex items-center gap-1 -rotate-90 origin-center whitespace-nowrap">
              <span className="w-1.5 h-px bg-channel-600/40" />
              <span>{tick}</span>
            </div>
          ))}
        </div>

        {/* Map Viewport Area */}
        <div className="relative flex-1 w-full h-full overflow-hidden bg-field-50">
          {children}

          {/* Surveying Corner Crosshairs */}
          <div className="absolute top-3 left-3 pointer-events-none z-10 text-channel-600/60 font-mono text-xs">
            +
          </div>
          <div className="absolute top-3 right-3 pointer-events-none z-10 text-channel-600/60 font-mono text-xs">
            +
          </div>
          <div className="absolute bottom-3 left-3 pointer-events-none z-10 text-channel-600/60 font-mono text-xs">
            +
          </div>
          <div className="absolute bottom-3 right-3 pointer-events-none z-10 text-channel-600/60 font-mono text-xs">
            +
          </div>
        </div>
      </div>

      {/* Bottom Status / Legend Bar */}
      <div className="h-5 w-full bg-field-100/90 border-t border-channel-600/30 flex items-center justify-between px-4 text-[10px] font-mono text-secondary shrink-0 z-20">
        <div className="flex items-center gap-4">
          <span className="text-channel-800 font-medium">CRS: EPSG:4326</span>
          <span className="hidden sm:inline">DBSCAN PROJECTION: PLANAR (~100m EPS)</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="inline-block w-1.5 h-1.5 rounded-full bg-status-success" />
          <span>SPATIAL_INDEX: READY</span>
        </div>
      </div>
    </div>
  );
};
