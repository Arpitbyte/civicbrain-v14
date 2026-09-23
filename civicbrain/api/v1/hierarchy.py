"""Administrative hierarchy, department taxonomy, and representative discovery endpoints."""

import csv
import hashlib
import io
import logging
import re
import secrets
import uuid
from datetime import date, timedelta

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from civicbrain.domain.identity.jwt import CurrentUserClaims, require_roles
from civicbrain.domain.identity.models import (
    Department,
    ElectedRepresentative,
    StaffBulkImportLog,
    StaffRole,
    UserAccount,
    UserRoleAssignment,
    Ward,
    Zone,
)
from civicbrain.domain.identity.services import (
    create_staff_user,
    get_departments,
    get_organization_hierarchy,
    get_ward_representative,
)
from civicbrain.domain.notifications.service import dispatch_account_setup_invitation
from civicbrain.infra.database import get_db
from civicbrain.infra.rate_limit import RateLimiter
from civicbrain.infra.security import sanitize_csv_cell
from civicbrain.infra.supabase import get_supabase_admin_client
from civicbrain.schemas.identity import (
    BulkImportResponse,
    BulkImportRowResult,
    DepartmentCreate,
    DepartmentResponse,
    ElectedRepresentativeResponse,
    HierarchyTreeResponse,
    UserAccountCreate,
    UserAccountResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Hierarchy & Administration"])

# Maximum upload constraints
MAX_IMPORT_FILE_BYTES = 2 * 1024 * 1024  # 2 MB
MAX_IMPORT_ROWS = 500

# Canonical staff roles permitted in bulk import (Admin strictly prohibited)
ALLOWED_BULK_ROLES = {
    StaffRole.DISPATCHER.value,
    StaffRole.DEPARTMENT_STAFF.value,
    StaffRole.ZONAL_SUPERVISOR.value,
    StaffRole.FIELD_WORKER.value,
    StaffRole.CORPORATOR.value,
}

PHONE_REGEX = re.compile(r"^(\+91[\s-]?)?[6-9]\d{9}$")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_indian_phone(raw_phone: str) -> str | None:
    """Validate and normalize Indian phone number to E.164 +91XXXXXXXXXX format."""
    cleaned = re.sub(r"[\s-]", "", raw_phone.strip())
    if not PHONE_REGEX.match(cleaned):
        return None
    digits = re.sub(r"\D", "", cleaned)
    if len(digits) == 10:
        return f"+91{digits}"
    if len(digits) == 12 and digits.startswith("91"):
        return f"+{digits}"
    return None


@router.get(
    "/orgs/{org_id}/hierarchy",
    response_model=HierarchyTreeResponse,
    summary="Get zonal and ward hierarchy tree",
)
async def get_hierarchy(
    org_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> HierarchyTreeResponse:
    """Retrieve complete tree of zones and wards for an organization."""
    tree = await get_organization_hierarchy(db, org_id)
    if not tree:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    return tree


@router.get(
    "/orgs/{org_id}/departments",
    response_model=list[DepartmentResponse],
    summary="List active ULB departments",
)
async def list_departments(
    org_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[DepartmentResponse]:
    """List all active departments within the ULB."""
    depts = await get_departments(db, org_id)
    return [DepartmentResponse.model_validate(d) for d in depts]


@router.post(
    "/orgs/{org_id}/departments",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create active ULB department (Admin only)",
)
async def create_department(
    org_id: uuid.UUID,
    payload: DepartmentCreate,
    claims: CurrentUserClaims = Depends(require_roles([StaffRole.ADMIN])),
    db: AsyncSession = Depends(get_db),
) -> DepartmentResponse:
    """Create a new department within the admin's tenant organization."""
    if not claims.org_id or claims.org_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin can only manage departments in their own organization",
        )

    clean_code = payload.code.strip().upper()
    existing_res = await db.execute(
        select(Department).where(
            Department.organization_id == org_id,
            Department.code == clean_code,
        )
    )
    if existing_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Department with code '{clean_code}' already exists in this organization",
        )

    dept = Department(
        organization_id=org_id,
        name=payload.name.strip(),
        code=clean_code,
        is_active=payload.is_active,
    )
    db.add(dept)
    await db.commit()
    await db.refresh(dept)
    return DepartmentResponse.model_validate(dept)


@router.get(
    "/orgs/{org_id}/wards/{ward_id}/representative",
    response_model=ElectedRepresentativeResponse,
    summary="Get elected Corporator/Councillor for a ward",
)
async def get_representative(
    org_id: uuid.UUID,
    ward_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ElectedRepresentativeResponse:
    """Public endpoint to discover the elected representative for a specific ward."""
    rep = await get_ward_representative(db, ward_id)
    if not rep or rep.organization_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elected representative not found for this ward",
        )
    return ElectedRepresentativeResponse.model_validate(rep)


@router.post(
    "/admin/users",
    response_model=UserAccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register staff user and assign role (Admin only)",
)
async def create_staff_member(
    user_in: UserAccountCreate,
    claims: CurrentUserClaims = Depends(require_roles([StaffRole.ADMIN])),
    db: AsyncSession = Depends(get_db),
) -> UserAccountResponse:
    """Register staff account and assign role with jurisdictional scope within admin's tenant."""
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin must belong to an organization to provision staff",
        )

    auth_user_id = uuid.uuid4()
    staff = await create_staff_user(db, claims.org_id, user_in, auth_user_id)
    return UserAccountResponse.model_validate(staff)


