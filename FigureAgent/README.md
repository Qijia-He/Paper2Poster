# FigureAgent Quickstart

## Workflow Overview
The FigureAgent package mirrors the main PosterAgent pipeline but focuses on turning a structured text specification into an SVG diagram. The typical flow is:

1. **Parse** the markdown description into semantic figure elements.
2. **Layout** the elements into layers, rows, and connectors.
3. **Generate content** strings (labels, annotations) from the parsed data.
4. **Render** the computed layout as a stylized SVG file.

Each stage is implemented in the corresponding module under `FigureAgent/` (`parse_figure.py`, `layout_figure.py`, `gen_svg_content.py`, `render_svg.py`) and orchestrated by `new_pipeline.py`.

## Running the CLI
Run the end-to-end pipeline with:

```bash
python -m FigureAgent.new_pipeline <path_to_spec_markdown> --out <output_svg_path>
```

Example using the bundled specification:

```bash
python -m FigureAgent.new_pipeline FigureAgent/examples/workflow.md --out FigureAgent/examples/workflow.svg
```

The command reads the markdown specification, generates an SVG, and saves it to the provided path.

## Understanding "Create PR", "Copy git apply", and "Copy patch"
These terms usually appear in code review tools such as GitHub when reviewing pull requests (PRs):

- **Create PR**: Opens a pull request from your current branch, allowing collaborators to review the proposed changes before merging them into the main branch.
- **Copy git apply**: Copies a `git apply` command that reproduces a suggested change. You can paste it into a terminal to apply that change directly to your working tree.
- **Copy patch**: Copies the raw patch diff for a suggestion so you can save it or apply it manually (for example with `git apply` or `git am`).

These options streamline incorporating reviewers' suggestions during the PR process.

