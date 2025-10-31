"""Utilities for parsing diagram specifications into structured plans."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List

from .types import FigureEdge, FigureNode, FigurePlan


@dataclass
class ParseConfig:
    """Configuration controlling how textual specs are interpreted."""

    default_node_type: str = "process"


NODE_PATTERN = re.compile(r"^[-*]\s*(?P<id>[\w-]+)\s*\|\s*(?P<label>[^|]+?)(?:\s*\|\s*(?P<type>[^|]+))?\s*$")
EDGE_PATTERN = re.compile(
    r"^[-*]\s*(?P<src>[\w-]+)\s*->\s*(?P<tgt>[\w-]+)(?:\s*\|\s*(?P<label>.+))?\s*$"
)


def _parse_node_line(line: str, config: ParseConfig) -> FigureNode:
    match = NODE_PATTERN.match(line)
    if not match:
        raise ValueError(f"Invalid node line: {line!r}")
    node_type = match.group("type") or config.default_node_type
    return FigureNode(
        identifier=match.group("id"),
        label=match.group("label").strip(),
        node_type=node_type.strip(),
    )


def _parse_edge_line(line: str) -> FigureEdge:
    match = EDGE_PATTERN.match(line)
    if not match:
        raise ValueError(f"Invalid edge line: {line!r}")
    label = match.group("label")
    return FigureEdge(
        source=match.group("src"),
        target=match.group("tgt"),
        label=label.strip() if label else None,
    )


def parse_figure_spec(text: str, *, config: ParseConfig | None = None) -> FigurePlan:
    """Parse a lightweight DSL into a :class:`FigurePlan`.

    The DSL intentionally mirrors the data that :mod:`PosterAgent.parse_raw`
    produces: named sections separated by markdown headings. We reuse the
    familiar bullet-list format so diagram specs can be embedded inside a
    README or prompt without additional tooling.

    Example::

        # Title
        Scientific Workflow

        ## Nodes
        - ingest | Data Ingest | io
        - process | Model Training
        - evaluate | Evaluation | decision

        ## Edges
        - ingest -> process
        - process -> evaluate | accuracy report

    Returns
    -------
    FigurePlan
        Structured nodes and edges extracted from the text.
    """

    config = config or ParseConfig()
    sections = _split_sections(text)

    title = sections.get("title", "").strip() or None
    description = sections.get("description", "").strip() or None

    nodes_section = sections.get("nodes")
    if not nodes_section:
        raise ValueError("A figure specification must include a 'Nodes' section.")

    edges_section = sections.get("edges", "")

    nodes = _parse_lines(nodes_section.splitlines(), lambda line: _parse_node_line(line, config))
    edges = _parse_lines(edges_section.splitlines(), _parse_edge_line)

    return FigurePlan(nodes=nodes, edges=edges, title=title, description=description)


def _split_sections(text: str) -> dict[str, str]:
    current = "body"
    sections: dict[str, List[str]] = {current: []}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections.setdefault(current, [])
            continue
        if line.startswith("# "):
            current = "title"
            sections.setdefault(current, [])
            sections[current] = [line[2:].strip()]
            continue
        sections.setdefault(current, []).append(raw_line)

    if "description" not in sections:
        body = sections.get("body", [])
        sections["description"] = body
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def _parse_lines(lines: Iterable[str], parser) -> List:
    results: List = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        results.append(parser(stripped))
    return results