@router.get(
    "/admin/users",
    response_model=list[UserAccountResponse],
    summary="List staff users in organization (Admin only)",
)
async def list_staff_members(
    claims: CurrentUserClaims = Depends(require_roles([StaffRole.ADMIN])),
    db: AsyncSession = Depends(get_db),
) -> list[UserAccountResponse]:
    """List staff accounts within the admin's tenant organization."""
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin must belong to an organization to list staff",
        )

    res = await db.execute(
        select(UserAccount)
        .where(UserAccount.organization_id == claims.org_id)
        .options(selectinload(UserAccount.roles))
    )
    users = res.scalars().all()
    return [UserAccountResponse.model_validate(u) for u in users]


@router.post(
    "/admin/users/import",
    response_model=BulkImportResponse,
    summary="Bulk import staff users via CSV with dry-run default (Admin only)",
)
async def bulk_import_users(
    file: UploadFile = File(...),
    dry_run: bool = Query(default=True, description="Validate CSV without creating accounts"),
    claims: CurrentUserClaims = Depends(require_roles([StaffRole.ADMIN])),
    _rate_limit: None = Depends(
        RateLimiter(max_requests=5, window_seconds=60, prefix="admin_import")
    ),
    db: AsyncSession = Depends(get_db),
) -> BulkImportResponse:
    """Bulk import staff users for non-admin operational roles from a CSV file.

    Features:
    - Default dry_run=true for safe pre-flight validation.
    - Idempotency protection via SHA-256 file content hash.
    - Passwordless onboarding: dispatches setup tokens for user-defined passwords.
    - Formula injection defense: sanitizes =, +, -, @ prefixes.
    - Explicit duplicate phone rejection (never overwrites).
    - Permanent audit logging in staff_bulk_import_log.
    """
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin must belong to an organization to import staff",
        )

    # 1. Enforce file size limit (2 MB)
    content = await file.read(MAX_IMPORT_FILE_BYTES + 1)
    if len(content) > MAX_IMPORT_FILE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="File size exceeds maximum allowed limit of 2MB",
        )

    # 2. Compute SHA-256 file hash for idempotency
    file_hash = hashlib.sha256(content).hexdigest()

    # 3. Check idempotency on real commits
    if not dry_run:
        existing_log_res = await db.execute(
            select(StaffBulkImportLog).where(
                StaffBulkImportLog.organization_id == claims.org_id,
                StaffBulkImportLog.file_hash == file_hash,
                StaffBulkImportLog.is_dry_run.is_(False),
            )
        )
        dup_log = existing_log_res.scalar_one_or_none()
        if dup_log:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"File with SHA-256 hash '{file_hash}' has already been processed for this organization on {dup_log.created_at.isoformat()}.",
            )

    # 4. Parse CSV text
    text_content = content.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text_content))

    fieldnames = [f.strip() for f in (reader.fieldnames or [])]
    required_headers = {"full_name", "phone", "role"}
    missing_headers = required_headers - set(fieldnames)
    if missing_headers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CSV missing required columns: {sorted(missing_headers)}. Found: {fieldnames}",
        )

    rows = list(reader)
    total_rows = len(rows)
    if total_rows == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV file contains no data rows.",
        )
    if total_rows > MAX_IMPORT_ROWS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CSV row count ({total_rows}) exceeds maximum allowed limit of {MAX_IMPORT_ROWS} rows.",
        )

    # 5. Pre-load organization metadata for scope and uniqueness validation
    dept_res = await db.execute(
        select(Department).where(
            Department.organization_id == claims.org_id,
            Department.is_active.is_(True),
        )
    )
    dept_map = {d.code.upper(): d.id for d in dept_res.scalars().all()}

    zone_res = await db.execute(select(Zone).where(Zone.organization_id == claims.org_id))
    zone_map = {z.code.upper(): z.id for z in zone_res.scalars().all()}

    ward_res = await db.execute(select(Ward).where(Ward.organization_id == claims.org_id))
    ward_map = {w.ward_number: w.id for w in ward_res.scalars().all()}

    existing_phones_res = await db.execute(select(UserAccount.phone))
    existing_phones = {p for p in existing_phones_res.scalars().all() if p}

    rep_res = await db.execute(
        select(ElectedRepresentative.ward_id).where(
            ElectedRepresentative.organization_id == claims.org_id
        )
    )
    existing_corporator_wards = set(rep_res.scalars().all())

    # 6. Validate and process each row
    seen_batch_phones: set[str] = set()
    results: list[BulkImportRowResult] = []
    created_count = 0
    skipped_count = 0

    for idx, raw_row in enumerate(rows):
        row_number = idx + 2  # Account for 1-indexed header

        # Sanitize against CSV formula injection
        full_name = sanitize_csv_cell(raw_row.get("full_name", ""))
        phone_raw = sanitize_csv_cell(raw_row.get("phone", ""))
        email_raw = sanitize_csv_cell(raw_row.get("email", ""))
        role_raw = sanitize_csv_cell(raw_row.get("role", "")).lower().strip()
        dept_code = sanitize_csv_cell(raw_row.get("department_code", "")).upper().strip()
        zone_code = sanitize_csv_cell(raw_row.get("zone_code", "")).upper().strip()
        ward_num_raw = sanitize_csv_cell(raw_row.get("ward_number", "")).strip()

        # Check required full_name
        if not full_name:
            skipped_count += 1
            results.append(
                BulkImportRowResult(
                    row_number=row_number,
                    full_name="",
                    phone=phone_raw,
                    email=email_raw or None,
                    role=role_raw,
                    status="skipped",
                    reason="Full name is required.",
                )
            )
            continue

        # Check non-admin role restriction (Hard Invariant)
        if role_raw == StaffRole.ADMIN.value:
            skipped_count += 1
            results.append(
                BulkImportRowResult(
                    row_number=row_number,
                    full_name=full_name,
                    phone=phone_raw,
                    email=email_raw or None,
                    role=role_raw,
                    status="skipped",
                    reason="Admin accounts cannot be provisioned via bulk import.",
                )
            )
            continue

        if role_raw not in ALLOWED_BULK_ROLES:
            skipped_count += 1
            results.append(
                BulkImportRowResult(
                    row_number=row_number,
                    full_name=full_name,
                    phone=phone_raw,
                    email=email_raw or None,
                    role=role_raw,
                    status="skipped",
                    reason=f"Invalid role '{role_raw}'. Must be one of: {', '.join(sorted(ALLOWED_BULK_ROLES))}.",
                )
            )
            continue

        # Validate phone format
        normalized_phone = normalize_indian_phone(phone_raw)
        if not normalized_phone:
            skipped_count += 1
            results.append(
                BulkImportRowResult(
                    row_number=row_number,
                    full_name=full_name,
                    phone=phone_raw,
                    email=email_raw or None,
                    role=role_raw,
                    status="skipped",
                    reason=f"Invalid phone number format '{phone_raw}'. Expected 10-digit Indian mobile number.",
                )
            )
            continue

        # Validate duplicate phone
        if normalized_phone in existing_phones:
            skipped_count += 1
            results.append(
                BulkImportRowResult(
                    row_number=row_number,
                    full_name=full_name,
                    phone=normalized_phone,
                    email=email_raw or None,
                    role=role_raw,
                    status="skipped",
                    reason=f"Phone number '{normalized_phone}' is already registered to an existing account.",
                )
            )
            continue

        if normalized_phone in seen_batch_phones:
            skipped_count += 1
            results.append(
                BulkImportRowResult(
                    row_number=row_number,
                    full_name=full_name,
                    phone=normalized_phone,
                    email=email_raw or None,
                    role=role_raw,
                    status="skipped",
                    reason=f"Duplicate phone number '{normalized_phone}' within the same import file.",
                )
            )
            continue
        seen_batch_phones.add(normalized_phone)

        # Validate email if provided
        email: str | None = None
        if email_raw:
            if not EMAIL_REGEX.match(email_raw):
                skipped_count += 1
                results.append(
                    BulkImportRowResult(
                        row_number=row_number,
                        full_name=full_name,
                        phone=normalized_phone,
                        email=email_raw,
                        role=role_raw,
                        status="skipped",
                        reason=f"Invalid email address format '{email_raw}'.",
                    )
                )
                continue
            email = email_raw

        # Role-specific scope validations
        dept_id: uuid.UUID | None = None
        zone_id: uuid.UUID | None = None
        ward_id: uuid.UUID | None = None

        if role_raw == StaffRole.DEPARTMENT_STAFF.value:
            if not dept_code or dept_code not in dept_map:
                skipped_count += 1
                results.append(
                    BulkImportRowResult(
                        row_number=row_number,
                        full_name=full_name,
                        phone=normalized_phone,
                        email=email,
                        role=role_raw,
                        status="skipped",
                        reason=f"Role 'department_staff' requires a valid department_code. '{dept_code}' not found.",
                    )
                )
                continue
            dept_id = dept_map[dept_code]

        elif role_raw == StaffRole.ZONAL_SUPERVISOR.value:
            if not zone_code or zone_code not in zone_map:
                skipped_count += 1
                results.append(
                    BulkImportRowResult(
                        row_number=row_number,
                        full_name=full_name,
                        phone=normalized_phone,
                        email=email,
                        role=role_raw,
                        status="skipped",
                        reason=f"Role 'zonal_supervisor' requires a valid zone_code. '{zone_code}' not found.",
                    )
                )
                continue
            zone_id = zone_map[zone_code]

        elif role_raw == StaffRole.FIELD_WORKER.value:
            if not dept_code or dept_code not in dept_map:
                skipped_count += 1
                results.append(
                    BulkImportRowResult(
                        row_number=row_number,
                        full_name=full_name,
                        phone=normalized_phone,
                        email=email,
                        role=role_raw,
                        status="skipped",
                        reason=f"Role 'field_worker' requires a valid department_code. '{dept_code}' not found.",
                    )
                )
                continue
            if not ward_num_raw or not ward_num_raw.isdigit() or int(ward_num_raw) not in ward_map:
                skipped_count += 1
                results.append(
                    BulkImportRowResult(
                        row_number=row_number,
                        full_name=full_name,
                        phone=normalized_phone,
                        email=email,
                        role=role_raw,
                        status="skipped",
                        reason=f"Role 'field_worker' requires a valid ward_number. '{ward_num_raw}' not found.",
                    )
                )
                continue
            dept_id = dept_map[dept_code]
            ward_id = ward_map[int(ward_num_raw)]

        elif role_raw == StaffRole.CORPORATOR.value:
            if not ward_num_raw or not ward_num_raw.isdigit() or int(ward_num_raw) not in ward_map:
                skipped_count += 1
                results.append(
                    BulkImportRowResult(
                        row_number=row_number,
                        full_name=full_name,
                        phone=normalized_phone,
                        email=email,
                        role=role_raw,
                        status="skipped",
                        reason=f"Role 'corporator' requires a valid ward_number. '{ward_num_raw}' not found.",
                    )
                )
                continue
            target_ward_id = ward_map[int(ward_num_raw)]
            if target_ward_id in existing_corporator_wards:
                skipped_count += 1
                results.append(
                    BulkImportRowResult(
                        row_number=row_number,
                        full_name=full_name,
                        phone=normalized_phone,
                        email=email,
                        role=role_raw,
                        status="skipped",
                        reason=f"Ward {ward_num_raw} already has an assigned elected representative.",
                    )
                )
                continue
            ward_id = target_ward_id

        # Row is fully validated
        if dry_run:
            created_count += 1
            results.append(
                BulkImportRowResult(
                    row_number=row_number,
                    full_name=full_name,
                    phone=normalized_phone,
                    email=email,
                    role=role_raw,
                    status="would_create",
                    reason=None,
                    setup_link_dispatched=False,
                )
            )
        else:
            # 7. Real account creation & onboarding
            setup_token = secrets.token_urlsafe(32)
            auth_user_id = uuid.uuid4()

            try:
                sb_client = get_supabase_admin_client()
                sb_res = sb_client.auth.admin.create_user(
                    {
                        "email": email or f"{normalized_phone.replace('+', '')}@civicbrain.local",
                        "phone": normalized_phone,
                        "email_confirm": True,
                        "phone_confirm": True,
                        "user_metadata": {
                            "full_name": full_name,
                            "org_id": str(claims.org_id),
                            "role": role_raw,
                        },
                    }
                )
                if sb_res and sb_res.user and sb_res.user.id:
                    auth_user_id = uuid.UUID(sb_res.user.id)
            except Exception as exc:
                logger.warning("Supabase Auth admin create_user fallback/notice: %s", exc)

            # Create UserAccount
            user_acc = UserAccount(
                id=auth_user_id,
                organization_id=claims.org_id,
                email=email,
                phone=normalized_phone,
                full_name=full_name,
                is_active=True,
                mfa_enabled=False,
            )
            db.add(user_acc)
            await db.flush()

            # Create UserRoleAssignment
            assignment = UserRoleAssignment(
                user_id=auth_user_id,
                organization_id=claims.org_id,
                role=StaffRole(role_raw),
                department_id=dept_id,
                zone_id=zone_id,
                ward_id=ward_id,
            )
            db.add(assignment)

            # If corporator, create ElectedRepresentative entry
            if role_raw == StaffRole.CORPORATOR.value and ward_id:
                rep = ElectedRepresentative(
                    organization_id=claims.org_id,
                    ward_id=ward_id,
                    user_id=auth_user_id,
                    full_name=full_name,
                    term_start=date.today(),
                    term_end=date.today() + timedelta(days=5 * 365),
                )
                db.add(rep)
                existing_corporator_wards.add(ward_id)

            # Dispatch passwordless setup invitation link
            await dispatch_account_setup_invitation(
                user_id=str(auth_user_id),
                org_id=str(claims.org_id),
                phone=normalized_phone,
                email=email,
                full_name=full_name,
                setup_token=setup_token,
            )

            existing_phones.add(normalized_phone)
            created_count += 1
            results.append(
                BulkImportRowResult(
                    row_number=row_number,
                    full_name=full_name,
                    phone=normalized_phone,
                    email=email,
                    role=role_raw,
                    status="created",
                    reason=None,
                    setup_link_dispatched=True,
                )
            )

    # 8. Record audit log entry in staff_bulk_import_log
    import_log = StaffBulkImportLog(
        organization_id=claims.org_id,
        admin_user_id=claims.user_id,
        file_name=file.filename or "bulk_import.csv",
        file_hash=file_hash,
        total_rows=total_rows,
        created_count=created_count,
        skipped_count=skipped_count,
        is_dry_run=dry_run,
    )
    db.add(import_log)
    await db.commit()

    return BulkImportResponse(
        file_name=file.filename or "bulk_import.csv",
        file_hash=file_hash,
        dry_run=dry_run,
        total_rows=total_rows,
        created_count=created_count,
        skipped_count=skipped_count,
        results=results,
    )
