import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Button,
} from '@civicbrain/ui';
import {
  ArrowRight,
  ShieldCheck,
  CheckCircle,
  Truck,
  Droplet,
  Lightbulb,
  Trash2,
  Waves,
  HeartPulse,
} from 'lucide-react';
import { useReportDraft } from '../context/ReportDraftContext';
import { IntakeStepHeader } from '../components/IntakeStepHeader';

interface TaxonomyOption {
  code: string;
  name: string;
  nameHindi: string;
  deptCode: string;
  deptName: string;
  icon: React.ComponentType<{ className?: string }>;
  description: string;
}

const TAXONOMY_OPTIONS: TaxonomyOption[] = [
  {
    code: 'POTHOLE',
    name: 'Pothole / Road Crater',
    nameHindi: 'सड़क पर गड्ढा',
    deptCode: 'ROADS',
    deptName: 'Roads & Infrastructure (PWD)',
    icon: Truck,
    description: 'Surface depression, asphalt erosion, or deep roadway crater.',
  },
  {
    code: 'GARBAGE_BLACKSPOT',
    name: 'Garbage Dump / Overflow',
    nameHindi: 'कचरे का ढेर',
    deptCode: 'SWM',
    deptName: 'Solid Waste Management',
    icon: Trash2,
    description: 'Uncollected waste piles, overflowing bins, or illegal dumping.',
  },
  {
    code: 'DRAIN_BLOCKAGE',
    name: 'Stormwater Drain Blockage',
    nameHindi: 'नाली जाम / रुकावट',
    deptCode: 'SWD',
    deptName: 'Stormwater Drains',
    icon: Waves,
    description: 'Choked storm drain, broken culvert, or flood risk blockage.',
  },
  {
    code: 'STREETLIGHT_OUT',
    name: 'Street Light Inoperative',
    nameHindi: 'स्ट्रीट लाइट बंद',
    deptCode: 'LIGHTING',
    deptName: 'Electrical & Street Lighting',
    icon: Lightbulb,
    description: 'Non-functional fixture, continuous day burning, or exposed wires.',
  },
  {
    code: 'WATER_LEAK',
    name: 'Water Supply Pipeline Leak',
    nameHindi: 'पानी की पाइपलाइन लीकेज',
    deptCode: 'WATER',
    deptName: 'Water Supply & Sewerage Board',
    icon: Droplet,
    description: 'High-pressure mains burst, valve leak, or sewage overflow.',
  },
  {
    code: 'STAGNANT_WATER',
    name: 'Stagnant Water / Sanitation',
    nameHindi: 'जलभराव और स्वच्छता',
    deptCode: 'HEALTH',
    deptName: 'Public Health & Sanitation',
    icon: HeartPulse,
    description: 'Standing water pools, mosquito breeding risk, or unsanitary conditions.',
  },
];

export const ReportCategoryView: React.FC = () => {
  const navigate = useNavigate();
  const { draft, updateDraft, isStep3Valid } = useReportDraft();

  const handleSelectCategory = (opt: TaxonomyOption) => {
    updateDraft({
      categoryCode: opt.code,
      categoryName: opt.name,
      departmentCode: opt.deptCode,
      departmentName: opt.deptName,
    });
  };

  return (
    <div className="w-full max-w-[640px] mx-auto flex flex-col gap-6 font-ui">
      {/* Field Notebook Header */}
      <IntakeStepHeader
        currentStep={3}
        title="What kind of issue is this?"
        subtitle="Citizen-declared classification. Select the category that best matches the defect you observed."
        backUrl="/report/new/location"
        backLabel="Back to location"
      />

      {/* Mandatory Honest Governance Notice (ANTIGRAVITY_PROMPTS.md Prompt 13 & SCREEN_SPECS.md §2.2) */}
      <div className="p-3.5 rounded-md bg-surface-raised border border-border flex items-start gap-3">
        <ShieldCheck className="w-5 h-5 text-action-primary shrink-0 mt-0.5" />
        <div className="flex flex-col gap-0.5 text-xs text-text-secondary leading-relaxed">
          <span className="font-semibold text-primary">
            Citizen-Declared Classification (नागरिक घोषित वर्गीकरण)
          </span>
          <p>
            You determine the issue classification directly. CivicBrain preserves your declaration exactly as selected and routes it directly to the responsible municipal department without automated reclassification.
          </p>
        </div>
      </div>

      {/* Category Grid */}
      <div className="flex flex-col gap-3">
        <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider font-mono">
          Select Municipal Category
        </label>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {TAXONOMY_OPTIONS.map((opt) => {
            const isSelected = draft.categoryCode === opt.code;
            const Icon = opt.icon;

            return (
              <button
                key={opt.code}
                type="button"
                onClick={() => handleSelectCategory(opt)}
                className={`
                  p-4 rounded-md border text-left flex flex-col gap-2 transition-all duration-fast
                  ${isSelected
                    ? 'bg-surface border-2 border-action-primary ring-1 ring-action-primary shadow-flat'
                    : 'bg-surface hover:bg-surface-raised border-border text-text-secondary'}
                `}
                aria-pressed={isSelected}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className={`
                      w-8 h-8 rounded flex items-center justify-center shrink-0
                      ${isSelected ? 'bg-marker-500 text-station-950 font-bold' : 'bg-surface-raised border border-border text-primary'}
                    `}>
                      <Icon className="w-4 h-4" />
                    </div>
                    <div className="flex flex-col">
                      <span className="font-semibold text-sm text-primary">
                        {opt.name}
                      </span>
                      <span className="text-[11px] text-text-secondary">
                        {opt.nameHindi}
                      </span>
                    </div>
                  </div>

                  {isSelected && (
                    <CheckCircle className="w-4 h-4 text-action-primary shrink-0" />
                  )}
                </div>

                <p className="text-xs text-text-secondary leading-normal">
                  {opt.description}
                </p>

                <div className="pt-1.5 border-t border-border/60 flex items-center justify-between text-[11px] font-mono text-text-secondary">
                  <span>Routing:</span>
                  <span className="font-semibold text-primary">{opt.deptCode}</span>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Step Navigation Actions */}
      <div className="flex items-center justify-between pt-4 border-t border-border">
        <span className="text-xs text-text-secondary font-mono">
          {isStep3Valid ? `✓ Category: ${draft.categoryCode}` : '* Please select a category to proceed'}
        </span>

        <Button
          type="button"
          variant="primary"
          size="lg"
          disabled={!isStep3Valid}
          onClick={() => navigate('/report/new/review')}
          rightIcon={<ArrowRight className="w-4 h-4" />}
        >
          Next: Review & Submit
        </Button>
      </div>
    </div>
  );
};
