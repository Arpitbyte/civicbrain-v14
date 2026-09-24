import React, { useState } from 'react';
import { MapPin, Calendar, ShieldCheck, Eye, EyeOff } from 'lucide-react';

export interface EvidencePhotoCardProps {
  /**
   * Primary image URL
   */
  src: string;
  /**
   * Responsive srcset string
   */
  srcSet?: string;
  /**
   * Accessible description of the civic evidence (e.g. "Pothole on 80ft Road, Indiranagar").
   * Never generic "photo" or filename per DESIGN.md §12.
   */
  alt: string;
  /**
   * Formatted GPS coordinates string (e.g. "12.9716° N, 77.5946° E")
   */
  coordinates?: string;
  /**
   * ISO timestamp or formatted capture time
   */
  timestamp?: string;
  /**
   * Whether automated PII blurring/redaction (faces/plates) was applied
   */
  isRedacted?: boolean;
  /**
   * Low-resolution blur-up placeholder data URL or small thumbnail
   */
  blurDataUrl?: string;
  /**
   * Optional caption label or department badge
   */
  caption?: string;
  className?: string;
}

/**
 * EvidencePhotoCard
 * Conforms strictly to DESIGN.md §7:
 * - Real evidence photography: 4:3 or native aspect preserved (never force-cropped to a square)
 * - Shown full width within a bordered card, NOT a rounded thumbnail
 * - GPS + timestamp burned into a Plex Mono caption strip *below* the photo, NEVER overlaid on top of it
 * - Redaction badge (Seal-outline icon) when face/plate blurring was applied
 * - Real-pixel blur-up placeholder while loading (never generic gray box or skeleton shimmer)
 */
export const EvidencePhotoCard: React.FC<EvidencePhotoCardProps> = ({
  src,
  srcSet,
  alt,
  coordinates,
  timestamp,
  isRedacted = false,
  blurDataUrl,
  caption,
  className = '',
}) => {
  const [isLoaded, setIsLoaded] = useState(false);

  return (
    <figure
      className={`
        flex flex-col w-full bg-surface rounded-md border border-border overflow-hidden
        ${className}
      `}
    >
      {/* Photo Container with 4:3 Aspect Ratio */}
      <div className="relative w-full aspect-[4/3] bg-field-200 overflow-hidden">
        {/* Blur-up placeholder if provided */}
        {blurDataUrl && !isLoaded && (
          <img
            src={blurDataUrl}
            alt=""
            aria-hidden="true"
            className="absolute inset-0 w-full h-full object-cover filter blur-md scale-105"
          />
        )}

        {/* Real Evidence Image */}
        <img
          src={src}
          srcSet={srcSet}
          alt={alt}
          loading="lazy"
          onLoad={() => setIsLoaded(true)}
          className={`
            w-full h-full object-cover transition-opacity duration-fast ease-standard
            ${isLoaded ? 'opacity-100' : 'opacity-0'}
          `}
        />

        {/* Redaction Badge (top-right of photo) */}
        {isRedacted && (
          <div
            role="status"
            aria-label="Automated PII redaction applied (faces/license plates obscured)"
            className="
              absolute top-3 right-3 flex items-center gap-1.5 px-2 py-1
              rounded-full bg-station-900/85 text-text-inverse text-[11px] font-ui font-medium
              backdrop-blur-sm border border-border-strong/50 shadow-flat
            "
          >
            <ShieldCheck className="w-3.5 h-3.5 text-status-success" aria-hidden="true" />
            <span>Redacted</span>
          </div>
        )}
      </div>

      {/* Mono Caption Strip strictly *below* the photo (DESIGN.md §7) */}
      <figcaption className="p-3 bg-surface-raised border-t border-border flex flex-col gap-1.5 text-xs font-mono">
        <div className="flex items-center justify-between text-primary font-medium">
          {caption && <span className="font-ui text-xs font-semibold text-primary">{caption}</span>}
          {coordinates && (
            <span className="flex items-center gap-1 text-text-secondary" title="GPS Coordinates">
              <MapPin className="w-3.5 h-3.5 text-action-primary flex-shrink-0" aria-hidden="true" />
              <span>{coordinates}</span>
            </span>
          )}
        </div>

        <div className="flex items-center justify-between text-text-secondary text-[11px]">
          <span className="truncate max-w-[70%] font-ui" title={alt}>
            {alt}
          </span>
          {timestamp && (
            <span className="flex items-center gap-1 font-mono text-text-secondary flex-shrink-0" title="Capture Timestamp">
              <Calendar className="w-3 h-3 text-text-secondary" aria-hidden="true" />
              <span>{timestamp}</span>
            </span>
          )}
        </div>
      </figcaption>
    </figure>
  );
};
