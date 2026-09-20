"""Live Supabase Phase 4 GIS Core, Spatial Clustering RPC & Cross-Tenant RLS Test Suite (§A14).

In strict accordance with:
- Hard Rule 5: RLS is the real authorization boundary, tested via client SDK using real per-role JWTs.
- User Correction 1: get_incident_clusters runs as calling role (SECURITY INVOKER) and inherits table-level RLS on incident.
  Org A calling the function with Org B's organization_id returns zero rows, using real seeded data and a real JWT.
- Standing Invariant 4: Scoped grants, zero blanket GRANT ALL.
- Standing Invariant 5: Real seeded data, live command executions, teardown in finally blocks.
"""

import json
import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from supabase import Client, create_client

from civicbrain.infra.config import settings
from civicbrain.main import app


def is_live_supabase_configured() -> bool:
    """Check if real Supabase credentials are provided in settings."""
    url = settings.SUPABASE_URL
    return bool(
        url
        and not url.startswith("https://mock")
        and not url.startswith("https://your-project")
        and settings.SUPABASE_ANON_KEY
        and not settings.SUPABASE_ANON_KEY.startswith("mock")
        and settings.SUPABASE_SERVICE_ROLE_KEY
        and not settings.SUPABASE_SERVICE_ROLE_KEY.startswith("mock")
    )


