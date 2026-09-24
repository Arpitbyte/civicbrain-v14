import React, { useState } from 'react';
import {
  Button,
  IconButton,
  Field,
  Input,
  Textarea,
  Select,
  Checkbox,
  RadioGroup,
  Switch,
  Tabs,
  TabsContent,
  Tooltip,
  ToastProvider,
  useToast,
  Dialog,
  Sheet,
  Drawer,
  Badge,
  Chip,
  Skeleton,
  EmptyState,
  ErrorState,
} from './index';
import {
  Search,
  Plus,
  Trash2,
  Settings,
  AlertCircle,
  CheckCircle2,
  HelpCircle,
  Inbox,
  Filter,
} from 'lucide-react';

const WORKSPACES = [
  { id: 'nagrik-setu', name: 'Nagrik Setu (Citizen)' },
  { id: 'command-deck', name: 'Command Deck (Triage)' },
  { id: 'ops-board', name: 'Ops Board (Dept)' },
  { id: 'city-pulse', name: 'City Pulse (Supervisor)' },
  { id: 'karmi-sahayak', name: 'Karmi Sahayak (Field)' },
  { id: 'control-room', name: 'Control Room (Admin)' },
  { id: 'transparency-board', name: 'Transparency Board (Public)' },
] as const;

export const PrimitivesShowcaseInner: React.FC = () => {
  const { toast } = useToast();
  const [currentWorkspace, setCurrentWorkspace] = useState<string>('command-deck');

  // Interactive states
  const [inputValue, setInputValue] = useState('WARD-14-DRAINAGE');
  const [textareaValue, setTextareaValue] = useState('Reported severe blockage near municipal gate 4.');
  const [selectValue, setSelectValue] = useState('high');
  const [checkboxChecked, setCheckboxChecked] = useState(true);
  const [radioValue, setRadioValue] = useState('dept-roads');
  const [switchChecked, setSwitchChecked] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [sheetOpen, setSheetOpen] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);

  return (
    <div
      data-workspace={currentWorkspace}
      className="min-h-screen bg-background text-primary p-6 md:p-10 font-ui transition-colors duration-fast"
    >
      {/* Top Workspace Theme Switcher Bar */}
      <header className="mb-10 pb-6 border-b border-border flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-primary">
              CivicBrain Primitives Showcase
            </h1>
            <Badge variant="neutral" size="sm">Tier 0 Benchmark</Badge>
          </div>
          <p className="text-sm text-text-secondary mt-1 max-w-2xl">
            Isolated demo showing all Tier 0 primitives in default, hover, focus, disabled, and invalid states.
            Swapping the workspace dynamically tests token re-skinning without component changes.
          </p>
        </div>

        <div className="flex items-center gap-3 bg-surface p-2 rounded-md border border-border">
          <label htmlFor="workspace-select" className="text-xs font-semibold text-text-secondary whitespace-nowrap">
            Theme Context:
          </label>
          <select
            id="workspace-select"
            value={currentWorkspace}
            onChange={(e) => setCurrentWorkspace(e.target.value)}
            className="text-xs bg-surface-raised border border-border rounded-sm py-1.5 px-2.5 font-medium text-primary outline-none focus:ring-2 focus:ring-focus"
          >
            {WORKSPACES.map((w) => (
              <option key={w.id} value={w.id}>
                {w.name}
              </option>
            ))}
          </select>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        {/* 1. BUTTONS & ICON BUTTONS */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">Buttons & IconButtons</h2>
            <span className="text-xs font-mono text-text-secondary">DESIGN.md §8 (radius-md)</span>
          </div>

          <div className="space-y-4">
            <div className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Variants</div>
            <div className="flex flex-wrap items-center gap-3">
              <Button variant="primary">Primary Action</Button>
              <Button variant="secondary">Secondary Action</Button>
              <Button variant="destructive">Destructive</Button>
              <Button variant="ghost">Ghost Button</Button>
            </div>

            <div className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Sizes</div>
            <div className="flex flex-wrap items-center gap-3">
              <Button size="sm">Small (32px)</Button>
              <Button size="md">Medium (40px)</Button>
              <Button size="lg">Large (48px)</Button>
            </div>

            <div className="text-xs font-semibold text-text-secondary uppercase tracking-wider">States & Icons</div>
            <div className="flex flex-wrap items-center gap-3">
              <Button leftIcon={<Plus className="w-4 h-4" />}>With Left Icon</Button>
              <Button rightIcon={<Settings className="w-4 h-4" />} variant="secondary">
                With Right Icon
              </Button>
              <Button isLoading>Processing</Button>
              <Button disabled>Disabled Action</Button>
            </div>

            <div className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Icon Buttons</div>
            <div className="flex items-center gap-3">
              <IconButton aria-label="Search records" icon={<Search className="w-4 h-4" />} variant="primary" />
              <IconButton aria-label="Settings configuration" icon={<Settings className="w-4 h-4" />} variant="secondary" />
              <IconButton aria-label="Delete observation" icon={<Trash2 className="w-4 h-4" />} variant="destructive" />
              <IconButton aria-label="Disabled settings" icon={<Settings className="w-4 h-4" />} disabled />
            </div>
          </div>
        </section>

        {/* 2. FORM FIELDS & INPUTS */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">Form Fields & Inputs</h2>
            <span className="text-xs font-mono text-text-secondary">radius-sm, 1px border</span>
          </div>

          <div className="space-y-4">
            <Field id="default-input" label="Tracking Token / Case ID" helperText="Alphanumeric identifier assigned upon ingestion.">
              <Input
                id="default-input"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="e.g. WARD-14-1092"
                leftIcon={<Search className="w-4 h-4" />}
              />
            </Field>

            <Field
              id="invalid-input"
              label="Citizen Mobile Number"
              required
              errorMessage="Enter a valid 10-digit Indian mobile number for OTP verification."
            >
              <Input
                id="invalid-input"
                defaultValue="98765"
                isInvalid
                placeholder="10-digit number"
              />
            </Field>

            <Field id="disabled-input" label="GIS Ward Code (Read-Only)" disabled helperText="Automatically detected from polygon boundaries.">
              <Input id="disabled-input" value="ZONE-SOUTH-WARD-114" disabled />
            </Field>

            <Field id="notes-textarea" label="Dispatcher Triage Notes">
              <Textarea
                id="notes-textarea"
                value={textareaValue}
                onChange={(e) => setTextareaValue(e.target.value)}
                rows={3}
                placeholder="Add contextual field observations..."
              />
            </Field>
          </div>
        </section>

        {/* 3. SELECTION CONTROLS */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">Select, Checkbox, Radio & Switch</h2>
            <span className="text-xs font-mono text-text-secondary">Radix Unstyled</span>
          </div>

          <div className="space-y-5">
            <Field label="Severity Assessment Level">
              <Select
                value={selectValue}
                onValueChange={setSelectValue}
                options={[
                  { value: 'low', label: 'Priority 1 - Standard SLA (72h)' },
                  { value: 'medium', label: 'Priority 2 - Elevated SLA (48h)' },
                  { value: 'high', label: 'Priority 3 - Urgent SLA (24h)' },
                  { value: 'critical', label: 'Priority 4 - Emergency / Hazard (6h)' },
                ]}
              />
            </Field>

            <div className="pt-2 border-t border-border flex flex-col gap-3">
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Checkboxes</span>
              <Checkbox
                label="Require Supervisor Sign-off"
                description="Flags the incident for zonal engineer review before closure."
                checked={checkboxChecked}
                onCheckedChange={(c) => setCheckboxChecked(Boolean(c))}
              />
              <Checkbox
                label="Disabled State Option"
                description="Cannot be toggled in offline draft mode."
                disabled
                checked={false}
              />
            </div>

            <div className="pt-2 border-t border-border flex flex-col gap-3">
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Radio Group</span>
              <RadioGroup
                value={radioValue}
                onValueChange={setRadioValue}
                options={[
                  { value: 'dept-roads', label: 'Roads & Infrastructure', description: 'Potholes, pavers, dividers' },
                  { value: 'dept-drainage', label: 'Stormwater & Drainage', description: 'Clogged culverts, desilting' },
                  { value: 'dept-sanitation', label: 'Solid Waste Management', description: 'Garbage dumps, missed bin clearance', disabled: true },
                ]}
              />
            </div>

            <div className="pt-2 border-t border-border flex flex-col gap-3">
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Switch</span>
              <Switch
                label="Auto-assign nearest field crew"
                description="Uses geospatial routing to alert active personnel."
                checked={switchChecked}
                onCheckedChange={setSwitchChecked}
              />
              <Switch
                label="Enforce strict biometric check-in"
                description="Unavailable for non-field roles."
                disabled
              />
            </div>
          </div>
        </section>

        {/* 4. TABS, TOOLTIPS, TOASTS & BADGES */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">Tabs, Tooltips, Toasts & Badges</h2>
            <span className="text-xs font-mono text-text-secondary">Underline Tabs / Pill Chips</span>
          </div>

          <div className="space-y-6">
            <div>
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider block mb-2">
                Underline Tabs (DESIGN.md §8)
              </span>
              <Tabs
                items={[
                  { value: 'active', label: 'Active Queue', badge: <Badge size="sm">24</Badge> },
                  { value: 'dispatched', label: 'Dispatched', badge: <Badge size="sm" variant="info">12</Badge> },
                  { value: 'resolved', label: 'Verified Resolved' },
                ]}
              >
                <TabsContent value="active" className="p-4 bg-surface-raised rounded-md border border-border text-xs mt-3">
                  Viewing Active Incidents requiring triage or dispatch allocation.
                </TabsContent>
                <TabsContent value="dispatched" className="p-4 bg-surface-raised rounded-md border border-border text-xs mt-3">
                  Work orders actively claimed by field crew with offline-sync badges.
                </TabsContent>
                <TabsContent value="resolved" className="p-4 bg-surface-raised rounded-md border border-border text-xs mt-3">
                  Cases with before/after evidence pairs awaiting citizen confirmation.
                </TabsContent>
              </Tabs>
            </div>

            <div>
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider block mb-2">
                Badges & Chips (The Only Pill / rounded-full)
              </span>
              <div className="flex flex-wrap items-center gap-2">
                <Badge variant="default">Default</Badge>
                <Badge variant="neutral">Ward 14</Badge>
                <Badge variant="success" icon={<CheckCircle2 className="w-3 h-3" />}>Verified</Badge>
                <Badge variant="warning" icon={<AlertCircle className="w-3 h-3" />}>Under Review</Badge>
                <Badge variant="danger">Disputed</Badge>
                <Badge variant="info">In Flight</Badge>
                <Chip variant="priority-1">P1 Low</Chip>
                <Chip variant="priority-2">P2 Med</Chip>
                <Chip variant="priority-3">P3 High</Chip>
                <Chip variant="priority-4">P4 Crit</Chip>
                <Chip variant="neutral" interactive onRemove={() => toast({ description: 'Filter chip dismissed.' })}>
                  Dismissible Chip
                </Chip>
              </div>
            </div>

            <div>
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider block mb-2">
                Tooltips & Toasts
              </span>
              <div className="flex flex-wrap items-center gap-3">
                <Tooltip content="AHP Consistency Ratio must be < 0.10 for stable prioritization.">
                  <Button variant="secondary" size="sm" leftIcon={<HelpCircle className="w-3.5 h-3.5" />}>
                    Hover or Focus for Tooltip
                  </Button>
                </Tooltip>

                <Button
                  size="sm"
                  variant="primary"
                  onClick={() =>
                    toast({
                      title: 'Evidence Uploaded',
                      description: 'GPS metadata and EXIF timestamp verified by server.',
                      variant: 'success',
                    })
                  }
                >
                  Trigger Toast
                </Button>

                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() =>
                    toast({
                      title: 'Sync Collision Detected',
                      description: 'Observation was modified concurrently by another dispatcher.',
                      variant: 'danger',
                      action: {
                        label: 'View Conflict',
                        onClick: () => alert('Navigating to Conflict Adjudication...'),
                      },
                    })
                  }
                >
                  Actionable Toast
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* 5. OVERLAYS: DIALOG, SHEET, DRAWER */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">Overlays: Dialog, Sheet & Drawer</h2>
            <span className="text-xs font-mono text-text-secondary">Caller-Decided Presentation</span>
          </div>

          <div className="space-y-4">
            <p className="text-xs text-text-secondary leading-relaxed">
              Per DESIGN.md §8: Dialog is center-modal with radius-lg for genuinely blocking decisions.
              Sheet is bottom-anchored with radius-xl top corners for mobile interfaces (Nagrik Setu / Karmi Sahayak).
              Drawer is right-anchored for list detail inspection without losing scroll context (Command Deck).
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-2">
              <Button onClick={() => setDialogOpen(true)}>Open Center Dialog</Button>
              <Button variant="secondary" onClick={() => setSheetOpen(true)}>Open Bottom Sheet</Button>
              <Button variant="secondary" onClick={() => setDrawerOpen(true)}>Open Right Drawer</Button>
            </div>

            {/* Dialog Instance */}
            <Dialog
              open={dialogOpen}
              onOpenChange={setDialogOpen}
              title="Adjudicate Sync Collision"
              description="Review competing mutations for Observation #OBS-9921."
              footer={
                <>
                  <Button variant="ghost" onClick={() => setDialogOpen(false)}>
                    Cancel
                  </Button>
                  <Button variant="destructive" onClick={() => setDialogOpen(false)}>
                    Confirm Overwrite
                  </Button>
                </>
              }
            >
              <div className="text-xs text-text-secondary leading-relaxed space-y-2">
                <p>
                  Field worker and dispatcher submitted conflicting status updates while the terminal was offline.
                  Confirming will record this resolution in the immutable Transparency Board audit ledger.
                </p>
              </div>
            </Dialog>

            {/* Sheet Instance */}
            <Sheet
              open={sheetOpen}
              onOpenChange={setSheetOpen}
              title="Filter Incidents by Zone"
              description="Nagrik Setu mobile-first bottom sheet drawer."
              footer={
                <Button className="w-full" onClick={() => setSheetOpen(false)}>
                  Apply 3 Filters
                </Button>
              }
            >
              <div className="space-y-3 py-2">
                <Checkbox label="South Zone (Wards 110–135)" defaultChecked />
                <Checkbox label="East Zone (Wards 70–95)" defaultChecked />
                <Checkbox label="Central Commercial District" />
              </div>
            </Sheet>

            {/* Drawer Instance */}
            <Drawer
              open={drawerOpen}
              onOpenChange={setDrawerOpen}
              title="Incident #INC-2026-0819"
              description="Quick view from Command Deck dispatch triage queue."
              footer={
                <Button variant="primary" onClick={() => setDrawerOpen(false)}>
                  Assign Work Order
                </Button>
              }
            >
              <div className="space-y-4 text-xs font-ui">
                <div className="p-3 bg-surface-raised rounded-md border border-border">
                  <div className="font-semibold text-primary mb-1">Ward 14 · Main Stormwater Drain</div>
                  <div className="text-text-secondary">Severity: Priority 3 (Urgent) · Z-Score: 0.88</div>
                </div>
                <p className="text-text-secondary">
                  Multiple citizen reports confirmed blocked culvert causing roadway waterlogging. Field team alerted.
                </p>
              </div>
            </Drawer>
          </div>
        </section>

        {/* 6. SKELETON, EMPTY STATE & ERROR STATE */}
        <section className="bg-surface p-6 rounded-md border border-border flex flex-col gap-6">
          <div className="border-b border-border pb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-primary">Skeleton, Empty & Error States</h2>
            <span className="text-xs font-mono text-text-secondary">Required Specific Messages</span>
          </div>

          <div className="space-y-5">
            <div>
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider block mb-2">
                Honest Skeleton Pulse (DESIGN.md §10)
              </span>
              <div className="p-4 bg-surface-raised rounded-md border border-border flex items-center gap-3">
                <Skeleton variant="circle" width={40} height={40} />
                <div className="flex-1 space-y-2">
                  <Skeleton variant="text" width="60%" />
                  <Skeleton variant="text" width="90%" />
                </div>
              </div>
            </div>

            <div>
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider block mb-2">
                EmptyState (Mandatory specific message prop)
              </span>
              <EmptyState
                title="No active work orders in Ward 14"
                message="All dispatched tasks for this ward have been completed or scheduled for next shift."
                action={{
                  label: 'Switch Ward Filter',
                  onClick: () => toast({ description: 'Filter opened.' }),
                }}
              />
            </div>

            <div>
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider block mb-2">
                ErrorState (Mandatory plain-language message + nextStep)
              </span>
              <ErrorState
                title="Failed to fetch ward boundaries"
                message="The geospatial service did not respond within the 5000ms threshold."
                nextStep="Check your network connection and retry. If offline, cached boundaries remain active."
                onRetry={() => toast({ description: 'Retrying geospatial fetch...' })}
              />
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export const PrimitivesShowcase: React.FC = () => {
  return (
    <ToastProvider>
      <PrimitivesShowcaseInner />
    </ToastProvider>
  );
};
