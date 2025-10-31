"""Layout routines for arranging figure nodes into an SVG canvas."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, List, Tuple

from .types import FigurePlan, LayoutResult, PositionedNode


DEFAULT_CANVAS_SIZE = (800.0, 600.0)
NODE_SPACING = (200.0, 140.0)
MARGIN = 60.0


class LayoutError(RuntimeError):
    """Raised when layout generation fails."""


def compute_layout(plan: FigurePlan, *, canvas_size: Tuple[float, float] | None = None) -> LayoutResult:
    """Generate a deterministic layout for the supplied figure plan."""

    width, height = canvas_size or DEFAULT_CANVAS_SIZE
    levels = _assign_layers(plan)
    columns: Dict[int, List[str]] = defaultdict(list)
    for node_id, level in levels.items():
        columns[level].append(node_id)

    sorted_levels = sorted(columns)
    nodes: List[PositionedNode] = []
    node_lookup = plan.node_map()
    for level_index, level in enumerate(sorted_levels):
        column = columns[level]
        column.sort()
        x = MARGIN + level_index * NODE_SPACING[0]
        col_height = NODE_SPACING[1] * max(1, len(column) - 1)
        y_offset = max(MARGIN, (height - col_height) / 2)
        for row_index, node_id in enumerate(column):
            y = y_offset + row_index * NODE_SPACING[1]
            node = node_lookup[node_id]
            nodes.append(
                PositionedNode(
                    identifier=node.identifier,
                    label=node.label,
                    node_type=node.node_type,
                    metadata=dict(node.metadata),
                    x=x,
                    y=y,
                )
            )

    return LayoutResult(width=width, height=height, nodes=nodes, edges=plan.edges)


def _assign_layers(plan: FigurePlan) -> Dict[str, int]:
    incoming: Dict[str, List[str]] = defaultdict(list)
    outgoing: Dict[str, List[str]] = defaultdict(list)
    for edge in plan.edges:
        incoming[edge.target].append(edge.source)
        outgoing[edge.source].append(edge.target)

    levels: Dict[str, int] = {}
    queue = deque()
    for node in plan.nodes:
        if node.identifier not in incoming:
            levels[node.identifier] = 0
            queue.append(node.identifier)

    if not queue:
        # Fall back to arbitrary starting point when the graph is cyclic.
        queue.append(plan.nodes[0].identifier)
        levels[plan.nodes[0].identifier] = 0

    while queue:
        current = queue.popleft()
        current_level = levels[current]
        for neighbor in outgoing.get(current, []):
            proposed = current_level + 1
            if neighbor not in levels or proposed > levels[neighbor]:
                levels[neighbor] = proposed
                queue.append(neighbor)

    # Some nodes might be isolated; assign them to level zero.
    for node in plan.nodes:
        levels.setdefault(node.identifier, 0)

    return levels
