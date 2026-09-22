"""Citizen Transparency, Jan Sunwai Ledger, Differential Privacy & Civic Assistant Domain Services (§A21, §A23)."""

import hashlib
import logging
import math
import re
import secrets
import struct
import uuid
from datetime import UTC, date, datetime, timedelta
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.analytics.services import compute_csi
from civicbrain.domain.identity.models import Department
from civicbrain.domain.intake.models import Incident, IncidentStatus
from civicbrain.domain.prioritization.models import WardEquityCredibility
from civicbrain.domain.transparency.models import (
    JanSunwaiLedgerEntry,
    NagarPragatiCitySnapshot,
)
from civicbrain.schemas.transparency import (
    CivicAssistantQueryRequest,
    CivicAssistantQueryResponse,
    IncidentLedgerChainResponse,
    JanSunwaiLedgerResponse,
    NagarPragatiResponse,
)

logger = logging.getLogger(__name__)

GENESIS_PREV_HASH = "0" * 64


def extract_coordinates(geom: Any) -> tuple[float, float]:
    """Extracts (longitude, latitude) from GeoAlchemy geometry, WKBElement, or WKT string."""
    if hasattr(geom, "x") and hasattr(geom, "y"):
        return float(geom.x), float(geom.y)

    geom_str = str(geom)
    match = re.search(r"POINT\s*\(\s*([-\d.]+)\s+([-\d.]+)\s*\)", geom_str, re.IGNORECASE)
    if match:
        return float(match.group(1)), float(match.group(2))

    # Binary WKB / EWKB parsing via struct
    data = getattr(geom, "data", None)
    if isinstance(data, (bytes, bytearray)):
        b = bytes(data)
        if len(b) >= 21:
            order = "<" if b[0] == 1 else ">"
            geom_type = struct.unpack(order + "I", b[1:5])[0]
            offset = 5
            if geom_type & 0x20000000:  # PostGIS EWKB SRID flag
                offset += 4
            lon, lat = struct.unpack(order + "dd", b[offset : offset + 16])
            return float(lon), float(lat)

    raise ValueError(f"Unable to extract coordinates from geometry: {geom}")


def generate_laplace_dp_perturbation(
    lon: float,
    lat: float,
    created_at: datetime,
) -> tuple[float, float, timedelta]:
    """Generates 2D planar Laplace spatial noise and 1D continuous Laplace temporal jitter (§A23).

    - Spatial budget: epsilon_geom = 0.8, sensitivity = 100m -> b = 125m.
      Bounded to [-250m, +250m], guaranteed minimal displacement >= 30m.
    - Temporal budget: epsilon_time = 0.2, sensitivity = 15 min -> b = 75 min.
      Bounded to [-120 min, +120 min], guaranteed minimal displacement >= 5 min.
    """
    # 1. Spatial Laplace noise (Inverse CDF)
    sys_rand = secrets.SystemRandom()
    u_x = sys_rand.uniform(-0.4999, 0.4999)
    u_y = sys_rand.uniform(-0.4999, 0.4999)
    delta_x = -125.0 * (1.0 if u_x >= 0 else -1.0) * math.log(1.0 - 2.0 * abs(u_x))
    delta_y = -125.0 * (1.0 if u_y >= 0 else -1.0) * math.log(1.0 - 2.0 * abs(u_y))

    # Clamping & minimal distance guard
    delta_x = max(-250.0, min(250.0, delta_x))
    delta_y = max(-250.0, min(250.0, delta_y))
    if math.hypot(delta_x, delta_y) < 30.0:
        delta_x = 35.0 if delta_x >= 0 else -35.0
        delta_y = 35.0 if delta_y >= 0 else -35.0

    lat_rad = math.radians(lat)
    d_lat = delta_y / 111000.0
    d_lon = delta_x / (111000.0 * max(0.1, math.cos(lat_rad)))
    dp_lon = round(lon + d_lon, 6)
    dp_lat = round(lat + d_lat, 6)

    # 2. Temporal Laplace noise
    u_t = sys_rand.uniform(-0.4999, 0.4999)
    delta_t_min = -75.0 * (1.0 if u_t >= 0 else -1.0) * math.log(1.0 - 2.0 * abs(u_t))
    delta_t_min = max(-120.0, min(120.0, delta_t_min))
    if abs(delta_t_min) < 5.0:
        delta_t_min = 15.0 if delta_t_min >= 0 else -15.0

    time_offset = timedelta(minutes=round(delta_t_min, 1))
    return dp_lon, dp_lat, time_offset