@pytest.mark.skipif(
    not is_live_supabase_configured(),
    reason="Requires live Supabase project credentials in .env",
)
@pytest.mark.asyncio
async def test_live_supabase_phase4_gis():
    """Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and GeoJSON endpoints."""
    run_id = str(uuid.uuid4())[:8]
    service_client: Client = create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )

    created_user_ids: list[str] = []
    created_org_ids: list[str] = []

    try:
        # =====================================================================
        # 1. Seed Multi-Tenant Hierarchy (Org A and Org B) via privileged service_role
        # =====================================================================

        # Org A (Bengaluru)
        org_a_res = (
            service_client.table("organization")
            .insert(
                {
                    "name": f"BBMP GIS Org A {run_id}",
                    "code": f"BBMP_GIS_{run_id}",
                    "ulb_type": "municipal_corporation",
                    "state": "Karnataka",
                }
            )
            .execute()
        )
        org_a_id = org_a_res.data[0]["id"]
        created_org_ids.append(org_a_id)

        # Org B (Hyderabad)
        org_b_res = (
            service_client.table("organization")
            .insert(
                {
                    "name": f"GHMC GIS Org B {run_id}",
                    "code": f"GHMC_GIS_{run_id}",
                    "ulb_type": "municipal_corporation",
                    "state": "Telangana",
                }
            )
            .execute()
        )
        org_b_id = org_b_res.data[0]["id"]
        created_org_ids.append(org_b_id)

        # Zone A & Ward A in Org A
        zone_a_res = (
            service_client.table("zone")
            .insert(
                {
                    "organization_id": org_a_id,
                    "name": f"Zone A {run_id}",
                    "code": f"ZA_{run_id}",
                    "geom": "SRID=4326;POLYGON((77.5 12.9, 77.6 12.9, 77.6 13.0, 77.5 13.0, 77.5 12.9))",
                }
            )
            .execute()
        )
        zone_a_id = zone_a_res.data[0]["id"]

        ward_a_res = (
            service_client.table("ward")
            .insert(
                {
                    "organization_id": org_a_id,
                    "zone_id": zone_a_id,
                    "ward_number": 101,
                    "name": f"Ward 101 A {run_id}",
                    "code": f"W101A_{run_id}",
                    "geom": "SRID=4326;POLYGON((77.51 12.91, 77.59 12.91, 77.59 12.99, 77.51 12.99, 77.51 12.91))",
                    "centroid": "SRID=4326;POINT(77.55 12.95)",
                }
            )
            .execute()
        )
        ward_a_id = ward_a_res.data[0]["id"]

        # Zone B & Ward B in Org B
        zone_b_res = (
            service_client.table("zone")
            .insert(
                {
                    "organization_id": org_b_id,
                    "name": f"Zone B {run_id}",
                    "code": f"ZB_{run_id}",
                    "geom": "SRID=4326;POLYGON((78.4 17.3, 78.5 17.3, 78.5 17.4, 78.4 17.4, 78.4 17.3))",
                }
            )
            .execute()
        )
        zone_b_id = zone_b_res.data[0]["id"]

        ward_b_res = (
            service_client.table("ward")
            .insert(
                {
                    "organization_id": org_b_id,
                    "zone_id": zone_b_id,
                    "ward_number": 201,
                    "name": f"Ward 201 B {run_id}",
                    "code": f"W201B_{run_id}",
                    "geom": "SRID=4326;POLYGON((78.41 17.31, 78.49 17.31, 78.49 17.39, 78.41 17.39, 78.41 17.31))",
                    "centroid": "SRID=4326;POINT(78.45 17.35)",
                }
            )
            .execute()
        )
        ward_b_id = ward_b_res.data[0]["id"]

        # Departments
        dept_a_res = (
            service_client.table("department")
            .insert(
                {
                    "organization_id": org_a_id,
                    "name": "Roads A",
                    "code": f"ROADS_A_{run_id}",
                }
            )
            .execute()
        )
        dept_a_id = dept_a_res.data[0]["id"]

        dept_b_res = (
            service_client.table("department")
            .insert(
                {
                    "organization_id": org_b_id,
                    "name": "Roads B",
                    "code": f"ROADS_B_{run_id}",
                }
            )
            .execute()
        )
        dept_b_id = dept_b_res.data[0]["id"]

        # =====================================================================
        # 2. Create Real Auth Users & Real JWTs for Org A and Org B Staff
        # =====================================================================
        def create_and_login_user(role_name: str, app_meta: dict) -> tuple[str, str, Client]:
            email = f"user_{role_name}_{run_id}@civicbrain.local"
            password = f"P4GisPass_{role_name}_{run_id}!2026"
            user_res = service_client.auth.admin.create_user(
                {
                    "email": email,
                    "password": password,
                    "email_confirm": True,
                    "app_metadata": app_meta,
                }
            )
            uid = user_res.user.id
            created_user_ids.append(uid)

            login_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
            login_res = login_client.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password,
                }
            )
            token = login_res.session.access_token
            assert token, f"Must obtain real JWT for role {role_name}"

            authed_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
            authed_client.postgrest.auth(token)
            return uid, token, authed_client

        # Staff in Org A
        staff_a_uid, staff_a_jwt, staff_a_client = create_and_login_user(
            "staff_a",
            {"org_id": org_a_id, "role": "admin"},
        )
        service_client.table("user_account").insert(
            {
                "id": staff_a_uid,
                "organization_id": org_a_id,
                "phone": f"+919800{run_id[:4]}11",
                "full_name": f"Staff A User {run_id}",
            }
        ).execute()
        service_client.table("user_role_assignment").insert(
            {
                "user_id": staff_a_uid,
                "organization_id": org_a_id,
                "role": "admin",
            }
        ).execute()

        # Staff in Org B
        staff_b_uid, staff_b_jwt, staff_b_client = create_and_login_user(
            "staff_b",
            {"org_id": org_b_id, "role": "admin"},
        )
        service_client.table("user_account").insert(
            {
                "id": staff_b_uid,
                "organization_id": org_b_id,
                "phone": f"+919800{run_id[:4]}12",
                "full_name": f"Staff B User {run_id}",
            }
        ).execute()
        service_client.table("user_role_assignment").insert(
            {
                "user_id": staff_b_uid,
                "organization_id": org_b_id,
                "role": "admin",
            }
        ).execute()

        # =====================================================================
        # 3. Seed Incidents in Org B (4 in a cluster <20m apart, 1 isolated >10km away)
        # =====================================================================
        # Clustered incidents around (78.4500, 17.3500)
        cluster_b_coords = [
            (78.45000, 17.35000),
            (78.45005, 17.35005),
            (78.45010, 17.35010),
            (78.45015, 17.35015),
        ]
        org_b_cluster_incident_ids: list[str] = []
        for lon, lat in cluster_b_coords:
            inc_res = (
                service_client.table("incident")
                .insert(
                    {
                        "organization_id": org_b_id,
                        "department_id": dept_b_id,
                        "ward_id": ward_b_id,
                        "category_code": "POTHOLE",
                        "geom": f"SRID=4326;POINT({lon} {lat})",
                        "status": "reported",
                        "severity": 3,
                    }
                )
                .execute()
            )
            org_b_cluster_incident_ids.append(inc_res.data[0]["id"])

        # Isolated incident far away from cluster (78.55, 17.45)
        iso_res = (
            service_client.table("incident")
            .insert(
                {
                    "organization_id": org_b_id,
                    "department_id": dept_b_id,
                    "ward_id": ward_b_id,
                    "category_code": "POTHOLE",
                    "geom": "SRID=4326;POINT(78.5500 17.4500)",
                    "status": "reported",
                    "severity": 2,
                }
            )
            .execute()
        )
        isolated_b_incident_id = iso_res.data[0]["id"]

        # Also seed 1 incident in Org A
        (
            service_client.table("incident")
            .insert(
                {
                    "organization_id": org_a_id,
                    "department_id": dept_a_id,
                    "ward_id": ward_a_id,
                    "category_code": "STREETLIGHT",
                    "geom": "SRID=4326;POINT(77.5500 12.9500)",
                    "status": "reported",
                    "severity": 1,
                }
            )
            .execute()
        )

        # =====================================================================
        # 4. Mandatory User Correction 1 Verification:
        # Org A calling get_incident_clusters with Org B's organization_id returns ZERO rows
        # using real seeded data and a real JWT.
        # =====================================================================
        cross_tenant_rpc_res = staff_a_client.rpc(
            "get_incident_clusters",
            {
                "p_organization_id": org_b_id,
                "p_department_id": None,
                "p_eps_meters": 100.0,
                "p_min_points": 3,
            },
        ).execute()

        assert len(cross_tenant_rpc_res.data) == 0, (
            "Cross-tenant leakage violation! Org A staff calling get_incident_clusters with "
            "Org B's organization_id MUST return zero rows due to incident table RLS inheritance."
        )

        # =====================================================================
        # 5. Legitimate Intra-Tenant Cluster Detection (Org B calls with Org B's ID)
        # =====================================================================
        intra_tenant_rpc_res = staff_b_client.rpc(
            "get_incident_clusters",
            {
                "p_organization_id": org_b_id,
                "p_department_id": None,
                "p_eps_meters": 100.0,
                "p_min_points": 3,
            },
        ).execute()

        assert len(intra_tenant_rpc_res.data) == 1, (
            "Org B should detect exactly 1 cluster for the 4 proximate incidents."
        )
        cluster_data = intra_tenant_rpc_res.data[0]
        assert cluster_data["incident_count"] == 4
        # Assert all 4 clustered incidents are in the cluster
        for inc_id in org_b_cluster_incident_ids:
            assert inc_id in cluster_data["incident_ids"]
        # Assert isolated incident is NOT in cluster
        assert isolated_b_incident_id not in cluster_data["incident_ids"]

        # Assert centroid GeoJSON is valid Point geometry
        centroid = json.loads(cluster_data["centroid_geojson"])
        assert centroid["type"] == "Point"
        assert len(centroid["coordinates"]) == 2
        # Coordinates should be close to 78.45, 17.35
        assert abs(centroid["coordinates"][0] - 78.45) < 0.01
        assert abs(centroid["coordinates"][1] - 17.35) < 0.01

        # =====================================================================
        # 6. REST API Live Roundtrips
        # =====================================================================
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            # 6.1 Ward GeoJSON
            res_ward = await client.get(f"/v1/gis/wards/geojson?organization_id={org_a_id}")
            assert res_ward.status_code == 200
            ward_fc = res_ward.json()
            assert ward_fc["type"] == "FeatureCollection"
            assert len(ward_fc["features"]) == 1
            assert ward_fc["features"][0]["properties"]["ward_number"] == 101

            # 6.2 Incident GeoJSON with spatial bounding box
            # Bounding box covering only the cluster area (78.44 to 78.46, 17.34 to 17.36)
            res_bbox_cluster = await client.get(
                f"/v1/gis/incidents/geojson?organization_id={org_b_id}&bbox=78.44,17.34,78.46,17.36"
            )
            assert res_bbox_cluster.status_code == 200
            fc_cluster = res_bbox_cluster.json()
            assert fc_cluster["type"] == "FeatureCollection"
            # Must return the 4 clustered incidents, omitting the isolated one
            assert len(fc_cluster["features"]) == 4

            # Bounding box covering only the isolated area (78.54 to 78.56, 17.44 to 17.46)
            res_bbox_iso = await client.get(
                f"/v1/gis/incidents/geojson?organization_id={org_b_id}&bbox=78.54,17.44,78.56,17.46"
            )
            assert res_bbox_iso.status_code == 200
            fc_iso = res_bbox_iso.json()
            assert len(fc_iso["features"]) == 1
            assert fc_iso["features"][0]["id"] == isolated_b_incident_id

            # 6.3 REST Clusters endpoint
            res_clusters = await client.get(
                f"/v1/gis/clusters?organization_id={org_b_id}&eps_meters=100&min_points=3"
            )
            assert res_clusters.status_code == 200
            clusters = res_clusters.json()
            assert len(clusters) == 1
            assert clusters[0]["incident_count"] == 4

    finally:
        # =====================================================================
        # 7. Complete Teardown via privileged service_role in finally block
        # =====================================================================
        for oid in created_org_ids:
            try:
                service_client.table("organization").delete().eq("id", oid).execute()
            except Exception:
                pass
        for uid in created_user_ids:
            try:
                service_client.auth.admin.delete_user(uid)
            except Exception:
                pass
