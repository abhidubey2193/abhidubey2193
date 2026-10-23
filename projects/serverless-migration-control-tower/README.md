# Serverless Migration Control Tower — Public Demo

**Status:** Early, standalone, **read-only rules-based portfolio demo**. No customer datasets or workspace exports. This is not the complete original workspace-scanning prototype, a Databricks deployment, or a bulk migration agent.

## Current demo
- Load a local **synthetic** JSON list of Databricks-style jobs
- Generate per-job readiness scores, blocker categories and risk counts
- Flag init scripts, DBFS mounts, custom Spark configs, environment variables, tasks over 10 and scheduled jobs
- **Never** perform workload execution, mutation, migration, promotion or cutover

## Run
```bash
cd projects/serverless-migration-control-tower
python control_tower.py sample_inventory.json
python -m unittest discover -p 'test_*.py' -v
```

## Proposed full architecture
Read-only Databricks SDK inventory → rules assessment → Unity Catalog-backed review state → approval workflow → safe cloned jobs → A/B validation → controlled cutover and rollback.

Not implemented here: API discovery, SQL/Delta persistence, notebook source scans, clone-and-promote, cost validation, A/B execution, and production deployment. This demo deliberately excludes identifying metadata, credentials, employer-specific documents and any proprietary source code.
