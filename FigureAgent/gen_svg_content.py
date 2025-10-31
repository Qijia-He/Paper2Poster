"""Content helpers that convert layouts into renderable SVG components."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence

from .types import LayoutResult, PositionedNode


@dataclass
class ShapeStyle:
    """Styling primitives shared between nodes."""

    fill: str
    stroke: str
    stroke_width: float = 2.0
    text_color: str = "#0f172a"


DEFAULT_STYLES: Dict[str, ShapeStyle] = {
    "process": ShapeStyle(fill="#e0f2fe", stroke="#0284c7"),
    "io": ShapeStyle(fill="#ede9fe", stroke="#7c3aed"),
    "decision": ShapeStyle(fill="#fef3c7", stroke="#f59e0b"),
}

NODE_SIZE = (160, 60)


def build_svg_elements(layout: LayoutResult, *, styles: Dict[str, ShapeStyle] | None = None) -> List[str]:
    """Return a list of raw SVG element strings for nodes and edges."""

    style_map = {**DEFAULT_STYLES, **(styles or {})}
    elements: List[str] = []

    for node in layout.iter_nodes():
        style = style_map.get(node.node_type, style_map["process"])
        elements.append(_node_rect(node, style))
        elements.append(_node_label(node, style))

    for edge in layout.iter_edges():
        elements.append(_edge_line(layout, edge))
    return elements


def _node_rect(node: PositionedNode, style: ShapeStyle) -> str:
    width, height = NODE_SIZE
    attrs = {
        "x": f"{node.x - width / 2:.2f}",
        "y": f"{node.y - height / 2:.2f}",
        "width": f"{width:.2f}",
        "height": f"{height:.2f}",
        "rx": "12",
        "ry": "12",
        "fill": style.fill,
        "stroke": style.stroke,
        "stroke-width": f"{style.stroke_width}",
    }
    return _serialize("rect", attrs)


def _node_label(node: PositionedNode, style: ShapeStyle) -> str:
    attrs = {
        "x": f"{node.x:.2f}",
        "y": f"{node.y:.2f}",
        "fill": style.text_color,
        "font-family": "Inter, Helvetica, Arial, sans-serif",
        "font-size": "16px",
        "text-anchor": "middle",
        "dominant-baseline": "middle",
    }
    lines = _wrap_label(node.label)
    if len(lines) == 1:
        return _serialize("text", attrs, text=lines[0], self_closing=False)
    tspans = []
    for idx, line in enumerate(lines):
        t_attrs = {"x": attrs["x"], "dy": "0" if idx == 0 else "1.2em"}
        tspans.append(_serialize("tspan", t_attrs, text=line, self_closing=False))
    return _serialize("text", attrs, children=tspans, self_closing=False)


def _wrap_label(label: str, *, max_len: int = 22) -> List[str]:
    words = label.split()
    if not words:
        return [""]
    lines: List[str] = []
    current: List[str] = []
    for word in words:
        tentative = " ".join(current + [word])
        if len(tentative) <= max_len:
            current.append(word)
            continue
        if current:
            lines.append(" ".join(current))
            current = [word]
        else:
            lines.append(word)
            current = []
    if current:
        lines.append(" ".join(current))
    return lines


def _edge_line(layout: LayoutResult, edge) -> str:
    source = next(node for node in layout.nodes if node.identifier == edge.source)
    target = next(node for node in layout.nodes if node.identifier == edge.target)
    attrs = {
        "x1": f"{source.x:.2f}",
        "y1": f"{source.y:.2f}",
        "x2": f"{target.x:.2f}",
        "y2": f"{target.y:.2f}",
        "stroke": "#334155",
        "stroke-width": "2",
        "marker-end": "url(#arrow)",
    }
    if edge.label:
        attrs["data-label"] = edge.label
    return _serialize("line", attrs)


def _serialize(
    tag: str,
    attrs: Dict[str, str],
    *,
    text: str | None = None,
    children: Sequence[str] | None = None,
    self_closing: bool | None = None,
) -> str:
    attr_str = " ".join(f"{key}='{value}'" for key, value in attrs.items())
    suffix = f" {attr_str}" if attr_str else ""
    if self_closing is None:
        self_closing = text is None and not children
    if self_closing:
        return f"<{tag}{suffix}/>"
    inner = text or ""
    if children:
        inner += "".join(children)
    return f"<{tag}{suffix}>{inner}</{tag}>"
