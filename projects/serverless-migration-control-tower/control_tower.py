"""Read-only rules-based assessment for synthetic Databricks job inventories.
Never changes a job, executes a notebook, or initiates cutover.
"""
import argparse
import json
from pathlib import Path

RISK_WEIGHT = {"init_scripts": 25, "legacy_mounts": 25, "spark_configs": 15,
               "environment_variables": 10, "many_tasks": 15, "scheduled": 10}


def assess(job: dict) -> dict:
    reasons = []
    if job.get("init_scripts"): reasons.append("init_scripts")
    if job.get("legacy_mounts"): reasons.append("legacy_mounts")
    if job.get("spark_configs"): reasons.append("spark_configs")
    if job.get("environment_variables"): reasons.append("environment_variables")
    if len(job.get("tasks", [])) > 10: reasons.append("many_tasks")
    if job.get("scheduled"): reasons.append("scheduled")
    score = min(100, sum(RISK_WEIGHT[r] for r in reasons))
    return {"id": job.get("id"), "name": job.get("name", "unnamed"),
            "readiness_score": 100 - score, "risk": "HIGH" if score >= 50 else "MEDIUM" if score >= 20 else "LOW",
            "blockers": reasons, "promotion_permitted": False}


def report(inventory: dict) -> dict:
    jobs = [assess(j) for j in inventory.get("jobs", [])]
    summary = {"total_jobs": len(jobs), "high_risk": sum(j["risk"] == "HIGH" for j in jobs),
               "medium_risk": sum(j["risk"] == "MEDIUM" for j in jobs),
               "low_risk": sum(j["risk"] == "LOW" for j in jobs)}
    return {"mode": "READ_ONLY_DEMO", "summary": summary, "jobs": jobs}


def main():
    p = argparse.ArgumentParser(description="Analyze a local JSON inventory without touching Databricks")
    p.add_argument("inventory", type=Path)
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    result = report(json.loads(args.inventory.read_text(encoding="utf-8")))
    rendered = json.dumps(result, indent=2)
    if args.out: args.out.write_text(rendered + "\n", encoding="utf-8")
    else: print(rendered)

if __name__ == "__main__": main()
