"""Unit tests for Phase 7 Causal Root-Cause Linking & Incident Graph Centrality (§A13)."""

import uuid

import pytest

from civicbrain.domain.causal.graph import (
    CausalGraphService,
    CyclicCausalDependencyError,
)


def test_direct_self_causation_rejected():
    """Verify linking incident A -> A raises CyclicCausalDependencyError."""
    service = CausalGraphService()
    node_a = uuid.uuid4()

    with pytest.raises(CyclicCausalDependencyError) as exc_info:
        service.validate_acyclic_addition(
            existing_edges=[],
            new_root_id=node_a,
            new_symptom_id=node_a,
        )
    assert "Direct self-causation is prohibited" in str(exc_info.value)


def test_2_node_cycle_rejected():
    """Verify linking B -> A when A -> B exists raises CyclicCausalDependencyError."""
    service = CausalGraphService()
    node_a = uuid.uuid4()
    node_b = uuid.uuid4()

    existing_edges = [(node_a, node_b)]  # A -> B

    with pytest.raises(CyclicCausalDependencyError) as exc_info:
        service.validate_acyclic_addition(
            existing_edges=existing_edges,
            new_root_id=node_b,
            new_symptom_id=node_a,  # B -> A completes cycle A -> B -> A
        )
    assert "Cyclic causal dependency detected" in str(exc_info.value)


def test_3_node_cycle_rejected():
    """Verify 3-node cycle attempt (A -> B -> C -> A) is strictly rejected (Correction 1)."""
    service = CausalGraphService()
    node_a = uuid.uuid4()
    node_b = uuid.uuid4()
    node_c = uuid.uuid4()

    existing_edges = [
        (node_a, node_b),  # A -> B
        (node_b, node_c),  # B -> C
    ]

    # Attempting C -> A would form cycle A -> B -> C -> A
    with pytest.raises(CyclicCausalDependencyError) as exc_info:
        service.validate_acyclic_addition(
            existing_edges=existing_edges,
            new_root_id=node_c,
            new_symptom_id=node_a,
        )
    assert "Cyclic causal dependency detected" in str(exc_info.value)


def test_valid_dag_branching_and_transitive_downstream_collection():
    """Verify valid acyclic DAG with branching and multi-tier downstream collection."""
    service = CausalGraphService()
    # Topology:
    #       A (Root)
    #      / \
    #     B   C
    #    /
    #   D
    node_a = uuid.uuid4()
    node_b = uuid.uuid4()
    node_c = uuid.uuid4()
    node_d = uuid.uuid4()

    edges: list[tuple[uuid.UUID, uuid.UUID]] = []

    # Add A -> B
    service.validate_acyclic_addition(edges, node_a, node_b)
    edges.append((node_a, node_b))

    # Add A -> C
    service.validate_acyclic_addition(edges, node_a, node_c)
    edges.append((node_a, node_c))

    # Add B -> D
    service.validate_acyclic_addition(edges, node_b, node_d)
    edges.append((node_b, node_d))

    # Downstream symptoms from Root A: B, C, D
    downstream_a = service.find_all_downstream_symptoms(node_a, edges)
    assert len(downstream_a) == 3
    assert set(downstream_a) == {node_b, node_c, node_d}

    # Downstream symptoms from B: D only
    downstream_b = service.find_all_downstream_symptoms(node_b, edges)
    assert set(downstream_b) == {node_d}


def test_root_cause_priority_boost_calculation():
    """Verify root cause priority multiplier scales with downstream blast radius (§A13).

    P_root = min(100.0, P_base * (1.0 + sum(alpha_j * (P_j / 100.0))))
    """
    service = CausalGraphService(coupling_coefficient=0.15)
    root_id = uuid.uuid4()
    child_1 = uuid.uuid4()
    child_2 = uuid.uuid4()

    base_priority = 60.0
    child_priorities = {
        child_1: 80.0,
        child_2: 70.0,
    }

    # scaling_sum = 0.15 * (80/100) + 0.15 * (70/100) = 0.12 + 0.105 = 0.225
    # expected_scaled = 60.0 * (1.0 + 0.225) = 73.5
    res = service.calculate_root_cause_priority(
        root_incident_id=root_id,
        base_priority_score=base_priority,
        child_priority_scores=child_priorities,
    )

    assert res.root_incident_id == root_id
    assert res.downstream_symptom_count == 2
    assert res.base_priority_score == 60.0
    assert abs(res.final_priority_score - 73.5) < 1e-4
    assert abs(res.priority_boost - 13.5) < 1e-4
