import React from 'react';
import { Link } from 'react-router-dom';
import { useOfflineSync } from '../context/OfflineSyncContext';
import { Clock, MapPin, ArrowRight, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface OrderItem {
  id: string;
  category: string;
  department: string;
  wardNumber: number;
  wardName: string;
  address: string;
  slaRemainingHours: number;
  status: 'assigned' | 'in_progress' | 'resolved';
}

const MOCK_ASSIGNED_ORDERS: OrderItem[] = [
  {
    id: 'WO-2026-8492',
    category: 'सड़क एवं गड्ढे (Roads & Pothole Repair)',
    department: 'लोक निर्माण विभाग (PWD)',
    wardNumber: 102,
    wardName: 'Rajajinagar',
    address: '14th Main Rd, Near Post Office Junction',
    slaRemainingHours: 2.25,
    status: 'assigned',
  },
  {
    id: 'WO-2026-8104',
    category: 'विद्युत एवं स्ट्रीटलाइट (Streetlighting / Broken Fixture)',
    department: 'विद्युत एवं प्रकाश विभाग (Electrical)',
    wardNumber: 101,
    wardName: 'Malleshwaram',
    address: '8th Cross, Temple Road',
    slaRemainingHours: 5.5,
    status: 'in_progress',
  },
  {
    id: 'WO-2026-7933',
    category: 'सीवरेज एवं जल निकासी (Drainage / Open Manhole)',
    department: 'जल आपूर्ति एवं सीवरेज (Water & Sewerage)',
    wardNumber: 103,
    wardName: 'Gandhinagar',
    address: '5th Cross, Market Area',
    slaRemainingHours: 1.1,
    status: 'assigned',
  },
];

export const MyOrdersView: React.FC = () => {
  const { isOrderQueued } = useOfflineSync();

  return (
    <div className="space-y-4 font-ui text-primary max-w-md mx-auto w-full">
      <div className="pb-3 border-b border-border flex items-center justify-between">
        <div>
          <h1 className="font-ui text-xl font-bold text-primary">
            कर्मी सहायक — मेरे कार्य आदेश
          </h1>
          <p className="font-mono text-xs text-secondary mt-0.5">
            Karmi Sahayak • Assigned Field Tasks (Offline-Cached)
          </p>
        </div>
        <div className="font-mono text-xs text-action-primary bg-action-primary/10 px-2 py-0.5 border border-action-primary/30 rounded-sm font-bold">
          {MOCK_ASSIGNED_ORDERS.length} कार्य (Tasks)
        </div>
      </div>

      {/* Work Orders List */}
      <div className="space-y-3">
        {MOCK_ASSIGNED_ORDERS.map((order) => {
          const isQueued = isOrderQueued(order.id);
          const isUrgent = order.slaRemainingHours < 3;

          return (
            <Link
              key={order.id}
              to={`/orders/${order.id}`}
              className={`block p-4 bg-surface rounded-md border-2 transition-all min-h-[52px] active:scale-[0.99] ${
                isUrgent ? 'border-action-primary/60 hover:border-action-primary' : 'border-border hover:border-border-strong'
              }`}
              aria-label={`Open work order ${order.id}: ${order.category}`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <span className="font-mono text-[11px] text-action-primary font-bold">
                    {order.id} • {order.department}
                  </span>
                  <h2 className="text-base font-bold text-primary tracking-tight mt-0.5">
                    {order.category}
                  </h2>
                </div>
                {isQueued ? (
                  <span className="font-mono text-[11px] px-2 py-0.5 bg-action-primary/20 text-action-primary border border-action-primary/40 rounded-sm">
                    ऑफ़लाइन सुरक्षित (Queued)
                  </span>
                ) : (
                  <span
                    className={`font-mono text-[11px] px-2 py-0.5 rounded-sm border ${
                      order.status === 'in_progress'
                        ? 'bg-status-warning/20 text-status-warning border-status-warning/40'
                        : 'bg-field-100 text-secondary border-border'
                    }`}
                  >
                    {order.status === 'in_progress' ? 'प्रगति पर (In Progress)' : 'आवंटित (Assigned)'}
                  </span>
                )}
              </div>

              <div className="flex items-center gap-1.5 font-mono text-xs text-secondary mt-2">
                <MapPin className="w-3.5 h-3.5 text-action-primary shrink-0" />
                <span className="truncate">
                  वार्ड {order.wardNumber} ({order.wardName}) • {order.address}
                </span>
              </div>

              <div className="flex items-center justify-between mt-3 pt-2.5 border-t border-border text-xs font-mono">
                <div className="flex items-center gap-1 text-action-primary font-bold">
                  <Clock className="w-3.5 h-3.5" />
                  <span>
                    एसएलए (SLA): {Math.floor(order.slaRemainingHours)}h{' '}
                    {Math.round((order.slaRemainingHours % 1) * 60)}m शेष
                  </span>
                </div>
                <div className="flex items-center gap-1 text-secondary group-hover:text-primary">
                  <span>विवरण खोलें (Open)</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
};
