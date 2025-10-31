"""Command-line interface for generating SVG diagrams from text specs."""

from __future__ import annotations

import argparse
from pathlib import Path

from .agent import FigureAgent, FigureAgentConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate SVG diagrams from textual specs.")
    parser.add_argument("spec", type=Path, help="Path to a markdown/DSL description of the figure")
    parser.add_argument("--out", type=Path, help="Output SVG file path", default=Path("figure.svg"))
    parser.add_argument("--width", type=float, default=960.0, help="Canvas width in pixels")
    parser.add_argument("--height", type=float, default=640.0, help="Canvas height in pixels")
    return parser


def main(args: list[str] | None = None) -> int:
    parser = build_parser()
    namespace = parser.parse_args(args=args)

    config = FigureAgentConfig(canvas_width=namespace.width, canvas_height=namespace.height)
    agent = FigureAgent(config=config)

    spec_text = namespace.spec.read_text(encoding="utf-8")
    svg = agent.generate(spec_text)
    namespace.out.write_text(svg, encoding="utf-8")
    print(f"Saved SVG to {namespace.out}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
