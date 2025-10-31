"""High-level orchestrator for SVG figure generation."""

from __future__ import annotations

from dataclasses import dataclass

from .layout_figure import compute_layout
from .parse_figure import ParseConfig, parse_figure_spec
from .render_svg import render_svg
from .types import FigurePlan, LayoutResult


@dataclass
class FigureAgentConfig:
    """Configuration options for the SVG figure agent."""

    canvas_width: float = 960.0
    canvas_height: float = 640.0
    default_node_type: str = "process"


class FigureAgent:
    """Compose parsing, layout, and rendering into a single entry point."""

    def __init__(self, config: FigureAgentConfig | None = None) -> None:
        self.config = config or FigureAgentConfig()

    def parse(self, spec: str) -> FigurePlan:
        """Parse the textual figure specification."""

        return parse_figure_spec(spec, config=ParseConfig(default_node_type=self.config.default_node_type))

    def layout(self, plan: FigurePlan) -> LayoutResult:
        """Compute spatial positions for figure nodes."""

        return compute_layout(plan, canvas_size=(self.config.canvas_width, self.config.canvas_height))

    def render(self, layout: LayoutResult) -> str:
        """Render the layout to SVG."""

        return render_svg(layout)

    def generate(self, spec: str) -> str:
        """Run the full pipeline returning SVG markup."""

        plan = self.parse(spec)
        layout = self.layout(plan)
        return self.render(layout)