def compute_entry_hash(
    prev_hash: str,
    incident_id: uuid.UUID,
    sequence_num: int,
    lifecycle_status: str,
    dp_lon: float,
    dp_lat: float,
    dp_timestamp: datetime,
    public_tracking_code: str,
) -> str:
    """Computes deterministic SHA-256 checkpoint hash for per-incident ledger chain (§A23)."""
    iso_ts = dp_timestamp.isoformat()
    wkt = f"POINT({dp_lon:.6f} {dp_lat:.6f})"
    payload = f"{prev_hash}:{incident_id}:{sequence_num}:{lifecycle_status}:{wkt}:{iso_ts}:{public_tracking_code}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


async def record_ledger_checkpoint(
    db: AsyncSession,
    incident_id: uuid.UUID,
    lifecycle_status: str,
    sla_status: str = "within_sla",
    resolution_media_count: int = 0,
    is_appealed: bool = False,
    predicted_eta_hours: float | None = None,
    milestone_time: datetime | None = None,
) -> JanSunwaiLedgerEntry:
    """Publishes an immutable milestone checkpoint to the Jan Sunwai Ledger (§A23).

    Anti-Composition Invariant:
    - DP spatial noise (dp_geom) and temporal offset (Delta t) are computed ONCE on sequence 0
      and strictly reused across all subsequent checkpoints for that incident.
    """
    # 1. Fetch incident
    inc_res = await db.execute(select(Incident).where(Incident.id == incident_id))
    incident = inc_res.scalar_one_or_none()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident {incident_id} not found",
        )

    # 2. Query existing checkpoints for this incident
    chain_res = await db.execute(
        select(JanSunwaiLedgerEntry)
        .where(JanSunwaiLedgerEntry.incident_id == incident_id)
        .order_by(JanSunwaiLedgerEntry.sequence_num.asc())
    )
    existing_entries = list(chain_res.scalars().all())

    tracking_code = f"CB-{str(incident_id)[:8].upper()}"
    base_time = milestone_time or datetime.now(UTC)

    if not existing_entries:
        # Checkpoint 0 (Genesis / REPORTED)
        sequence_num = 0
        prev_hash = GENESIS_PREV_HASH

        # Extract true coordinates
        true_lon, true_lat = extract_coordinates(incident.geom)
        dp_lon, dp_lat, time_offset = generate_laplace_dp_perturbation(
            lon=true_lon,
            lat=true_lat,
            created_at=incident.created_at or base_time,
        )
        dp_timestamp = (incident.created_at or base_time) + time_offset
    else:
        # Subsequent checkpoints: sequence k >= 1
        sequence_num = existing_entries[-1].sequence_num + 1
        prev_hash = existing_entries[-1].entry_hash

        # Anti-Composition: Reuse sequence 0 dp_geom and delta_t
        seq0 = existing_entries[0]
        dp_lon, dp_lat = extract_coordinates(seq0.dp_geom)

        inc_created = incident.created_at or seq0.created_at
        delta_t = seq0.dp_timestamp - inc_created
        dp_timestamp = base_time + delta_t

    # 3. Compute cryptographic entry hash
    entry_hash = compute_entry_hash(
        prev_hash=prev_hash,
        incident_id=incident_id,
        sequence_num=sequence_num,
        lifecycle_status=lifecycle_status,
        dp_lon=dp_lon,
        dp_lat=dp_lat,
        dp_timestamp=dp_timestamp,
        public_tracking_code=tracking_code,
    )

    dp_geom_wkt = f"SRID=4326;POINT({dp_lon:.6f} {dp_lat:.6f})"

    ledger_entry = JanSunwaiLedgerEntry(
        organization_id=incident.organization_id,
        incident_id=incident_id,
        sequence_num=sequence_num,
        public_tracking_code=tracking_code,
        category_code=incident.category_code,
        department_id=incident.department_id,
        ward_id=incident.ward_id,
        dp_geom=dp_geom_wkt,
        dp_timestamp=dp_timestamp,
        lifecycle_status=lifecycle_status,
        sla_status=sla_status,
        predicted_eta_hours=predicted_eta_hours,
        resolution_media_count=resolution_media_count,
        is_appealed=is_appealed,
        prev_hash=prev_hash,
        entry_hash=entry_hash,
    )
    db.add(ledger_entry)
    await db.commit()
    await db.refresh(ledger_entry)
    return ledger_entry


