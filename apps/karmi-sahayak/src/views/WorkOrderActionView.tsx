import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useOfflineSync } from '../context/OfflineSyncContext';
import { EvidencePhotoCard } from '@civicbrain/ui';
import {
  Camera,
  MapPin,
  Clock,
  AlertTriangle,
  CheckCircle2,
  Navigation,
  Upload,
  Trash2,
  ArrowLeft,
  ShieldAlert,
} from 'lucide-react';

export interface WorkOrderData {
  id: string;
  category: string;
  department: string;
  wardName: string;
  wardNumber: number;
  address: string;
  distanceKm: number;
  slaRemainingHours: number;
  citizenDescription: string;
  evidenceCoordinates: string;
  evidenceTimestamp: string;
  hasOpenConflict?: boolean;
  conflictReason?: string;
  status: 'assigned' | 'in_progress' | 'resolved';
}

// Authentic Indian Municipal Defect SVG Evidence Fixture (Never stock photography)
const CIVIC_DEFECT_SVG_DATA =
  'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600"><rect width="800" height="600" fill="%2322201d"/><path d="M 120 420 Q 280 320 440 380 T 720 460 L 680 560 L 150 560 Z" fill="%23141210" stroke="%23f59e0b" stroke-width="3" stroke-dasharray="8 4"/><circle cx="380" cy="410" r="90" fill="%230c0a09" stroke="%23ef4444" stroke-width="2"/><text x="40" y="60" fill="%23fbf8f3" font-family="monospace" font-size="20" font-weight="bold">CIVIC_DEFECT_INGEST // WARD-102</text><text x="40" y="90" fill="%23d6cebe" font-family="monospace" font-size="14">ROAD SURFACE CAVITY • DEPTH: 14CM • SEV: CRITICAL</text><rect x="580" y="30" width="180" height="36" fill="%23ef4444" rx="4"/><text x="595" y="54" fill="%23ffffff" font-family="monospace" font-size="12" font-weight="bold">PII_REDACTED [AUTO]</text></svg>';

const MOCK_WORK_ORDER: WorkOrderData = {
  id: 'WO-2026-8492',
  category: 'सड़क एवं गड्ढे (Roads & Asphalt / Deep Pothole)',
  department: 'लोक निर्माण विभाग (PWD) / Roads & Infrastructure',
  wardName: 'Rajajinagar',
  wardNumber: 102,
  address: '14th Main Rd, Near Post Office Junction',
  distanceKm: 1.2,
  slaRemainingHours: 2.25,
  citizenDescription:
    'Hazardous deep pothole on fast corner near post office. Two two-wheelers slipped during morning rain. Immediate asphalt patching requested.',
  evidenceCoordinates: '12.9784° N, 77.5621° E',
  evidenceTimestamp: '2026-09-24T05:30:00+05:30',
  hasOpenConflict: false,
  status: 'assigned',
};

