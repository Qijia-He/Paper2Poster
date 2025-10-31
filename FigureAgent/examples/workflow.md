# Scientific Workflow

## Description
High-level depiction of the experiment pipeline for a CSE research project.

## Nodes
- ingest | Data Ingest | io
- preprocess | Pre-process Data | process
- train | Train Model | process
- evaluate | Evaluate Metrics | decision
- deploy | Deployment | process

## Edges
- ingest -> preprocess
- preprocess -> train
- train -> evaluate | validation report
- evaluate -> deploy | go/no-go
