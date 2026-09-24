import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  ScoreBreakdown,
  Button,
  Badge,
  Skeleton,
  SealMark,
} from '@civicbrain/ui';
import {
  ArrowLeft,
  ArrowRight,
  Calculator,
  RotateCcw,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  Layers,
  ShieldCheck,
  Equal,
} from 'lucide-react';

interface SubscoresState {
  severity: number;
  risk: number;
  exposure: number;
  criticality: number;
  urgency: number;
}

const DEFAULT_WEIGHTS = {
  severity: 0.35,
  risk: 0.25,
  exposure: 0.15,
  criticality: 0.15,
  urgency: 0.10,
};

export const PrioritizationReRunView: React.FC = () => {
  const { id = 'INC-8892' } = useParams<{ id: string }>();
  const navigate = useNavigate();

  // Baseline "Before" State
  const [baselineSubscores] = useState<SubscoresState>({
    severity: 0.60,
    risk: 0.40,
    exposure: 0.50,
    criticality: 0.70,
    urgency: 0.30,
  });
  const [baselineEquityBoost] = useState<number>(0.15);
  const [baselineConfidence] = useState<number>(0.85);

  const calculateScore = (subs: SubscoresState, weights: typeof DEFAULT_WEIGHTS, boost: number) => {
    const raw =
      subs.severity * weights.severity +
      subs.risk * weights.risk +
      subs.exposure * weights.exposure +
      subs.criticality * weights.criticality +
      subs.urgency * weights.urgency;
    const finalScore = Math.min(1.0, raw * (1 + boost));
    return { raw: Number(raw.toFixed(4)), final: Number(finalScore.toFixed(4)) };
  };

  const baselineCalc = calculateScore(baselineSubscores, DEFAULT_WEIGHTS, baselineEquityBoost);

  // Editable "After" Draft State
  const [subscores, setSubscores] = useState<SubscoresState>({ ...baselineSubscores });
  const [equityBoost, setEquityBoost] = useState<number>(baselineEquityBoost);
  const [confidenceScore, setConfidenceScore] = useState<number>(baselineConfidence);

  const [isEvaluating, setIsEvaluating] = useState<boolean>(false);
  const [evaluatedScore, setEvaluatedScore] = useState<{ raw: number; final: number } | null>(null);
  const [isCommitted, setIsCommitted] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Run initial calculation on mount
  useEffect(() => {
    setEvaluatedScore(calculateScore(subscores, DEFAULT_WEIGHTS, equityBoost));
  }, []);

  const handleSubscoreChange = (key: keyof SubscoresState, value: number) => {
    setSubscores((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  // STRICT RULE (SCREEN_SPECS.md §2.7 & DESIGN.md §10):
  // "Quiet — the diff appears once data returns, no fake 'calculating' delay"
  const handleReEvaluate = async () => {
    setError(null);
    setIsEvaluating(true);

    try {
      // Direct fast evaluation against real math (no artificial timer)
      const res = calculateScore(subscores, DEFAULT_WEIGHTS, equityBoost);
      setEvaluatedScore(res);
      setIsEvaluating(false);
    } catch (err: any) {
      setError(err?.message || 'Error executing prioritization re-run');
      setIsEvaluating(false);
    }
  };

  const handleResetToBaseline = () => {
    setSubscores({ ...baselineSubscores });
    setEquityBoost(baselineEquityBoost);
    setConfidenceScore(baselineConfidence);
    setEvaluatedScore(baselineCalc);
    setError(null);
  };

  const handleCommitScore = () => {
    setIsCommitted(true);
  };

  const currentFinal = evaluatedScore?.final ?? baselineCalc.final;
  const delta = Number((currentFinal - baselineCalc.final).toFixed(4));
  const isUnchanged = Math.abs(delta) < 0.0001;

  // Criteria that moved between baseline and edited draft
  const movedCriteria = (Object.keys(baselineSubscores) as (keyof SubscoresState)[]).filter(
    (key) => Math.abs(baselineSubscores[key] - subscores[key]) > 0.001
  );

  // COMMITTED SUCCESS STATE
  if (isCommitted) {
    return (
      <div className="w-full max-w-[800px] mx-auto py-8 px-4 flex flex-col gap-6 font-ui animate-in fade-in duration-deliberate">
        <SealMark
          authority="BRUHAT BENGALURU MAHANAGARA PALIKE"
          label="AHP PRIORITIZATION RE-CALIBRATION COMMITTED"
          hash={`0xAHP_${Math.random().toString(16).substring(2, 10).toUpperCase()}`}
          timestamp={new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}
          size="lg"
        />

        <div className="flex flex-col gap-2 text-center items-center">
          <h2 className="text-2xl font-bold text-primary tracking-tight">
            Priority Score Re-calibrated
          </h2>
          <p className="text-sm text-text-secondary max-w-md leading-relaxed">
            The new glass-box priority score has been committed to the incident case file and logged in the municipal audit trail.
          </p>
        </div>

        {/* Ledger Summary Box */}
        <div className="p-5 rounded-md bg-surface border border-border shadow-flat flex flex-col sm:flex-row items-center justify-between gap-4 font-mono">
          <div className="flex flex-col">
            <span className="text-xs text-text-secondary uppercase">Incident Waybill</span>
            <span className="text-sm font-bold text-primary">CB-2026-W14-{id.slice(-4)}</span>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex flex-col items-end">
              <span className="text-xs text-text-secondary uppercase">Previous Score</span>
              <span className="text-sm line-through text-text-secondary">
                {baselineCalc.final.toFixed(4)}
              </span>
            </div>
            <ArrowRight className="w-4 h-4 text-action-primary" />
            <div className="flex flex-col items-start">
              <span className="text-xs text-text-secondary uppercase">Committed Score</span>
              <span className="text-sm font-bold text-action-primary">
                {currentFinal.toFixed(4)}
              </span>
            </div>
          </div>
        </div>

        <div className="flex justify-center pt-2">
          <Button
            type="button"
            variant="primary"
            size="lg"
            onClick={() => navigate(`/deck/incidents/${id}`)}
            rightIcon={<ArrowRight className="w-4 h-4" />}
          >
            Return to Incident Case File
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div
      data-workspace="command-deck"
      className="w-full max-w-[840px] mx-auto py-6 px-4 flex flex-col gap-6 font-ui"
    >
      {/* Top Header Strip */}
      <div className="flex flex-col gap-2 border-b border-border pb-3">
        <Link
          to={`/deck/incidents/${id}`}
          className="inline-flex items-center gap-1.5 text-xs font-medium text-text-secondary hover:text-primary transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Incident Case File ({id})</span>
        </Link>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Calculator className="w-5 h-5 text-action-primary" />
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-primary">
              Prioritization Re-run (पुनः प्राथमिकता मूल्यांकन)
            </h1>
          </div>
          <Badge variant="neutral" size="sm">
            Incident #{id}
          </Badge>
        </div>

        <p className="text-xs sm:text-sm text-text-secondary leading-normal">
          Manually calibrate the 5 orthogonal AHP criteria sub-scores and ward compensatory equity boost to recalculate dispatch priority.
        </p>
      </div>

      {/* Interactive Calibration Instrument Panel */}
      <div className="p-5 rounded-md bg-surface border border-border flex flex-col gap-5 shadow-flat">
        <div className="flex items-center justify-between border-b border-border pb-2">
          <span className="font-mono text-xs font-semibold text-text-secondary uppercase tracking-wider">
            5 Orthogonal Criteria Sub-scores (0.00 – 1.00)
          </span>
          <button
            type="button"
            onClick={handleResetToBaseline}
            className="inline-flex items-center gap-1 text-xs text-text-secondary hover:text-primary transition-colors font-mono"
          >
            <RotateCcw className="w-3 h-3" />
            <span>Reset to Baseline</span>
          </button>
        </div>

        {/* 5 Criteria Sliders */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {(
            [
              { key: 'severity', label: 'Severity (S) — भौतिक गंभीरता', desc: 'Direct physical hazard / crater depth' },
              { key: 'risk', label: 'Risk (R) — सुरक्षा जोखिम', desc: 'Pedestrian & vehicular injury hazard' },
              { key: 'exposure', label: 'Exposure (E) — नागरिक प्रभाव', desc: 'Traffic density and footfall exposure' },
              { key: 'criticality', label: 'Criticality (C) — महत्वपूर्णता', desc: 'Emergency / arterial route importance' },
              { key: 'urgency', label: 'Urgency (U) — तात्कालिकता', desc: 'Weather or degradation progression risk' },
            ] as const
          ).map(({ key, label, desc }) => {
            const val = subscores[key];
            const hasMoved = Math.abs(val - baselineSubscores[key]) > 0.001;

            return (
              <div
                key={key}
                className={`p-3 rounded-md border flex flex-col gap-1.5 transition-colors ${
                  hasMoved ? 'bg-marker-500/10 border-action-primary/50' : 'bg-surface-raised border-border'
                }`}
              >
                <div className="flex items-center justify-between">
                  <label htmlFor={`slider-${key}`} className="text-xs font-semibold text-primary">
                    {label}
                  </label>
                  <span className="font-mono text-xs font-bold text-action-primary">
                    {val.toFixed(2)}
                  </span>
                </div>

                <p className="text-[11px] text-text-secondary leading-tight">{desc}</p>

                <input
                  id={`slider-${key}`}
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={val}
                  onChange={(e) => handleSubscoreChange(key, parseFloat(e.target.value))}
                  className="w-full accent-action-primary cursor-pointer mt-1"
                />
              </div>
            );
          })}

          {/* Equity Boost Slider */}
          <div className="p-3 rounded-md bg-surface-raised border border-border flex flex-col gap-1.5">
            <div className="flex items-center justify-between">
              <label htmlFor="slider-equity" className="text-xs font-semibold text-primary">
                Ward Equity Boost (β) — समता बूस्ट
              </label>
              <span className="font-mono text-xs font-bold text-action-primary">
                +{Math.round(equityBoost * 100)}%
              </span>
            </div>
            <p className="text-[11px] text-text-secondary leading-tight">
              Bühlmann credibility compensation for under-reported ward equity
            </p>
            <input
              id="slider-equity"
              type="range"
              min="0"
              max="0.5"
              step="0.05"
              value={equityBoost}
              onChange={(e) => setEquityBoost(parseFloat(e.target.value))}
              className="w-full accent-action-primary cursor-pointer mt-1"
            />
          </div>
        </div>

        {/* Re-calculate Trigger */}
        <div className="flex justify-end pt-2">
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={handleReEvaluate}
            leftIcon={<Calculator className="w-3.5 h-3.5" />}
          >
            Calculate Re-run Delta
          </Button>
        </div>
      </div>

      {/* Stamped Ledger Correction (SCREEN_SPECS.md §2.7: struck-through old values, new values beside them) */}
      <div className="p-5 rounded-md bg-surface border border-border shadow-flat flex flex-col gap-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-border gap-2">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-action-primary" />
            <h2 className="text-sm font-semibold text-primary uppercase tracking-wider font-mono">
              Ledger Correction Comparison
            </h2>
          </div>

          {/* Score Delta Badge */}
          <div className="flex items-center gap-2 font-mono text-xs">
            <span className="text-text-secondary">Delta:</span>
            {isUnchanged ? (
              <Badge variant="neutral" size="sm">
                Score unchanged (±0.00)
              </Badge>
            ) : (
              <Badge variant={delta > 0 ? 'warning' : 'neutral'} size="sm">
                {delta > 0 ? `+${delta.toFixed(4)}` : delta.toFixed(4)}
              </Badge>
            )}
          </div>
        </div>

        {/* Summary Value Strikethrough Row */}
        <div className="p-3.5 rounded bg-surface-raised border border-border flex items-center justify-between font-mono text-xs">
          <span className="text-text-secondary font-medium">Composite Priority Rank</span>
          <div className="flex items-center gap-3">
            <span className="line-through text-text-secondary text-sm">
              {baselineCalc.final.toFixed(4)}
            </span>
            <ArrowRight className="w-3.5 h-3.5 text-action-primary" />
            <span className="font-bold text-base text-primary">
              {currentFinal.toFixed(4)}
            </span>
          </div>
        </div>

        {/* Moved Criteria Badges */}
        {movedCriteria.length > 0 && (
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <span className="text-text-secondary font-mono text-[11px]">Modified criteria:</span>
            {movedCriteria.map((crit) => (
              <span
                key={crit}
                className="px-2 py-0.5 rounded bg-marker-500/15 border border-marker-500/40 text-primary font-mono text-[11px]"
              >
                {crit.toUpperCase()}: {baselineSubscores[crit].toFixed(2)} → {subscores[crit].toFixed(2)}
              </span>
            ))}
          </div>
        )}

        {/* Side-by-Side ScoreBreakdowns (before / after) */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          {/* Left: Baseline Before */}
          <div className="flex flex-col gap-2">
            <div className="flex items-center justify-between text-xs font-mono text-text-secondary px-1">
              <span className="font-semibold uppercase tracking-wider text-text-secondary">
                Before (Active Baseline)
              </span>
            </div>
            <ScoreBreakdown
              priority_score={baselineCalc.final}
              raw_priority_score={baselineCalc.raw}
              equity_boost={baselineEquityBoost}
              confidence_score={baselineConfidence}
              subscores={baselineSubscores}
              weights_used={DEFAULT_WEIGHTS}
              defaultExpanded={true}
            />
          </div>

          {/* Right: Re-calibrated After */}
          <div className="flex flex-col gap-2">
            <div className="flex items-center justify-between text-xs font-mono text-action-primary px-1">
              <span className="font-semibold uppercase tracking-wider text-primary">
                After (Re-calibrated Draft)
              </span>
            </div>

            {isEvaluating ? (
              /* Loading Skeleton for After side only (SCREEN_SPECS.md §2.7) */
              <div className="p-4 rounded-md border border-border bg-surface flex flex-col gap-3">
                <Skeleton className="w-full h-8" />
                <Skeleton className="w-full h-24" />
                <Skeleton className="w-full h-16" />
              </div>
            ) : (
              <ScoreBreakdown
                priority_score={currentFinal}
                raw_priority_score={evaluatedScore?.raw ?? baselineCalc.raw}
                equity_boost={equityBoost}
                confidence_score={confidenceScore}
                subscores={subscores}
                weights_used={DEFAULT_WEIGHTS}
                defaultExpanded={true}
                className="border-action-primary/40"
              />
            )}
          </div>
        </div>
      </div>

      {/* Commit Decision Action */}
      <div className="flex items-center justify-between pt-4 border-t border-border">
        <Button
          type="button"
          variant="outline"
          size="md"
          onClick={() => navigate(`/deck/incidents/${id}`)}
        >
          Cancel & Return
        </Button>

        <Button
          type="button"
          variant="primary"
          size="lg"
          onClick={handleCommitScore}
          leftIcon={<ShieldCheck className="w-4 h-4" />}
        >
          Commit New Priority Score
        </Button>
      </div>
    </div>
  );
};
