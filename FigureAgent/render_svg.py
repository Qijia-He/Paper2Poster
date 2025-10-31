"""SVG rendering utilities for the figure agent."""

from __future__ import annotations

from typing import Dict

from .gen_svg_content import ShapeStyle, build_svg_elements
from .types import LayoutResult


ARROW_MARKER = """
<defs>
  <marker id='arrow' markerWidth='10' markerHeight='7' refX='10' refY='3.5' orient='auto' markerUnits='strokeWidth'>
    <path d='M0,0 L0,7 L10,3.5 z' fill='#334155'/>
  </marker>
</defs>
""".strip()


def render_svg(layout: LayoutResult, *, styles: Dict[str, ShapeStyle] | None = None) -> str:
    """Materialize the layout as an SVG document string."""

    elements = build_svg_elements(layout, styles=styles)
    body = "\n  ".join(elements)
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{layout.width}' height='{layout.height}' viewBox='0 0 {layout.width} {layout.height}'>\n"
        f"  {ARROW_MARKER}\n"
        f"  {body}\n"
        "</svg>"
    )
