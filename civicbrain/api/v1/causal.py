"""API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality (§A13)."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.causal.graph import CausalGraphService, CyclicCausalDependencyError
from civicbrain.domain.causal.models import IncidentCausalLink
from civicbrain.domain.identity.jwt import CurrentUserClaims, get_current_user_claims
from civicbrain.domain.identity.models import StaffRole
from civicbrain.domain.intake.models import Incident
from civicbrain.infra.database import get_db
from civicbrain.schemas.causal import (
    CausalLinkResponse,
    CreateCausalLinkRequest,
    DownstreamSymptomsResponse,
)

router = APIRouter()
graph_service = CausalGraphService()


@router.post(
    "/links",
    response_model=CausalLinkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a directed causal link from root cause to symptom incident",
)
async def create_causal_link(
    payload: CreateCausalLinkRequest,
    claims: CurrentUserClaims = Depends(get_current_user_claims),
    db: AsyncSession = Depends(get_db),
) -> CausalLinkResponse:
    """Create a causal link with strict multi-hop cycle prevention and staff authorization."""
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing organization scope in token"
        )

    # Only admin, dispatcher, or zonal_supervisor can establish causal links
    if claims.role not in (StaffRole.ADMIN, StaffRole.DISPATCHER, StaffRole.ZONAL_SUPERVISOR):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin, dispatcher, or zonal supervisor can manage causal root-cause links",
        )

    # 1. Fetch both incidents and verify they belong to caller's organization
    incidents_stmt = select(Incident).where(
        Incident.id.in_([payload.root_incident_id, payload.symptom_incident_id]),
        Incident.organization_id == claims.org_id,
    )
    inc_res = await db.execute(incidents_stmt)
    incidents = {inc.id: inc for inc in inc_res.scalars().all()}

    if payload.root_incident_id not in incidents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Root cause incident not found in organization",
        )
    if payload.symptom_incident_id not in incidents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Symptom incident not found in organization",
        )

    # 2. Fetch existing causal graph edges for the organization to verify acyclicity
    existing_edges_stmt = select(
        IncidentCausalLink.root_incident_id,
        IncidentCausalLink.symptom_incident_id,
    ).where(IncidentCausalLink.organization_id == claims.org_id)
    edges_res = await db.execute(existing_edges_stmt)
    existing_edges = [(row[0], row[1]) for row in edges_res.all()]

    # 3. Application-level multi-hop cycle check
    try:
        graph_service.validate_acyclic_addition(
            existing_edges=existing_edges,
            new_root_id=payload.root_incident_id,
            new_symptom_id=payload.symptom_incident_id,
        )
    except CyclicCausalDependencyError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e

    # 4. Insert link
    link = IncidentCausalLink(
        organization_id=claims.org_id,
        root_incident_id=payload.root_incident_id,
        symptom_incident_id=payload.symptom_incident_id,
        relation_type=payload.relation_type,
        confidence=payload.confidence,
        established_by=claims.user_id,
        notes=payload.notes,
    )
    db.add(link)

    # 5. Update root incident metadata (downstream count & boost)
    all_downstream = graph_service.find_all_downstream_symptoms(
        root_id=payload.root_incident_id,
        edges=existing_edges + [(payload.root_incident_id, payload.symptom_incident_id)],
    )

    root_inc = incidents[payload.root_incident_id]
    root_inc.is_root_cause = True
    root_inc.downstream_symptom_count = len(all_downstream)

    # Fetch child priorities to compute boost
    if all_downstream:
        children_stmt = select(Incident.id, Incident.priority_score).where(
            Incident.id.in_(all_downstream)
        )
        children_res = await db.execute(children_stmt)
        child_priorities = {row[0]: float(row[1]) for row in children_res.all()}
        boost_res = graph_service.calculate_root_cause_priority(
            root_incident_id=root_inc.id,
            base_priority_score=root_inc.priority_score,
            child_priority_scores=child_priorities,
        )
        root_inc.root_cause_priority_boost = boost_res.priority_boost
        root_inc.priority_score = boost_res.final_priority_score

    await db.commit()
    await db.refresh(link)

    return CausalLinkResponse(
        id=link.id,
        organization_id=link.organization_id,
        root_incident_id=link.root_incident_id,
        symptom_incident_id=link.symptom_incident_id,
        relation_type=link.relation_type,
        confidence=link.confidence,
        established_by=link.established_by,
        notes=link.notes,
        created_at=link.created_at,
    )


@router.get(
    "/incidents/{incident_id}/downstream",
    response_model=DownstreamSymptomsResponse,
    summary="Get all downstream symptoms and blast radius for a root cause incident",
)
async def get_downstream_symptoms(
    incident_id: uuid.UUID,
    claims: CurrentUserClaims = Depends(get_current_user_claims),
    db: AsyncSession = Depends(get_db),
) -> DownstreamSymptomsResponse:
    """Retrieve all downstream symptom incidents and priority boost breakdown."""
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing organization scope in token"
        )

    inc_stmt = select(Incident).where(
        Incident.id == incident_id,
        Incident.organization_id == claims.org_id,
    )
    inc_res = await db.execute(inc_stmt)
    incident = inc_res.scalars().first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")

    edges_stmt = select(
        IncidentCausalLink.root_incident_id,
        IncidentCausalLink.symptom_incident_id,
    ).where(IncidentCausalLink.organization_id == claims.org_id)
    edges_res = await db.execute(edges_stmt)
    edges = [(row[0], row[1]) for row in edges_res.all()]

    downstream_ids = graph_service.find_all_downstream_symptoms(incident_id, edges)

    return DownstreamSymptomsResponse(
        root_incident_id=incident.id,
        downstream_symptom_count=len(downstream_ids),
        downstream_incident_ids=downstream_ids,
        base_priority_score=incident.priority_score - incident.root_cause_priority_boost,
        priority_boost=incident.root_cause_priority_boost,
        final_priority_score=incident.priority_score,
    )
