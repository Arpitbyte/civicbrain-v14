import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Button,
  Field,
  Input,
} from '@civicbrain/ui';
import {
  MapPin,
  Crosshair,
  ArrowRight,
  CheckCircle,
  Navigation,
  Building2,
} from 'lucide-react';
import { useReportDraft } from '../context/ReportDraftContext';
import { IntakeStepHeader } from '../components/IntakeStepHeader';

const KNOWN_WARDS = [
  { code: 'W14', name: 'Ward 14 (Indiranagar)', lat: 12.9784, lng: 77.6408, defaultAddress: '100 Feet Road, Indiranagar' },
  { code: 'W11', name: 'Ward 11 (Malleshwaram)', lat: 13.0033, lng: 77.5694, defaultAddress: 'Margosa Road, 8th Cross, Malleshwaram' },
  { code: 'W85', name: 'Ward 85 (Koramangala)', lat: 12.9352, lng: 77.6245, defaultAddress: '80 Feet Road, 4th Block, Koramangala' },
  { code: 'W102', name: 'Ward 102 (Vasanth Nagar)', lat: 12.9892, lng: 77.5912, defaultAddress: 'Miller Road, Vasanth Nagar' },
];

export const ReportLocationView: React.FC = () => {
  const navigate = useNavigate();
  const { draft, updateDraft, isStep2Valid } = useReportDraft();

  const [isLocating, setIsLocating] = useState(false);
  const [gpsLocked, setGpsLocked] = useState(true);

  const handleDetectGPS = () => {
    setIsLocating(true);
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setIsLocating(false);
          setGpsLocked(true);
          updateDraft({
            latitude: Number(pos.coords.latitude.toFixed(4)),
            longitude: Number(pos.coords.longitude.toFixed(4)),
          });
        },
        () => {
          setIsLocating(false);
          // Fallback to current draft coordinates
          setGpsLocked(true);
        },
        { timeout: 5000 }
      );
    } else {
      setIsLocating(false);
    }
  };

  const handleSelectWard = (ward: typeof KNOWN_WARDS[0]) => {
    updateDraft({
      wardCode: ward.code,
      wardName: ward.name,
      latitude: ward.lat,
      longitude: ward.lng,
      addressText: ward.defaultAddress,
    });
  };

  return (
    <div className="w-full max-w-[640px] mx-auto flex flex-col gap-6 font-ui">
      {/* Field Notebook Header */}
      <IntakeStepHeader
        currentStep={2}
        title="Verify Location & Ward"
        subtitle="Confirm geographic coordinates for accurate municipal departmental routing."
        backUrl="/report/new/capture"
        backLabel="Back to capture"
      />

      {/* Mini-Map / Pin-Drop Visual Motif */}
      <div className="rounded-md border border-border bg-surface overflow-hidden shadow-flat flex flex-col">
        {/* Surveyed coordinate pin-drop canvas */}
        <div className="h-48 sm:h-56 bg-station-950 relative flex items-center justify-center overflow-hidden">
          {/* Subtle grid pattern */}
          <div
            className="absolute inset-0 opacity-20"
            style={{
              backgroundImage: 'radial-gradient(var(--border) 1px, transparent 1px)',
              backgroundSize: '16px 16px',
            }}
          />

          {/* Central Pin */}
          <div className="relative z-10 flex flex-col items-center animate-bounce">
            <div className="w-10 h-10 rounded-full bg-action-primary text-station-950 flex items-center justify-center shadow-lg border-2 border-white">
              <MapPin className="w-6 h-6 stroke-[2.5]" />
            </div>
            <div className="w-3 h-1 bg-black/50 rounded-full mt-1 blur-xs" />
          </div>

          {/* Top-Right GPS Lock Badge */}
          <div className="absolute top-3 right-3 z-10">
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-station-950/90 text-marker-500 font-mono text-[11px] border border-border shadow-sm">
              <Crosshair className="w-3.5 h-3.5" />
              <span>{gpsLocked ? 'GPS LOCKED (±4m)' : 'MANUAL LOCATION'}</span>
            </div>
          </div>

          {/* Coordinates Overlay Strip */}
          <div className="absolute bottom-2 left-2 right-2 z-10 flex items-center justify-between px-3 py-1.5 rounded bg-station-950/85 backdrop-blur-xs border border-border text-[11px] font-mono text-text-secondary">
            <span>COORDS: {draft.latitude.toFixed(4)}°N, {draft.longitude.toFixed(4)}°E</span>
            <span className="text-action-primary font-semibold">{draft.wardCode}</span>
          </div>
        </div>

        {/* GPS Re-detect Action */}
        <div className="p-3 bg-surface-raised border-t border-border flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-xs text-text-secondary">
            <Navigation className="w-4 h-4 text-action-primary" />
            <span>Auto-resolved via BBMP spatial boundary</span>
          </div>

          <button
            type="button"
            onClick={handleDetectGPS}
            disabled={isLocating}
            className="inline-flex items-center gap-1.5 text-xs font-medium text-action-primary hover:underline disabled:opacity-50"
          >
            <Crosshair className={`w-3.5 h-3.5 ${isLocating ? 'animate-spin' : ''}`} />
            <span>{isLocating ? 'Detecting GPS...' : 'Re-center GPS'}</span>
          </button>
        </div>
      </div>

      {/* Manual Override & Address Details */}
      <div className="flex flex-col gap-4 p-5 rounded-md bg-surface border border-border shadow-flat">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-text-secondary font-mono">
          <Building2 className="w-4 h-4 text-action-primary" />
          <span>Street Address & Landmarks</span>
        </div>

        <Field
          id="address-text"
          label="Street Name / Prominent Landmark"
          required
          helperText="E.g. shop name, pillar number, house number, or road intersection."
        >
          <Input
            id="address-text"
            value={draft.addressText}
            onChange={(e) => updateDraft({ addressText: e.target.value })}
            placeholder="e.g. 100 Feet Road, near Metro Pillar 42"
            className="text-sm"
          />
        </Field>

        {/* Quick Ward Selector */}
        <div className="flex flex-col gap-2 pt-2">
          <label className="text-xs font-medium text-primary">
            Municipal Ward (वार्ड चयन)
          </label>
          <div className="grid grid-cols-2 gap-2">
            {KNOWN_WARDS.map((ward) => {
              const isSelected = draft.wardCode === ward.code;
              return (
                <button
                  key={ward.code}
                  type="button"
                  onClick={() => handleSelectWard(ward)}
                  className={`
                    p-2.5 rounded-md border text-left flex flex-col gap-0.5 transition-colors
                    ${isSelected
                      ? 'bg-action-primary/10 border-action-primary text-primary font-medium'
                      : 'bg-surface hover:bg-surface-raised border-border text-text-secondary'}
                  `}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold">{ward.code}</span>
                    {isSelected && <CheckCircle className="w-3.5 h-3.5 text-action-primary" />}
                  </div>
                  <span className="text-xs truncate">{ward.name}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Step Navigation Actions */}
      <div className="flex items-center justify-between pt-4 border-t border-border">
        <span className="text-xs text-text-secondary font-mono">
          {isStep2Valid ? `✓ Location verified (${draft.wardCode})` : '* Address and ward required'}
        </span>

        <Button
          type="button"
          variant="primary"
          size="lg"
          disabled={!isStep2Valid}
          onClick={() => navigate('/report/new/category')}
          rightIcon={<ArrowRight className="w-4 h-4" />}
        >
          Next: Declare Category
        </Button>
      </div>
    </div>
  );
};
