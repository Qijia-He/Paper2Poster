"""Shared dataclasses used across the SVG figure generation pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional


@dataclass
class FigureNode:
    """Represents a single diagram element."""

    identifier: str
    label: str
    node_type: str = "process"
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class FigureEdge:
    """Represents a directed relationship between two nodes."""

    source: str
    target: str
    label: Optional[str] = None


@dataclass
class FigurePlan:
    """Structured view of the extracted figure semantics."""

    nodes: List[FigureNode]
    edges: List[FigureEdge]
    title: Optional[str] = None
    description: Optional[str] = None

    def node_map(self) -> Dict[str, FigureNode]:
        return {node.identifier: node for node in self.nodes}


@dataclass
class PositionedNode(FigureNode):
    """Extends :class:`FigureNode` with positional layout information."""

    x: float = 0.0
    y: float = 0.0


@dataclass
class LayoutResult:
    """Represents the outcome of the layout algorithm."""

    width: float
    height: float
    nodes: List[PositionedNode]
    edges: List[FigureEdge]

    def iter_nodes(self) -> Iterable[PositionedNode]:
        return iter(self.nodes)

    def iter_edges(self) -> Iterable[FigureEdge]:
        return iter(self.edges)
