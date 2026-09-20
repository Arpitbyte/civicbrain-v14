"""Causal Root-Cause Linking & Incident Graph Centrality Engine (§A13).

Provides:
1. Multi-hop cycle prevention graph traversal (detecting direct and indirect cycles A -> B -> C -> A).
2. Out-degree centrality / downstream blast radius computation.
3. Root-cause priority multiplier calculation:
   P_root = min(100.0, P_base * (1.0 + sum(alpha_j * (P_j / 100.0))))
"""

import uuid
from dataclasses import dataclass

DEFAULT_COUPLING_COEFFICIENT: float = 0.15


class CyclicCausalDependencyError(ValueError):
    """Raised when establishing a causal link would introduce a direct or indirect cycle."""


@dataclass(frozen=True)
class RootCauseBoostResult:
    """Itemized breakdown of root-cause priority boost."""

    root_incident_id: uuid.UUID
    base_priority_score: float
    downstream_symptom_count: int
    downstream_incident_ids: list[uuid.UUID]
    priority_boost: float
    final_priority_score: float


class CausalGraphService:
    """Pure CPU directed graph service managing civic causal topology and acyclicity."""

    def __init__(self, coupling_coefficient: float = DEFAULT_COUPLING_COEFFICIENT) -> None:
        self.coupling_coefficient = coupling_coefficient

    def validate_acyclic_addition(
        self,
        existing_edges: list[tuple[uuid.UUID, uuid.UUID]],
        new_root_id: uuid.UUID,
        new_symptom_id: uuid.UUID,
    ) -> None:
        """Verify adding new_root_id -> new_symptom_id will NOT create any cycles in existing_edges.

        Traverses all nodes reachable downstream from new_symptom_id.
        If new_root_id is reachable from new_symptom_id, adding the edge would complete a cycle!
        """
        if new_root_id == new_symptom_id:
            raise CyclicCausalDependencyError(
                f"Direct self-causation is prohibited: {new_root_id} -> {new_symptom_id}"
            )

        # Build adjacency list
        adj: dict[uuid.UUID, list[uuid.UUID]] = {}
        for root, symptom in existing_edges:
            adj.setdefault(root, []).append(symptom)

        # Check if new_root_id is reachable starting from new_symptom_id
        visited: set[uuid.UUID] = set()
        queue: list[uuid.UUID] = [new_symptom_id]

        while queue:
            curr = queue.pop(0)
            if curr == new_root_id:
                raise CyclicCausalDependencyError(
                    f"Cyclic causal dependency detected: incident {new_root_id} is already "
                    f"a downstream symptom of {new_symptom_id}"
                )
            if curr in visited:
                continue
            visited.add(curr)
            for neighbor in adj.get(curr, []):
                if neighbor not in visited:
                    queue.append(neighbor)

    def find_all_downstream_symptoms(
        self,
        root_id: uuid.UUID,
        edges: list[tuple[uuid.UUID, uuid.UUID]],
    ) -> list[uuid.UUID]:
        """Collect all transitively reachable downstream symptom incidents from a root cause."""
        adj: dict[uuid.UUID, list[uuid.UUID]] = {}
        for r, s in edges:
            adj.setdefault(r, []).append(s)

        visited: set[uuid.UUID] = set()
        queue: list[uuid.UUID] = list(adj.get(root_id, []))

        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)
            for neighbor in adj.get(curr, []):
                if neighbor not in visited:
                    queue.append(neighbor)

        return list(visited)

    def calculate_root_cause_priority(
        self,
        root_incident_id: uuid.UUID,
        base_priority_score: float,
        child_priority_scores: dict[uuid.UUID, float],
    ) -> RootCauseBoostResult:
        """Scale root cause priority proportionally to downstream blast radius (§A13).

        P_root = min(100.0, P_base * (1.0 + sum(alpha_j * (P_j / 100.0))))
        """
        child_ids = list(child_priority_scores.keys())
        symptom_count = len(child_ids)

        if symptom_count == 0:
            return RootCauseBoostResult(
                root_incident_id=root_incident_id,
                base_priority_score=round(base_priority_score, 6),
                downstream_symptom_count=0,
                downstream_incident_ids=[],
                priority_boost=0.0,
                final_priority_score=round(base_priority_score, 6),
            )

        # Multiplier term
        scaling_sum = sum(
            self.coupling_coefficient * (p_j / 100.0) for p_j in child_priority_scores.values()
        )
        scaled_priority = base_priority_score * (1.0 + scaling_sum)
        final_score = min(100.0, scaled_priority)
        boost = max(0.0, final_score - base_priority_score)

        return RootCauseBoostResult(
            root_incident_id=root_incident_id,
            base_priority_score=round(base_priority_score, 6),
            downstream_symptom_count=symptom_count,
            downstream_incident_ids=child_ids,
            priority_boost=round(boost, 6),
            final_priority_score=round(final_score, 6),
        )