export const WorkOrderActionView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { isOnline, queueStartOrder, queueResolveOrder } = useOfflineSync();

  const [order, setOrder] = useState<WorkOrderData>({
    ...MOCK_WORK_ORDER,
    id: id || MOCK_WORK_ORDER.id,
  });

  // Action state
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [offlineSavedAction, setOfflineSavedAction] = useState<string | null>(null);

  // Completion photo & notes state
  const [completionPhoto, setCompletionPhoto] = useState<{
    name: string;
    dataUrl: string;
  } | null>(null);
  const [workNotes, setWorkNotes] = useState<string>('');

  // Handle Photo selection/capture
  const handlePhotoCapture = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      setCompletionPhoto({
        name: file.name,
        dataUrl: reader.result as string,
      });
    };
    reader.readAsDataURL(file);
  };

  const handleClearPhoto = () => {
    setCompletionPhoto(null);
  };

  // Start Task Action
  const handleStartTask = async () => {
    setIsSubmitting(true);
    const result = await queueStartOrder(order.id);
    setIsSubmitting(false);

    setOrder((prev) => ({ ...prev, status: 'in_progress' }));

    if (result.queuedLocally) {
      setOfflineSavedAction('कार्य प्रारंभ (Started — queued offline)');
    }
  };

  // Resolve Task Action
  const handleResolveTask = async () => {
    if (!completionPhoto) return; // Strict block: photo required!

    setIsSubmitting(true);
    const result = await queueResolveOrder(order.id, completionPhoto, workNotes);
    setIsSubmitting(false);

    if (result.queuedLocally) {
      // Offline: Never show false "Done" or "Completed"
      setOfflineSavedAction('सहेजा गया — सिंक होगा (Saved — will sync)');
    } else {
      // Live online success
      setOrder((prev) => ({ ...prev, status: 'resolved' }));
    }
  };

  const isResolvedOnline = order.status === 'resolved' && !offlineSavedAction;
  const isOfflineSaved = Boolean(offlineSavedAction);

  return (
    <div
      data-testid="work-order-action-view"
      className="flex flex-col flex-1 max-w-md mx-auto w-full pb-24 font-ui text-primary select-none"
    >
      {/* Back Link & Karmi Sahayak Navigation Bar */}
      <div className="flex items-center justify-between pb-3 border-b border-border">
        <Link
          to="/my-orders"
          className="flex items-center gap-1.5 text-xs font-mono text-secondary hover:text-primary min-h-[48px] px-2"
          aria-label="Back to assigned work orders list"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>मेरे कार्य आदेश / My Orders</span>
        </Link>
        <div className="font-mono text-xs px-2.5 py-0.5 rounded-sm bg-surface-raised border border-border text-action-primary font-bold">
          {order.id}
        </div>
      </div>

      {/* Conflict Review Banner (SCREEN_SPECS.md §2.16) */}
      {order.hasOpenConflict && (
        <div
          role="alert"
          className="my-3 p-3 bg-status-danger/15 border-2 border-status-danger/40 rounded-md text-xs font-ui text-primary space-y-1"
        >
          <div className="flex items-center gap-2 text-status-danger font-bold uppercase tracking-wider font-mono">
            <ShieldAlert className="w-4 h-4 shrink-0" />
            <span>पर्यवेक्षक विवाद समीक्षा लंबित / Supervisor Conflict Review Pending</span>
          </div>
          <p className="text-secondary">
            A competing status was recorded by the municipal command desk. This work order is held for supervisor adjudication.
          </p>
        </div>
      )}

      {/* Offline Saved Banner (Honest offline feedback) */}
      {isOfflineSaved && (
        <div
          role="status"
          className="my-3 p-3 bg-action-primary/20 border-2 border-action-primary/50 rounded-md text-xs font-ui text-primary space-y-1"
        >
          <div className="flex items-center gap-2 text-action-primary font-bold uppercase tracking-wider font-mono">
            <Clock className="w-4 h-4 shrink-0" />
            <span>ऑफ़लाइन सुरक्षित — सिंक होगा / Saved to Local Queue</span>
          </div>
          <p className="text-field-200">
            Work order resolution recorded securely on this device. Will sync automatically with municipal dispatch when connection returns.
          </p>
        </div>
      )}

      {/* Top Context Strip: Task Details & Location */}
      <section className="my-3 p-4 bg-surface rounded-md border border-border space-y-3">
        <div>
          <div className="font-mono text-[11px] text-action-primary uppercase tracking-wider font-bold">
            {order.department}
          </div>
          <h1 className="text-lg font-bold text-primary tracking-tight mt-0.5">
            {order.category}
          </h1>
          <div className="flex items-center gap-1.5 font-mono text-xs text-secondary mt-1">
            <MapPin className="w-3.5 h-3.5 text-action-primary shrink-0" />
            <span>
              वार्ड {order.wardNumber} ({order.wardName}) • {order.address}
            </span>
          </div>
        </div>

        {/* SLA Timer Indicator (Prominent outdoor font) */}
        <div className="flex items-center justify-between p-2.5 bg-background border border-border rounded-sm">
          <div className="flex items-center gap-2 text-xs font-mono text-secondary">
            <Clock className="w-4 h-4 text-action-primary" />
            <span>एसएलए उलटी गिनती (SLA COUNTDOWN):</span>
          </div>
          <div className="font-mono text-sm font-bold text-action-primary">
            0{Math.floor(order.slaRemainingHours)}h{' '}
            {Math.round((order.slaRemainingHours % 1) * 60)}m शेष (remaining)
          </div>
        </div>

        {/* Citizen Ingest Defect Photo — Authentic Evidence Card (No stock photos) */}
        <div className="space-y-2 pt-1 border-t border-border">
          <div className="text-xs font-mono text-secondary uppercase tracking-wider">
            नागरिक शिकायत साक्ष्य (Reported Issue Evidence)
          </div>
          <EvidencePhotoCard
            src={CIVIC_DEFECT_SVG_DATA}
            alt="Citizen reported pothole defect on 14th Main Rajajinagar"
            coordinates={order.evidenceCoordinates}
            timestamp="2026-09-24 05:30 IST"
            isRedacted={true}
            caption={`"${order.citizenDescription}"`}
          />
        </div>
      </section>

      {/* Middle Stage 1: Assigned -> Navigation & Start */}
      {order.status === 'assigned' && !isOfflineSaved && (
        <section className="space-y-4 my-2">
          <div className="p-4 bg-surface rounded-md border border-border flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-sm bg-action-primary/20 border border-action-primary/40 flex items-center justify-center text-action-primary">
                <Navigation className="w-5 h-5" />
              </div>
              <div>
                <div className="font-bold text-sm text-primary">साइट पर नेविगेट करें (Navigate)</div>
                <div className="text-xs font-mono text-secondary">
                  {order.distanceKm} km from current GPS location
                </div>
              </div>
            </div>
            <a
              href={`https://maps.google.com/?q=${encodeURIComponent(order.address)}`}
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-2 text-xs font-mono font-bold text-action-primary border border-action-primary/40 rounded-sm hover:bg-action-primary/10 flex items-center justify-center min-h-[48px]"
            >
              दिशा-निर्देश (Directions)
            </a>
          </div>
        </section>
      )}

      {/* Middle Stage 2: In Progress -> Photo Capture & Resolution Notes */}
      {(order.status === 'in_progress' || isOfflineSaved) && (
        <section className="space-y-4 my-2">
          {/* Active Work In-Progress Header */}
          <div className="flex items-center justify-between p-3 bg-action-primary/10 border border-action-primary/30 rounded-md text-xs font-mono">
            <div className="flex items-center gap-2 text-action-primary font-bold">
              <span className="w-2.5 h-2.5 rounded-full bg-action-primary animate-pulse" />
              <span>कार्य प्रगति पर है / ACTIVE REPAIR IN PROGRESS</span>
            </div>
            <span className="text-secondary">ELAPSED: 18m</span>
          </div>

          {/* Completion Proof Capture (MANDATORY REQUIREMENT) */}
          <div className="p-4 bg-surface rounded-md border-2 border-border space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Camera className="w-4 h-4 text-action-primary" />
                <span className="font-bold text-sm text-primary">
                  पूर्णता प्रमाण फोटो (Completion Proof Photo)
                </span>
              </div>
              <span className="text-[11px] font-mono font-bold px-1.5 py-0.5 rounded-xs bg-status-danger/20 text-status-danger border border-status-danger/40">
                अनिवार्य (REQUIRED)
              </span>
            </div>

            {/* Photo Preview or File Input */}
            {completionPhoto ? (
              <div className="relative rounded-sm overflow-hidden border-2 border-action-primary/60 bg-background space-y-2 p-2">
                <img
                  src={completionPhoto.dataUrl}
                  alt="Captured repair completion evidence proof"
                  className="w-full h-48 object-cover rounded-xs"
                />
                <div className="flex items-center justify-between px-1 text-xs font-mono">
                  <span className="text-primary truncate max-w-[200px]">
                    {completionPhoto.name}
                  </span>
                  <button
                    onClick={handleClearPhoto}
                    className="flex items-center gap-1 text-status-danger hover:underline min-h-[48px] px-2"
                    aria-label="Remove photo and retake"
                  >
                    <Trash2 className="w-4 h-4" />
                    <span>पुनः फोटो लें (Retake)</span>
                  </button>
                </div>
              </div>
            ) : (
              <label
                htmlFor="camera-input"
                className="flex flex-col items-center justify-center p-6 border-2 border-dashed border-action-primary/50 hover:border-action-primary rounded-md bg-field-50/50 cursor-pointer min-h-[140px] text-center space-y-2 transition-colors active:bg-action-primary/10"
              >
                <div className="w-12 h-12 rounded-full bg-action-primary/20 border border-action-primary/40 flex items-center justify-center text-action-primary">
                  <Camera className="w-6 h-6" />
                </div>
                <div className="font-bold text-sm text-primary">
                  पूर्णता की फोटो लें (Capture Completion Photo)
                </div>
                <div className="text-[11px] font-mono text-secondary">
                  Tap to capture on-site completion proof
                </div>
                <input
                  id="camera-input"
                  type="file"
                  accept="image/*"
                  capture="environment"
                  onChange={handlePhotoCapture}
                  className="sr-only"
                />
              </label>
            )}

            {/* Resolution Work Notes */}
            <div className="space-y-1.5 pt-2">
              <label
                htmlFor="work-notes"
                className="text-xs font-mono text-secondary uppercase tracking-wider"
              >
                कार्य विवरण / Work Notes
              </label>
              <textarea
                id="work-notes"
                value={workNotes}
                onChange={(e) => setWorkNotes(e.target.value)}
                placeholder="उदा. गड्ढे को डामर से भरकर रोलर द्वारा समतल किया गया (Asphalt compacted)."
                rows={2}
                className="w-full bg-background border border-border rounded-sm p-3 text-sm text-primary font-ui focus:ring-2 focus:ring-focus outline-none"
              />
            </div>
          </div>
        </section>
      )}

      {/* Online Completed Confirmation Screen */}
      {isResolvedOnline && (
        <section className="p-6 bg-surface border-2 border-status-success/50 rounded-md text-center space-y-4 my-4">
          <div className="w-14 h-14 rounded-full bg-status-success/20 border border-status-success/40 flex items-center justify-center text-status-success mx-auto">
            <CheckCircle2 className="w-8 h-8" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-primary">कार्य आदेश पूर्ण / Work Order Resolved</h2>
            <p className="text-xs font-mono text-secondary mt-1">
              Proof submitted and verified with Municipal Command Deck
            </p>
          </div>
          <button
            onClick={() => navigate('/my-orders')}
            className="w-full min-h-[48px] bg-action-secondary text-primary font-bold text-sm rounded-sm hover:opacity-90 flex items-center justify-center"
          >
            मेरे कार्य आदेश सूची पर वापस जाएं (Back to Assigned Orders)
          </button>
        </section>
      )}

      {/* Bottom Fixed Action Bar: Single Large Primary Action (>=48px, Full-width) */}
      {!isResolvedOnline && (
        <footer
          role="region"
          aria-label="Field task primary action slot"
          className="fixed bottom-0 left-0 right-0 p-3 bg-surface/95 backdrop-blur-md border-t-2 border-border z-40 max-w-md mx-auto"
        >
          {order.status === 'assigned' && !isOfflineSaved ? (
            <button
              onClick={handleStartTask}
              disabled={isSubmitting}
              className="w-full min-h-[52px] bg-action-primary text-station-950 font-ui font-extrabold text-base rounded-md shadow-lifted flex items-center justify-center gap-2 active:scale-[0.98] transition-transform"
            >
              <span>{isSubmitting ? 'प्रारंभ हो रहा है...' : 'कार्य प्रारंभ करें (Start Task On-Site)'}</span>
            </button>
          ) : isOfflineSaved ? (
            /* Honest Offline State: Never false "Done" */
            <button
              disabled
              className="w-full min-h-[52px] bg-action-primary/30 text-action-primary border-2 border-action-primary/60 font-ui font-bold text-base rounded-md flex items-center justify-center gap-2 cursor-not-allowed"
            >
              <Clock className="w-5 h-5 text-action-primary" />
              <span>सहेजा गया — सिंक होगा (Saved — will sync)</span>
            </button>
          ) : (
            /* In-Progress Resolve Button: Strictly Disabled without Photo */
            <div className="space-y-1">
              <button
                onClick={handleResolveTask}
                disabled={!completionPhoto || isSubmitting}
                className={`w-full min-h-[52px] font-ui font-extrabold text-base rounded-md shadow-lifted flex items-center justify-center gap-2 transition-all ${
                  completionPhoto && !isSubmitting
                    ? 'bg-action-primary text-station-950 active:scale-[0.98]'
                    : 'bg-field-200 text-secondary border border-border cursor-not-allowed opacity-50'
                }`}
                aria-disabled={!completionPhoto}
              >
                {isSubmitting ? (
                  <span>सहेजा जा रहा है...</span>
                ) : isOnline ? (
                  <span>समाधान दर्ज करें / Resolve Work Order</span>
                ) : (
                  <span>ऑफ़लाइन सुरक्षित करें / Save Resolution Offline</span>
                )}
              </button>
              {!completionPhoto && (
                <p className="text-[11px] font-mono text-center text-status-warning font-semibold">
                  * समाधान दर्ज करने के लिए पूर्णता फोटो अनिवार्य है (Photo required)
                </p>
              )}
            </div>
          )}
        </footer>
      )}
    </div>
  );
};