def verify_incident_ledger_chain(
    entries: list[JanSunwaiLedgerEntry],
) -> tuple[bool, str | None]:
    """Validates the cryptographic integrity of an incident's checkpoint chain (§A23)."""
    if not entries:
        return True, None

    sorted_entries = sorted(entries, key=lambda e: e.sequence_num)
    for i, entry in enumerate(sorted_entries):
        if entry.sequence_num != i:
            return False, f"Sequence gap detected: expected index {i}, found {entry.sequence_num}"

        expected_prev = GENESIS_PREV_HASH if i == 0 else sorted_entries[i - 1].entry_hash
        if entry.prev_hash != expected_prev:
            return (
                False,
                f"Prev hash mismatch at seq {i}: expected {expected_prev}, found {entry.prev_hash}",
            )

        dp_lon, dp_lat = extract_coordinates(entry.dp_geom)
        recomputed = compute_entry_hash(
            prev_hash=entry.prev_hash,
            incident_id=entry.incident_id,
            sequence_num=entry.sequence_num,
            lifecycle_status=entry.lifecycle_status,
            dp_lon=dp_lon,
            dp_lat=dp_lat,
            dp_timestamp=entry.dp_timestamp,
            public_tracking_code=entry.public_tracking_code,
        )
        if entry.entry_hash != recomputed:
            return (
                False,
                f"Tamper detected at seq {i}: stored {entry.entry_hash} != recomputed {recomputed}",
            )

    return True, None


async def get_incident_ledger_chain(
    db: AsyncSession,
    incident_id: uuid.UUID,
) -> IncidentLedgerChainResponse:
    """Retrieves full milestone chain and cryptographic validity status for an incident (§A23)."""
    res = await db.execute(
        select(JanSunwaiLedgerEntry)
        .where(JanSunwaiLedgerEntry.incident_id == incident_id)
        .order_by(JanSunwaiLedgerEntry.sequence_num.asc())
    )
    entries = list(res.scalars().all())
    if not entries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No ledger entries found for incident {incident_id}",
        )

    is_valid, error_msg = verify_incident_ledger_chain(entries)
    code = entries[0].public_tracking_code

    response_items = []
    for e in entries:
        lon, lat = extract_coordinates(e.dp_geom)
        response_items.append(
            JanSunwaiLedgerResponse(
                id=e.id,
                organization_id=e.organization_id,
                incident_id=e.incident_id,
                sequence_num=e.sequence_num,
                public_tracking_code=e.public_tracking_code,
                category_code=e.category_code,
                department_id=e.department_id,
                ward_id=e.ward_id,
                dp_latitude=lat,
                dp_longitude=lon,
                dp_timestamp=e.dp_timestamp,
                lifecycle_status=e.lifecycle_status,
                sla_status=e.sla_status,
                predicted_eta_hours=e.predicted_eta_hours,
                resolution_media_count=e.resolution_media_count,
                is_appealed=e.is_appealed,
                prev_hash=e.prev_hash,
                entry_hash=e.entry_hash,
                created_at=e.created_at,
            )
        )

    return IncidentLedgerChainResponse(
        incident_id=incident_id,
        public_tracking_code=code,
        chain_length=len(entries),
        is_valid=is_valid,
        error_message=error_msg,
        entries=response_items,
    )


