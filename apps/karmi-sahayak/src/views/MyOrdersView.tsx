import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useOfflineSync } from '../context/OfflineSyncContext';
import {
  getCachedWorkOrders,
  saveCachedWorkOrders,
  CachedWorkOrder,
} from '../services/offlineSync';
import {
  Clock,
  MapPin,
  ArrowRight,
  AlertTriangle,
  CheckCircle2,
  HardHat,
  WifiOff,
  RefreshCw,
} from 'lucide-react';

export const MyOrdersView: React.FC = () => {
  const { isOnline, isOrderQueued, queuedMutations } = useOfflineSync();

  // SCREEN_SPECS.md §2.15: MUST render from cache BEFORE any network call resolves!
  // Initialize state synchronously with local cache
  const [orders, setOrders] = useState<CachedWorkOrder[]>(() => getCachedWorkOrders());
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [networkError, setNetworkError] = useState<string | null>(null);

  // Background fetch to update cache when online
  useEffect(() => {
    async function refreshOrdersFromApi() {
      if (!isOnline) return;
      setIsRefreshing(true);
      setNetworkError(null);

      try {
        const res = await fetch('/v1/dispatch/work-orders/my');
        if (res.ok) {
          const apiOrders = await res.json();
          if (Array.isArray(apiOrders) && apiOrders.length > 0) {
            // Map API response to field worker display format
            const mapped: CachedWorkOrder[] = apiOrders.map((wo: any, idx: number) => ({
              id: wo.id.slice(0, 12).toUpperCase(),
              incident_id: wo.incident_id,
              category: wo.category_code
                ? `${wo.category_code.replace(/_/g, ' ')}`
                : 'नागरिक मरम्मत कार्य (Civic Remediation)',
              department: 'लोक निर्माण विभाग (PWD / Municipal Works)',
              wardNumber: 102 + (idx % 4),
              wardName: 'Rajajinagar Sector',
              address: 'Field Assignment Location, Ward Zone',
              slaRemainingHours: 3.5,
              status: wo.status,
              dispatched_at: wo.dispatched_at || wo.created_at,
              started_at: wo.started_at,
              citizenDescription: wo.resolution_notes || 'Assigned field remediation task.',
              lastCachedAt: new Date().toISOString(),
            }));

            setOrders(mapped);
            saveCachedWorkOrders(mapped);
          }
        }
      } catch (err: any) {
        // Non-blanking: keep showing last good cached data
        setNetworkError('सर्वर से नया डेटा नहीं मिला — ऑफ़लाइन कैश प्रदर्शित (Offline cache shown)');
      } finally {
        setIsRefreshing(false);
      }
    }

    refreshOrdersFromApi();
  }, [isOnline]);

  return (
    <div className="space-y-4 font-ui text-primary max-w-md mx-auto w-full pb-8">
      {/* Top Banner & Title Area */}
      <div className="pb-3 border-b border-border flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <HardHat className="w-5 h-5 text-action-primary flex-shrink-0" />
            <h1 className="font-ui text-xl font-bold text-primary tracking-tight">
              कर्मी सहायक — मेरे कार्य
            </h1>
          </div>
          <p className="font-mono text-xs text-text-secondary mt-0.5">
            Karmi Sahayak • Field Work Orders (Offline First)
          </p>
        </div>

        <div className="flex flex-col items-end">
          <span className="font-mono text-xs text-station-900 bg-action-primary px-2.5 py-1 rounded-sm font-bold shadow-sm">
            {orders.length} सक्रिय कार्य (Tasks)
          </span>
          {isRefreshing && (
            <span className="font-mono text-[10px] text-text-muted mt-1 flex items-center gap-1">
              <RefreshCw className="w-2.5 h-2.5 animate-spin" /> अपडेट हो रहा है...
            </span>
          )}
        </div>
      </div>

      {/* Offline Status or Queued Notice Bar */}
      {!isOnline && (
        <div className="p-3 rounded-md bg-status-warning/15 border-2 border-status-warning text-station-900 flex items-center justify-between text-xs font-mono font-medium">
          <div className="flex items-center gap-2">
            <WifiOff className="w-4 h-4 text-status-warning flex-shrink-0" />
            <span>ऑफ़लाइन मोड (Offline Mode) • कैश्ड डेटा</span>
          </div>
          {queuedMutations.length > 0 && (
            <span className="px-2 py-0.5 bg-status-warning text-station-950 font-bold rounded-sm text-[11px]">
              {queuedMutations.length} लंबित (Queued)
            </span>
          )}
        </div>
      )}

      {/* Empty State */}
      {orders.length === 0 ? (
        <div className="p-8 text-center bg-surface rounded-md border border-border space-y-3">
          <div className="w-12 h-12 mx-auto rounded-full bg-surface-raised flex items-center justify-center text-text-muted">
            <CheckCircle2 className="w-6 h-6 text-status-success" />
          </div>
          <h2 className="text-base font-bold text-primary">
            कोई कार्य आदेश नहीं (No work orders assigned)
          </h2>
          <p className="text-xs text-text-secondary">
            आपके वार्ड के लिए सभी कार्य पूर्ण हो चुके हैं। नए कार्य आदेश आने पर स्वचालित रूप से यहां दिखाई देंगे।
          </p>
        </div>
      ) : (
        /* Work Orders List (SCREEN_SPECS.md §2.15: Hi-vis card format, large everything) */
        <div className="space-y-3">
          {orders.map((order) => {
            const isQueued = isOrderQueued(order.id);
            const isUrgent = order.slaRemainingHours < 3;

            return (
              <Link
                key={order.id}
                to={`/orders/${order.id}`}
                className={`
                  block p-5 bg-surface rounded-md border-2 transition-all min-h-[56px] active:scale-[0.99]
                  ${
                    isUrgent
                      ? 'border-action-primary/80 bg-surface hover:border-action-primary shadow-sm'
                      : 'border-border hover:border-border-strong'
                  }
                `}
                aria-label={`Open work order ${order.id}: ${order.category}`}
              >
                {/* Header Strip with Order Code and SLA */}
                <div className="flex items-start justify-between gap-2 pb-2 border-b border-border/80">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-action-primary font-bold">
                      {order.id}
                    </span>
                    <span className="text-text-muted">•</span>
                    <span className="font-mono text-[11px] text-text-secondary truncate max-w-[140px]">
                      {order.department}
                    </span>
                  </div>

                  {/* SLA Countdown Badge (Color-coded) */}
                  <div
                    className={`
                      inline-flex items-center gap-1 font-mono text-xs font-bold px-2 py-0.5 rounded-sm border
                      ${
                        isUrgent
                          ? 'bg-status-warning/20 text-station-900 border-status-warning'
                          : 'bg-surface-raised text-primary border-border'
                      }
                    `}
                  >
                    <Clock className="w-3 h-3 flex-shrink-0" />
                    <span>{order.slaRemainingHours.toFixed(1)}h शेष</span>
                  </div>
                </div>

                {/* Large Category Title */}
                <div className="mt-2.5">
                  <h2 className="text-lg font-bold text-primary tracking-tight leading-snug">
                    {order.category}
                  </h2>
                </div>

                {/* Location and Ward Strip (Large & Outdoor Legible) */}
                <div className="mt-2 flex items-start gap-1.5 text-xs text-text-secondary">
                  <MapPin className="w-4 h-4 text-action-primary flex-shrink-0 mt-0.5" />
                  <span className="leading-tight">
                    {order.address} · <strong className="text-primary font-medium">वार्ड {order.wardNumber} ({order.wardName})</strong>
                  </span>
                </div>

                {/* Footer with Status Tag and Action Prompt */}
                <div className="mt-4 pt-3 border-t border-border flex items-center justify-between">
                  {isQueued ? (
                    <span className="inline-flex items-center gap-1 font-mono text-[11px] font-bold px-2.5 py-1 bg-action-primary/20 text-station-900 border border-action-primary rounded-sm">
                      <Clock className="w-3 h-3 text-action-primary" />
                      लंबित सिंक (Queued Locally)
                    </span>
                  ) : order.status === 'in_progress' ? (
                    <span className="inline-flex items-center gap-1 font-mono text-[11px] font-bold px-2.5 py-1 bg-action-primary text-station-900 rounded-sm">
                      <span className="w-2 h-2 rounded-full bg-station-950 animate-pulse" />
                      प्रगति पर (In Progress)
                    </span>
                  ) : (
                    <span className="font-mono text-[11px] font-medium px-2 py-0.5 bg-surface-raised text-text-secondary border border-border rounded-sm">
                      आवंटित (Dispatched)
                    </span>
                  )}

                  <div className="flex items-center gap-1 text-xs font-semibold text-action-primary">
                    <span>कार्य शुरू करें</span>
                    <ArrowRight className="w-4 h-4" />
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
};
