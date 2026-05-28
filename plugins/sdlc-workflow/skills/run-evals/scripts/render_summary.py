#!/usr/bin/env python3
"""Render eval results and optional baseline comparison as Markdown."""

import argparse
import json
import sys
from pathlib import Path


def load_grading_files(results_dir: Path) -> list[dict]:
    """Load all eval-N/grading.json files, sorted by eval ID."""
    gradings = []
    for eval_dir in sorted(results_dir.glob("eval-*")):
        grading_path = eval_dir / "grading.json"
        if not grading_path.exists():
            continue
        grading = json.loads(grading_path.read_text())
        grading["_eval_id"] = eval_dir.name
        gradings.append(grading)
    return gradings


def render(results_dir: Path, baseline_dir: Path | None, skill: str | None = None) -> str:
    gradings = load_grading_files(results_dir)

    if not gradings:
        return "> No eval results found.\n"

    heading = f"## Eval Results: {skill}" if skill else "## Eval Results"
    lines = [heading, ""]

    # Per-eval table
    lines.append("| Eval | Passed | Failed | Pass Rate |")
    lines.append("|------|--------|--------|-----------|")

    for g in gradings:
        eval_id = g["_eval_id"]
        s = g.get("summary", {})
        passed = s.get("passed", 0)
        failed = s.get("failed", 0)
        total = s.get("total", 0)
        rate = s.get("pass_rate", 0)
        lines.append(
            f"| {eval_id} | {passed}/{total} | {failed} | {rate * 100:.0f}% |"
        )

    lines.append("")

    # Failed assertion evidence
    has_failures = any(g.get("summary", {}).get("failed", 0) > 0 for g in gradings)
    if has_failures:
        lines.append("### Failed Assertions")
        lines.append("")
        for g in gradings:
            s = g.get("summary", {})
            if s.get("failed", 0) == 0:
                continue
            eval_id = g["_eval_id"]
            failed = [
                a for a in g.get("assertion_results", []) if not a.get("passed", True)
            ]
            count = len(failed)
            label = "assertion" if count == 1 else "assertions"
            lines.append("<details>")
            lines.append(f"<summary>{eval_id}: {count} failing {label}</summary>")
            lines.append("")
            for a in failed:
                lines.append(f'- **Assertion:** "{a.get("text", "")}"')
                lines.append(f'  **Evidence:** "{a.get("evidence", "")}"')
                lines.append("")
            lines.append("</details>")
            lines.append("")

    # Aggregate from benchmark.json if present
    benchmark_path = results_dir / "benchmark.json"
    if benchmark_path.exists():
        benchmark = json.loads(benchmark_path.read_text())
        rs = benchmark.get("run_summary", {})
        pr_mean = rs.get("pass_rate", {}).get("mean")
        tokens_mean = rs.get("tokens", {}).get("mean")
        time_mean = rs.get("time_seconds", {}).get("mean")

        parts = []
        if pr_mean is not None:
            parts.append(f"**Pass rate:** {pr_mean * 100:.0f}%")
        if tokens_mean is not None:
            parts.append(f"**Tokens:** {int(tokens_mean):,}")
        if time_mean is not None:
            parts.append(f"**Duration:** {time_mean:.0f}s")
        if parts:
            lines.append(" · ".join(parts))
            lines.append("")

    # Baseline comparison
    if baseline_dir and baseline_dir.exists():
        baseline_benchmark = baseline_dir / "benchmark.json"
        if baseline_benchmark.exists():
            baseline = json.loads(baseline_benchmark.read_text())
            brs = baseline.get("run_summary", {})
            b_pr = brs.get("pass_rate", {}).get("mean")
            b_tokens = brs.get("tokens", {}).get("mean")
            b_time = brs.get("time_seconds", {}).get("mean")

            baseline_label = baseline_dir.name
            if baseline_dir.is_symlink():
                baseline_label = baseline_dir.resolve().name

            parts = []
            if b_pr is not None:
                parts.append(f"{b_pr * 100:.0f}%")
            if b_tokens is not None:
                parts.append(f"{int(b_tokens):,} tokens")
            if b_time is not None:
                parts.append(f"{b_time:.0f}s")
            if parts:
                lines.append(
                    f"**Baseline** (`{baseline_label}`): " + " · ".join(parts)
                )
                lines.append("")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Render eval results as Markdown"
    )
    parser.add_argument(
        "--results", type=Path, required=True, help="Workspace with eval results"
    )
    parser.add_argument(
        "--baseline", type=Path, default=None, help="Baseline directory"
    )
    parser.add_argument(
        "--skill",
        type=str,
        default=None,
        help="Skill name to include in the heading",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output file (default: <results>/summary.md)",
    )
    args = parser.parse_args()

    if not args.results.exists():
        print(f"Results directory not found: {args.results}", file=sys.stderr)
        sys.exit(1)

    baseline = args.baseline
    if baseline and not baseline.exists():
        print(f"Warning: baseline not found: {baseline}", file=sys.stderr)
        baseline = None

    md = render(args.results, baseline, args.skill)

    output_path = args.output or (args.results / "summary.md")
    output_path.write_text(md)
    print(md)


if __name__ == "__main__":
    main()