async def compute_nagar_pragati(
    db: AsyncSession,
    organization_id: uuid.UUID,
    snapshot_date: date | None = None,
    period_type: str = "monthly",
    persist: bool = True,
) -> NagarPragatiResponse:
    """Computes city-wide municipal progress and macro performance scorecard (§A21)."""
    target_date = snapshot_date or date.today()

    # Query organization incidents
    res = await db.execute(select(Incident).where(Incident.organization_id == organization_id))
    incidents = list(res.scalars().all())

    total_intake = len(incidents)
    resolved_incidents = [
        i for i in incidents if i.status in (IncidentStatus.RESOLVED, IncidentStatus.CONFIRMED)
    ]
    total_resolved = len(resolved_incidents)
    total_confirmed = sum(1 for i in incidents if i.status == IncidentStatus.CONFIRMED)
    total_appealed = sum(1 for i in incidents if i.status == IncidentStatus.APPEALED)

    # City MTTR & SLA
    durations = []
    within_sla = 0
    dept_stats: dict[uuid.UUID, dict[str, int]] = {}

    for i in resolved_incidents:
        if i.resolved_at and i.created_at:
            h = (i.resolved_at - i.created_at).total_seconds() / 3600.0
            durations.append(h)
            if h <= 72.0:
                within_sla += 1

    for i in incidents:
        if i.department_id not in dept_stats:
            dept_stats[i.department_id] = {"intake": 0, "resolved": 0}
        dept_stats[i.department_id]["intake"] += 1
        if i.status in (IncidentStatus.RESOLVED, IncidentStatus.CONFIRMED):
            dept_stats[i.department_id]["resolved"] += 1

    city_mttr = round(sum(durations) / len(durations), 2) if durations else None
    city_csi = compute_csi(total_confirmed, total_appealed, total_resolved)
    city_sla = round(within_sla / len(durations), 4) if durations else None

    # Department rankings
    dept_rankings = []
    if dept_stats:
        dept_ids = list(dept_stats.keys())
        d_res = await db.execute(select(Department).where(Department.id.in_(dept_ids)))
        dept_names = {d.id: d.name for d in d_res.scalars().all()}
        for d_id, stats in dept_stats.items():
            rate = round(stats["resolved"] / stats["intake"], 3) if stats["intake"] > 0 else 0.0
            dept_rankings.append(
                {
                    "department_id": str(d_id),
                    "department_name": dept_names.get(d_id, "Department"),
                    "total_intake": stats["intake"],
                    "total_resolved": stats["resolved"],
                    "resolution_rate": rate,
                }
            )
        dept_rankings.sort(key=lambda x: float(str(x["resolution_rate"])), reverse=True)

    # Ward Equity Distribution
    eq_res = await db.execute(
        select(WardEquityCredibility).where(
            WardEquityCredibility.organization_id == organization_id
        )
    )
    eq_rows = list(eq_res.scalars().all())
    ward_equity_dist = {str(r.ward_id): round(r.equity_gap, 3) for r in eq_rows}

    if persist:
        snap_query = select(NagarPragatiCitySnapshot).where(
            NagarPragatiCitySnapshot.organization_id == organization_id,
            NagarPragatiCitySnapshot.snapshot_date == target_date,
            NagarPragatiCitySnapshot.period_type == period_type,
        )
        snap_res = await db.execute(snap_query)
        snap = snap_res.scalar_one_or_none()
        if snap:
            snap.city_mttr_hours = city_mttr
            snap.city_csi = city_csi
            snap.city_sla_compliance_rate = city_sla
            snap.total_intake = total_intake
            snap.total_resolved = total_resolved
            snap.department_rankings = dept_rankings
            snap.ward_equity_distribution = ward_equity_dist
        else:
            snap = NagarPragatiCitySnapshot(
                organization_id=organization_id,
                snapshot_date=target_date,
                period_type=period_type,
                city_mttr_hours=city_mttr,
                city_csi=city_csi,
                city_sla_compliance_rate=city_sla,
                total_intake=total_intake,
                total_resolved=total_resolved,
                department_rankings=dept_rankings,
                ward_equity_distribution=ward_equity_dist,
            )
            db.add(snap)
        await db.commit()

    return NagarPragatiResponse(
        organization_id=organization_id,
        snapshot_date=target_date,
        period_type=period_type,
        city_mttr_hours=city_mttr,
        city_csi=city_csi,
        city_sla_compliance_rate=city_sla,
        total_intake=total_intake,
        total_resolved=total_resolved,
        department_rankings=dept_rankings,
        ward_equity_distribution=ward_equity_dist,
    )


