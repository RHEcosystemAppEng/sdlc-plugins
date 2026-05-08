#!/usr/bin/env python3
"""Generate performance baseline reports from JSON measurement data.

Reads JSON output from capture-baseline.template.mjs (frontend/Playwright) and/or
perf-benchmark.sh (backend/curl), populates the baseline-report template, generates
waterfall ASCII charts, and optionally compares against a previous baseline.

Uses only Python stdlib — no external dependencies required.

Usage:
    python3 perf-baseline-report.py \\
        --frontend-json baselines/frontend.json \\
        --backend-json baselines/benchmark-results.json \\
        --config .claude/performance-config.json \\
        --template skills/performance/baseline-report.template.md \\
        --output baselines/baseline-report.md \\
        --previous baselines/baseline-report.md
"""

import argparse
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def fmt_ms(val: Any) -> str:
    """Format a millisecond value for display."""
    if val is None:
        return "-"
    try:
        v = float(val)
        if v == int(v):
            return str(int(v))
        return f"{v:.1f}"
    except (TypeError, ValueError):
        return str(val)


# --- Waterfall chart generation ---


def generate_waterfall(resources: List[Dict], scenario_name: str, max_width: int = 60) -> str:
    """Generate an ASCII waterfall chart for resource loading timeline.

    Args:
        resources: List of {name, type, duration, startTime, transferSize} dicts
        scenario_name: Name for the chart heading
        max_width: Character width of the timeline bar area
    """
    if not resources:
        return f"### Waterfall -- {scenario_name}\n\nNo resource timing data available.\n"

    sorted_res = sorted(resources, key=lambda r: float(r.get("startTime", 0)))
    top_resources = sorted_res[:15]

    if not top_resources:
        return f"### Waterfall -- {scenario_name}\n\nNo resource timing data available.\n"

    max_end = max(
        float(r.get("startTime", 0)) + float(r.get("duration", 0))
        for r in top_resources
    )
    if max_end <= 0:
        max_end = 1

    type_chars = {
        "script": "=",
        "stylesheet": "-",
        "image": "*",
        "fetch": "+",
        "xmlhttprequest": "+",
        "other": ".",
    }

    max_name_len = 25
    lines = []
    lines.append(f"### Waterfall -- {scenario_name}")
    lines.append("")

    scale_points = [0]
    step = max_end / 3
    for i in range(1, 4):
        scale_points.append(step * i)
    header_labels = "".join(f"{int(p)}ms".ljust(max_width // 3) for p in scale_points[:3])
    header_labels += f"{int(scale_points[3])}ms"
    lines.append(f"{'':>{max_name_len}}  {header_labels}")
    lines.append(f"{'':>{max_name_len}}  {'|' + '-' * (max_width // 3 - 1)}" * 3 + "|")

    for r in top_resources:
        name = r.get("name", "unknown")
        if len(name) > max_name_len:
            name = "..." + name[-(max_name_len - 3):]

        res_type = r.get("type", "other").lower()
        char = type_chars.get(res_type, ".")
        start = float(r.get("startTime", 0))
        duration = float(r.get("duration", 0))

        start_col = int((start / max_end) * max_width)
        dur_cols = max(1, int((duration / max_end) * max_width))
        end_col = min(start_col + dur_cols, max_width)

        bar = " " * start_col + "[" + char * max(0, end_col - start_col - 2) + "]"
        bar = bar.ljust(max_width)
        dur_label = f"({int(duration)}ms)"

        lines.append(f"{name:>{max_name_len}}  {bar} {dur_label}")

    lines.append("")
    lines.append("**Legend:** `[====]` Script  `[----]` Stylesheet  `[****]` Image  `[++++]` Fetch/XHR")
    lines.append("")
    return "\n".join(lines)


# --- Comparison section ---


def generate_comparison(current_metrics: Dict, previous_metrics: Dict) -> str:
    """Generate a comparison table between current and previous baseline."""
    if not previous_metrics:
        return "_This is the initial baseline. Future re-baselines will show comparison here._"

    lines = []
    lines.append("| Metric | Old p95 | New p95 | Delta | Change |")
    lines.append("|--------|---------|---------|-------|--------|")

    metric_names = [
        ("LCP", "lcp"),
        ("FCP", "fcp"),
        ("DOM Interactive", "domInteractive"),
        ("Total Load Time", "totalLoadTime"),
    ]

    for display_name, key in metric_names:
        old_val = previous_metrics.get(key, {}).get("p95")
        new_val = current_metrics.get(key, {}).get("p95")
        if old_val is None or new_val is None:
            continue

        old_f = float(old_val)
        new_f = float(new_val)
        delta = new_f - old_f
        if old_f > 0:
            pct = (delta / old_f) * 100
        else:
            pct = 0

        direction = "+" if delta >= 0 else ""
        emoji = "regressed" if delta > 0 else "improved"
        lines.append(
            f"| {display_name} | {fmt_ms(old_val)}ms | {fmt_ms(new_val)}ms "
            f"| {direction}{fmt_ms(delta)}ms | {direction}{pct:.1f}% ({emoji}) |"
        )

    return "\n".join(lines) if len(lines) > 2 else "_No comparable metrics found in previous baseline._"


# --- Per-scenario section ---


def generate_scenario_section(scenario: Dict) -> str:
    """Generate a per-scenario metrics section."""
    name = scenario.get("name", "Unknown")
    url = scenario.get("url", scenario.get("path", "-"))
    metrics = scenario.get("metrics", {})

    lines = []
    lines.append(f"### Scenario: {name}")
    lines.append(f"")
    lines.append(f"**URL:** `{url}`")
    lines.append("")

    has_frontend = any(k in metrics for k in ("lcp", "fcp", "domInteractive", "totalLoadTime"))
    if has_frontend:
        lines.append("| Metric | Mean | p50 | p95 | p99 | Unit |")
        lines.append("|---|---|---|---|---|---|")
        for metric_key, metric_name in [
            ("lcp", "LCP"),
            ("fcp", "FCP"),
            ("domInteractive", "DOM Interactive"),
            ("totalLoadTime", "Total Load Time"),
        ]:
            m = metrics.get(metric_key, {})
            if m:
                lines.append(
                    f"| {metric_name} | {fmt_ms(m.get('mean'))} "
                    f"| {fmt_ms(m.get('p50'))} | {fmt_ms(m.get('p95'))} "
                    f"| {fmt_ms(m.get('p99'))} | ms |"
                )

    resources = scenario.get("resources", {})
    if resources:
        lines.append("")
        lines.append("**Resources loaded:**")
        for res_type in ("scripts", "stylesheets", "images", "fetch"):
            res = resources.get(res_type, {})
            count = res.get("count", 0)
            if count > 0:
                lines.append(f"- {res_type.capitalize()}: {count}")

    lines.append("")
    return "\n".join(lines)


def generate_backend_scenario_section(endpoint_path: str, data: Dict) -> str:
    """Generate a per-endpoint metrics section for backend."""
    lines = []
    lines.append(f"### Endpoint: {endpoint_path}")
    lines.append("")
    lines.append(f"**Test URL:** `{data.get('test_url', endpoint_path)}`")
    lines.append("")
    lines.append("| Metric | Value | Unit |")
    lines.append("|---|---|---|")
    lines.append(f"| p50 (Median) | {fmt_ms(data.get('p50_ms'))} | ms |")
    lines.append(f"| p95 | {fmt_ms(data.get('p95_ms'))} | ms |")
    lines.append(f"| p99 | {fmt_ms(data.get('p99_ms'))} | ms |")
    lines.append(f"| Mean | {fmt_ms(data.get('mean_ms'))} | ms |")
    lines.append("")
    lines.append(f"**Cache:** First request {fmt_ms(data.get('first_request_ms'))}ms "
                 f"-> warm mean {fmt_ms(data.get('subsequent_mean_ms'))}ms "
                 f"({data.get('cache_improvement_pct', '0')}% improvement, "
                 f"{data.get('cache_status', 'N/A')})")
    lines.append("")
    return "\n".join(lines)


# --- Resource timing table ---


def generate_resource_table(scenarios: List[Dict], limit: int = 10) -> str:
    """Extract top resources by duration across all scenarios."""
    all_resources = []
    for s in scenarios:
        scenario_name = s.get("name", "unknown")
        for res_type_key in ("scripts", "stylesheets", "images", "fetch"):
            items = s.get("resources", {}).get(res_type_key, {}).get("items", [])
            for item in items:
                all_resources.append({
                    "name": item.get("name", item.get("url", "unknown")),
                    "type": res_type_key.rstrip("s"),
                    "duration": float(item.get("duration", 0)),
                    "size": float(item.get("transferSize", 0)) / 1024,
                    "scenario": scenario_name,
                    "startTime": float(item.get("startTime", 0)),
                })

    sorted_res = sorted(all_resources, key=lambda r: r["duration"], reverse=True)
    top = sorted_res[:limit]

    if not top:
        return "No resource timing data available."

    lines = []
    lines.append("| Resource | Type | Duration (ms) | Size (KB) | Scenario |")
    lines.append("|---|---|---|---|---|")
    for r in top:
        name = r["name"]
        if "?" in name:
            name = name.split("?")[0]
        if len(name) > 60:
            name = "..." + name[-57:]
        lines.append(
            f"| {name} | {r['type']} | {int(r['duration'])} "
            f"| {r['size']:.1f} | {r['scenario']} |"
        )
    return "\n".join(lines)


# --- Extract previous baseline metrics ---


def parse_previous_baseline(path: str) -> Optional[Dict]:
    """Parse aggregate metrics from a previous baseline report (markdown)."""
    try:
        with open(path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        return None

    metrics = {}
    metric_patterns = {
        "lcp": r"\*\*LCP\*\*.*?\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|",
        "fcp": r"\*\*FCP\*\*.*?\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|",
        "domInteractive": r"\*\*DOM Interactive\*\*.*?\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|",
        "totalLoadTime": r"\*\*Total Load Time\*\*.*?\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|",
    }

    for key, pattern in metric_patterns.items():
        match = re.search(pattern, content)
        if match:
            try:
                metrics[key] = {
                    "mean": float(match.group(1).strip()),
                    "p50": float(match.group(2).strip()),
                    "p95": float(match.group(3).strip()),
                    "p99": float(match.group(4).strip()),
                }
            except (ValueError, IndexError):
                pass

    return metrics if metrics else None


# --- Main report generation ---


def generate_report(
    frontend_data: Optional[Dict],
    backend_data: Optional[Dict],
    config: Dict,
    previous_metrics: Optional[Dict],
) -> str:
    """Assemble the complete baseline report."""

    ts = now_iso()
    date = now_date()
    repo_name = config.get("repositories", {}).get("frontend", {}).get("name") or \
                config.get("repositories", {}).get("backend", {}).get("name") or "unknown"
    metric_type = config.get("metadata", {}).get("metric_type", "frontend")
    iterations = config.get("baseline_settings", {}).get("iterations", 20)
    warmup = config.get("baseline_settings", {}).get("warmup_runs", 2)

    capture_mode = "cold-start"
    if metric_type == "backend":
        capture_mode = "api-benchmark"
    elif metric_type == "hybrid":
        capture_mode = "hybrid"

    sections = []

    # --- Frontmatter ---
    sections.append(f"""---
generated_by: perf-baseline-report.py
timestamp: {ts}
repository: {repo_name}
capture_mode: {capture_mode}
---""")

    # --- Header ---
    scenario_count = 0
    if frontend_data:
        scenario_count += len(frontend_data.get("scenarios", []))
    if backend_data:
        scenario_count += len(backend_data.get("endpoints", {}))

    sections.append(f"""
# Performance Baseline Report

## Configuration Summary

- **Capture Date:** {date}
- **Iterations:** {iterations}
- **Warmup Runs:** {warmup}
- **Scenarios Measured:** {scenario_count}

## Capture Mode

**Mode:** {capture_mode}

{"Direct URL navigation with cold cache. Measures worst-case/first-visit performance." if "cold" in capture_mode else ""}
{"API endpoint benchmarking via HTTP load testing." if "api" in capture_mode or "benchmark" in capture_mode else ""}
{"Combined frontend browser metrics and backend API benchmarking." if capture_mode == "hybrid" else ""}
""")

    # --- Aggregate metrics ---
    sections.append("---\n\n## Aggregate Metrics\n")

    if frontend_data and metric_type in ("frontend", "hybrid"):
        agg = frontend_data.get("aggregate", {})
        sections.append("**Frontend Performance Metrics:**\n")
        sections.append("| Metric | Mean | p50 (Median) | p95 | p99 | Unit |")
        sections.append("|---|---|---|---|---|---|")
        for key, name in [("lcp", "LCP"), ("fcp", "FCP"),
                          ("domInteractive", "DOM Interactive"),
                          ("totalLoadTime", "Total Load Time")]:
            m = agg.get(key, {})
            sections.append(
                f"| **{name}** | {fmt_ms(m.get('mean'))} | {fmt_ms(m.get('p50'))} "
                f"| {fmt_ms(m.get('p95'))} | {fmt_ms(m.get('p99'))} | ms |"
            )
        sections.append("")

    if backend_data and metric_type in ("backend", "hybrid"):
        agg = backend_data.get("aggregate", {})
        sections.append("**Backend API Performance Metrics:**\n")
        sections.append("| Metric | Mean | p50 (Median) | p95 | p99 | Unit |")
        sections.append("|---|---|---|---|---|---|")
        sections.append(
            f"| **Response Time** | {fmt_ms(agg.get('mean_ms'))} | {fmt_ms(agg.get('p50_ms'))} "
            f"| {fmt_ms(agg.get('p95_ms'))} | {fmt_ms(agg.get('p99_ms'))} | ms |"
        )
        sections.append("")

    # --- Per-scenario sections ---
    sections.append("## Per-Scenario Metrics\n")

    if frontend_data and metric_type in ("frontend", "hybrid"):
        for scenario in frontend_data.get("scenarios", []):
            sections.append(generate_scenario_section(scenario))

    if backend_data and metric_type in ("backend", "hybrid"):
        for ep_path, ep_data in backend_data.get("endpoints", {}).items():
            sections.append(generate_backend_scenario_section(ep_path, ep_data))

    # --- Resource timing ---
    if frontend_data and metric_type in ("frontend", "hybrid"):
        sections.append("## Resource Timing Breakdown\n")
        sections.append("Top resources by load duration across all scenarios:\n")
        sections.append(generate_resource_table(frontend_data.get("scenarios", [])))
        sections.append("")

    # --- Waterfall ---
    if frontend_data and metric_type in ("frontend", "hybrid"):
        sections.append("## Waterfall Visualization\n")
        for scenario in frontend_data.get("scenarios", []):
            all_res = []
            for res_type in ("scripts", "stylesheets", "images", "fetch"):
                items = scenario.get("resources", {}).get(res_type, {}).get("items", [])
                for item in items:
                    all_res.append({
                        "name": item.get("name", item.get("url", "?")),
                        "type": res_type.rstrip("s"),
                        "duration": item.get("duration", 0),
                        "startTime": item.get("startTime", 0),
                    })
            sections.append(generate_waterfall(all_res, scenario.get("name", "unknown")))

    # --- Comparison ---
    sections.append("## Comparison with Previous Baseline\n")
    current_agg = frontend_data.get("aggregate", {}) if frontend_data else {}
    sections.append(generate_comparison(current_agg, previous_metrics or {}))
    sections.append("")

    # --- Known limitations (static) ---
    sections.append("""---

## Known Limitations

This baseline measures performance under controlled conditions. It does not capture
interactive workflows, runtime performance, or concurrent load behavior.
See the full baseline-report template for detailed limitation descriptions.

## Next Steps

1. Review scenarios with LCP > 2.5s or DOM Interactive > 3.5s
2. Identify heavy resources (> 500KB scripts, > 200KB stylesheets)
3. Run module-level analysis: `/sdlc-workflow:performance-analyze-module`
""")

    return "\n".join(sections)


# --- CLI ---


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="perf-baseline-report.py",
        description="Generate performance baseline reports from JSON data",
    )
    parser.add_argument("--frontend-json", help="Path to frontend (Playwright) JSON results")
    parser.add_argument("--backend-json", help="Path to backend (benchmark) JSON results")
    parser.add_argument("--config", required=True, help="Path to performance-config.json")
    parser.add_argument("--output", required=True, help="Path to write the baseline report")
    parser.add_argument("--previous", help="Path to previous baseline report (for comparison)")

    args = parser.parse_args()

    if not args.frontend_json and not args.backend_json:
        print("Error: At least one of --frontend-json or --backend-json is required", file=sys.stderr)
        sys.exit(1)

    # Load inputs
    frontend_data = None
    if args.frontend_json:
        try:
            with open(args.frontend_json) as f:
                frontend_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading frontend JSON: {e}", file=sys.stderr)
            sys.exit(1)

    backend_data = None
    if args.backend_json:
        try:
            with open(args.backend_json) as f:
                backend_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading backend JSON: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        with open(args.config) as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading config: {e}", file=sys.stderr)
        sys.exit(1)

    previous_metrics = None
    if args.previous and os.path.exists(args.previous):
        previous_metrics = parse_previous_baseline(args.previous)

    report = generate_report(frontend_data, backend_data, config, previous_metrics)

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w") as f:
        f.write(report)

    print(f"Baseline report generated: {args.output}")
    print(f"  Mode: {config.get('metadata', {}).get('metric_type', 'unknown')}")
    if frontend_data:
        print(f"  Frontend scenarios: {len(frontend_data.get('scenarios', []))}")
    if backend_data:
        print(f"  Backend endpoints: {len(backend_data.get('endpoints', {}))}")


if __name__ == "__main__":
    main()