# Multilingual template catalog for Civic Assistant (§A23, Bootstrap Principle §A3)
ASSISTANT_TEMPLATES: dict[str, dict[str, str]] = {
    "en": {
        "status_found": "Complaint {code} is currently {status}. Assigned to {dept}. Expected resolution within {eta} hours.",
        "status_resolved": "Complaint {code} has been resolved! Please confirm resolution or report an appeal if unsatisfied.",
        "not_found": "Tracking code {code} could not be found. Please verify the code or submit a new grievance.",
        "intake_guidance": "To file a grievance, provide a photo, brief description, and your ward/location. We route it automatically to the responsible department.",
        "general_help": "CivicBrain 24/7 Citizen Assistant: Track existing complaints, check ward progress, or file new municipal defects.",
    },
    "hi": {
        "status_found": "शिकायत {code} वर्तमान में {status} स्थिति में है। विभाग: {dept}। अनुमानित समाधान समय: {eta} घंटे।",
        "status_resolved": "शिकायत {code} का समाधान हो गया है! कृपया पुष्टि करें या असंतुष्ट होने पर अपील दर्ज करें।",
        "not_found": "ट्रैकिंग कोड {code} नहीं मिला। कृपया कोड जांचें या नई शिकायत दर्ज करें।",
        "intake_guidance": "शिकायत दर्ज करने के लिए फोटो, संक्षिप्त विवरण और स्थान भेजें। हम इसे संबंधित विभाग को अग्रेषित करेंगे।",
        "general_help": "सिविकब्रेन 24/7 नागरिक सहायक: शिकायत ट्रैक करें, वार्ड प्रगति देखें, या नई शिकायत दर्ज करें।",
    },
    "kn": {
        "status_found": "ದೂರು {code} ಪ್ರಸ್ತುತ {status} ಹಂತದಲ್ಲಿದೆ. ಇಲಾಖೆ: {dept}. ನಿರೀಕ್ಷಿತ ಪರಿಹಾರ ಸಮಯ: {eta} ಗಂಟೆಗಳು.",
        "status_resolved": "ದೂರು {code} ಪರಿಹರಿಸಲಾಗಿದೆ! ದಯವಿಟ್ಟು ಪರಿಹಾರವನ್ನು ದೃಢೀಕರಿಸಿ ಅಥವಾ ಅತೃಪ್ತರಾಗಿದ್ದರೆ ಮೇಲ್ಮನವಿ ಸಲ್ಲಿಸಿ.",
        "not_found": "ಟ್ರ್ಯಾಕಿಂಗ್ ಕೋಡ್ {code} ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಕೋಡ್ ಪರಿಶೀಲಿಸಿ ಅಥವಾ ಹೊಸ ದೂರು ದಾಖಲಿಸಿ.",
        "intake_guidance": "ದೂರು ಸಲ್ಲಿಸಲು ಫೋಟೋ, ವಿವರಣೆ ಮತ್ತು ಸ್ಥಳವನ್ನು ನೀಡಿ. ನಾವು ಅದನ್ನು ಸಂಬಂಧಿತ ಇಲಾಖೆಗೆ ನಿರ್ದೇಶಿಸುತ್ತೇವೆ.",
        "general_help": "ಸಿವಿಕ್‌ಬ್ರೈನ್ 24/7 ನಾಗರಿಕ ಸಹಾಯಕ: ದೂರುಗಳನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ, ವಾರ್ಡ್ ಪ್ರಗತಿ ನೋಡಿ ಅಥವಾ ಹೊಸ ದೂರು ದಾಖಲಿಸಿ.",
    },
}


async def process_civic_assistant_query(
    db: AsyncSession,
    request: CivicAssistantQueryRequest,
) -> CivicAssistantQueryResponse:
    """Processes natural language citizen inquiries with deterministic multilingual templates (§A23)."""
    lang = request.language_code.lower() if request.language_code in ASSISTANT_TEMPLATES else "en"
    templates = ASSISTANT_TEMPLATES[lang]
    text = request.query_text.strip()

    # 1. Extract Tracking Code if present in query or request
    code = request.tracking_code
    if not code:
        code_match = re.search(r"\bCB-[A-F0-9]{8}\b", text, re.IGNORECASE)
        if code_match:
            code = code_match.group(0).upper()

    if code:
        # Query ledger entry for tracking code
        q = (
            select(JanSunwaiLedgerEntry)
            .where(JanSunwaiLedgerEntry.public_tracking_code == code)
            .order_by(JanSunwaiLedgerEntry.sequence_num.desc())
        )
        res = await db.execute(q)
        latest = res.scalars().first()

        if latest:
            dept_res = await db.execute(
                select(Department).where(Department.id == latest.department_id)
            )
            dept = dept_res.scalar_one_or_none()
            dept_name = dept.name if dept else "Municipal Department"
            eta = latest.predicted_eta_hours or 48.0

            if latest.lifecycle_status in ("resolved", "confirmed"):
                resp_text = templates["status_resolved"].format(code=code)
                next_acts = ["confirm_resolution", "file_appeal"]
            else:
                resp_text = templates["status_found"].format(
                    code=code,
                    status=latest.lifecycle_status,
                    dept=dept_name,
                    eta=eta,
                )
                next_acts = ["track_progress", "contact_control_room"]

            return CivicAssistantQueryResponse(
                query_text=text,
                detected_language=lang,
                intent="STATUS_INQUIRY",
                response_text=resp_text,
                tracking_code=code,
                eta_explanation=f"{eta} hours remaining based on current ward backlog.",
                next_actions=next_acts,
            )
        else:
            return CivicAssistantQueryResponse(
                query_text=text,
                detected_language=lang,
                intent="STATUS_INQUIRY",
                response_text=templates["not_found"].format(code=code),
                tracking_code=code,
                next_actions=["check_code", "submit_new_intake"],
            )

    # 2. Intake intent or general inquiry
    intake_keywords = ["report", "complaint", "pothole", "garbage", "leak", "शिकायत", "ದೂರು"]
    if any(k in text.lower() for k in intake_keywords):
        return CivicAssistantQueryResponse(
            query_text=text,
            detected_language=lang,
            intent="INTAKE_GUIDANCE",
            response_text=templates["intake_guidance"],
            next_actions=["capture_photo", "submit_location"],
        )

    return CivicAssistantQueryResponse(
        query_text=text,
        detected_language=lang,
        intent="GENERAL_ASSISTANCE",
        response_text=templates["general_help"],
        next_actions=["track_complaint", "file_complaint", "view_ward_report_card"],
    )
