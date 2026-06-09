#!/usr/bin/env python3
"""Performance configuration manager for sdlc-workflow performance skills.

Manages .claude/performance-config.json — the structured configuration file
used by all performance skills (performance-setup, performance-baseline,
performance-analyze-module, performance-plan-optimization, implement-task, verify-pr).

Uses only Python stdlib — no external dependencies required.

Subcommands:
    init            Create a new config from CLI arguments
    get             Read a value by dotpath (e.g., metadata.baseline_mode)
    get-section     Dump a top-level section as JSON
    set             Write a scalar value by dotpath
    set-json        Write structured data by dotpath
    validate        Check required fields and value constraints
    resolve-scope   Resolve analysis_scope to capability flags
    resolve-module-path  Pick module directory with most handlers
"""

import argparse
import json
import os
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


DEFAULT_CONFIG_PATH = ".claude/performance-config.json"

DEFAULT_CONFIG = {
    "metadata": {
        "version": "1.0",
        "created": None,
        "last_updated": None,
        "workflow_selected": False,
        "baseline_captured": False,
        "baseline_mode": None,
        "baseline_timestamp": None,
        "baseline_commit_sha": None,
        "capture_target": None,
        "capture_base_url": None,
        "backend_available": False,
        "analysis_scope": "frontend-only",
        "backend_endpoint_discovery_method": None,
        "serena_status": None,
        "metric_type": "frontend",
    },
    "repositories": {
        "frontend": {
            "name": None,
            "path": None,
            "framework": None,
            "bundler": None,
        },
        "backend": {
            "name": None,
            "path": None,
            "framework": None,
            "serena_instance": None,
            "api_base_path": "/api/v2",
            "available": False,
            "last_validated": None,
        },
    },
    "workflow": {
        "name": None,
        "entry_point": None,
        "key_screens": [],
        "complexity": None,
        "selected_on": None,
    },
    "scenarios": [],
    "modules": [],
    "baseline_settings": {
        "iterations": 20,
        "warmup_runs": 2,
    },
    "optimization_targets": {
        "frontend": {
            "lcp": {"baseline": None, "latest": None, "target": 2.5, "unit": "seconds"},
            "fcp": {"baseline": None, "latest": None, "target": 1.8, "unit": "seconds"},
            "dom_interactive": {"baseline": None, "latest": None, "target": 3.5, "unit": "seconds"},
            "total_load_time": {"baseline": None, "latest": None, "target": 4.0, "unit": "seconds"},
        },
        "backend": {
            "response_time_p95": {"baseline": None, "latest": None, "target": 200, "unit": "ms"},
            "response_time_p99": {"baseline": None, "latest": None, "target": 500, "unit": "ms"},
            "throughput": {"baseline": None, "latest": None, "target": 100, "unit": "req/sec"},
            "error_rate": {"baseline": None, "latest": None, "target": 0.1, "unit": "%"},
            "db_query_time_p95": {"baseline": None, "latest": None, "target": 50, "unit": "ms"},
        },
    },
    "analysis_assumptions": {
        "bandwidth_mbps": 5,
        "api_latency_ms": 100,
        "reflow_cost_ms": 5,
        "cache_hit_rate": 0.8,
        "chain_depth": 3,
        "db_latency_ms": 10,
    },
    "dev_environment": {
        "command": None,
        "source": None,
        "port": None,
        "command_approved": False,
        "last_validated": None,
    },
    "directories": {
        "baselines": ".claude/performance/baselines/",
        "analysis": ".claude/performance/analysis/",
        "plans": ".claude/performance/plans/",
        "optimization_results": ".claude/performance/optimization-results/",
        "verification": ".claude/performance/verification/",
        "test_data": ".claude/performance/test-data/",
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_config_path(args_config: Optional[str]) -> str:
    if args_config:
        return args_config
    # Walk up from CWD to find the config, like git finds .git
    current = os.path.abspath(".")
    while True:
        candidate = os.path.join(current, DEFAULT_CONFIG_PATH)
        if os.path.isfile(candidate):
            return candidate
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return DEFAULT_CONFIG_PATH


def read_config(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config not found at {path}", file=sys.stderr)
        print("Run: perf-config.py init  — or —  /sdlc-workflow:performance-setup", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)


def write_config(path: str, config: Dict[str, Any]) -> None:
    """Atomic write: write to temp file then rename."""
    dir_name = os.path.dirname(path) or "."
    os.makedirs(dir_name, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".json.tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(config, f, indent=2)
            f.write("\n")
        os.rename(tmp_path, path)
    except Exception:
        os.unlink(tmp_path)
        raise


class _KeyNotFound(Exception):
    """Raised when a dotpath key is missing and the caller wants to handle it."""


def get_by_dotpath(obj: Any, dotpath: str, raise_on_missing: bool = False) -> Any:
    """Traverse a nested dict/list by dot-separated path.

    Supports integer indices for lists: scenarios.0.name

    If raise_on_missing is True, raises _KeyNotFound instead of calling sys.exit(1)
    when a dict key is absent. Use this when a default value should be printed instead.
    """
    parts = dotpath.split(".")
    current = obj
    for part in parts:
        if isinstance(current, dict):
            if part not in current:
                if raise_on_missing:
                    raise _KeyNotFound(dotpath)
                print(f"Error: Key '{part}' not found in path '{dotpath}'", file=sys.stderr)
                sys.exit(1)
            current = current[part]
        elif isinstance(current, list):
            try:
                idx = int(part)
                current = current[idx]
            except (ValueError, IndexError):
                print(f"Error: Invalid list index '{part}' in path '{dotpath}'", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Error: Cannot traverse into {type(current).__name__} at '{part}' in '{dotpath}'", file=sys.stderr)
            sys.exit(1)
    return current


def set_by_dotpath(obj: Dict, dotpath: str, value: Any) -> None:
    """Set a value in a nested dict by dot-separated path, creating intermediate dicts as needed."""
    parts = dotpath.split(".")
    current = obj
    for part in parts[:-1]:
        if isinstance(current, dict):
            if part not in current:
                current[part] = {}
            current = current[part]
        elif isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                print(f"Error: Invalid list index '{part}' in path '{dotpath}'", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Error: Cannot traverse into {type(current).__name__} at '{part}'", file=sys.stderr)
            sys.exit(1)

    last_key = parts[-1]
    if isinstance(current, dict):
        current[last_key] = value
    elif isinstance(current, list):
        try:
            current[int(last_key)] = value
        except (ValueError, IndexError):
            print(f"Error: Invalid list index '{last_key}' in path '{dotpath}'", file=sys.stderr)
            sys.exit(1)


def parse_scalar(value_str: str) -> Any:
    """Parse a CLI string into a typed Python value."""
    if value_str.lower() == "null" or value_str.lower() == "none":
        return None
    if value_str.lower() == "true":
        return True
    if value_str.lower() == "false":
        return False
    try:
        return int(value_str)
    except ValueError:
        pass
    try:
        return float(value_str)
    except ValueError:
        pass
    return value_str


# --- Subcommands ---


def cmd_init(args: argparse.Namespace) -> None:
    """Create a new performance config from CLI arguments."""
    path = resolve_config_path(args.config)
    if os.path.exists(path) and not args.force:
        print(f"Error: Config already exists at {path}. Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    config = json.loads(json.dumps(DEFAULT_CONFIG))
    ts = now_iso()
    config["metadata"]["created"] = ts
    config["metadata"]["last_updated"] = ts

    if args.analysis_scope:
        config["metadata"]["analysis_scope"] = args.analysis_scope
        config["metadata"]["metric_type"] = _resolve_metric_type(args.analysis_scope)

    if args.frontend_path:
        config["repositories"]["frontend"]["path"] = args.frontend_path
    if args.frontend_framework:
        config["repositories"]["frontend"]["framework"] = args.frontend_framework
    if args.frontend_name:
        config["repositories"]["frontend"]["name"] = args.frontend_name
    if args.bundler:
        config["repositories"]["frontend"]["bundler"] = args.bundler

    if args.backend_path:
        config["repositories"]["backend"]["path"] = args.backend_path
        config["repositories"]["backend"]["available"] = True
        config["repositories"]["backend"]["last_validated"] = ts
        config["metadata"]["backend_available"] = True
    if args.backend_framework:
        config["repositories"]["backend"]["framework"] = args.backend_framework
    if args.backend_name:
        config["repositories"]["backend"]["name"] = args.backend_name
    if args.api_base_path:
        config["repositories"]["backend"]["api_base_path"] = args.api_base_path
    if args.serena_instance:
        config["repositories"]["backend"]["serena_instance"] = args.serena_instance
    if args.serena_status:
        config["metadata"]["serena_status"] = args.serena_status

    if args.lcp_target is not None:
        config["optimization_targets"]["frontend"]["lcp"]["target"] = args.lcp_target
    if args.fcp_target is not None:
        config["optimization_targets"]["frontend"]["fcp"]["target"] = args.fcp_target
    if args.dom_target is not None:
        config["optimization_targets"]["frontend"]["dom_interactive"]["target"] = args.dom_target
    if args.total_target is not None:
        config["optimization_targets"]["frontend"]["total_load_time"]["target"] = args.total_target

    if args.resp_p95_target is not None:
        config["optimization_targets"]["backend"]["response_time_p95"]["target"] = args.resp_p95_target
    if args.resp_p99_target is not None:
        config["optimization_targets"]["backend"]["response_time_p99"]["target"] = args.resp_p99_target
    if args.throughput_target is not None:
        config["optimization_targets"]["backend"]["throughput"]["target"] = args.throughput_target
    if args.error_rate_target is not None:
        config["optimization_targets"]["backend"]["error_rate"]["target"] = args.error_rate_target
    if args.db_query_time_target is not None:
        config["optimization_targets"]["backend"]["db_query_time_p95"]["target"] = args.db_query_time_target

    if args.iterations is not None:
        config["baseline_settings"]["iterations"] = args.iterations
    if args.warmup_runs is not None:
        config["baseline_settings"]["warmup_runs"] = args.warmup_runs

    write_config(path, config)
    print(f"Config created at {path}")


def cmd_get(args: argparse.Namespace) -> None:
    """Read a value by dotpath and print to stdout."""
    config = read_config(resolve_config_path(args.config))
    try:
        value = get_by_dotpath(config, args.dotpath,
                               raise_on_missing=(args.default_value is not None))
    except _KeyNotFound:
        print(args.default_value)
        return
    if isinstance(value, (dict, list)):
        print(json.dumps(value, indent=2))
    elif value is None:
        print("null")
    elif isinstance(value, bool):
        print("true" if value else "false")
    else:
        print(value)


def cmd_get_section(args: argparse.Namespace) -> None:
    """Dump a top-level section as JSON."""
    config = read_config(resolve_config_path(args.config))
    if args.section not in config:
        print(f"Error: Section '{args.section}' not found", file=sys.stderr)
        print(f"Available sections: {', '.join(config.keys())}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(config[args.section], indent=2))


def cmd_set(args: argparse.Namespace) -> None:
    """Write a scalar value by dotpath."""
    path = resolve_config_path(args.config)
    config = read_config(path)
    value = parse_scalar(args.value)
    set_by_dotpath(config, args.dotpath, value)
    if args.dotpath == "metadata.analysis_scope" and isinstance(value, str):
        resolved = _resolve_metric_type(value)
        if resolved:
            config["metadata"]["metric_type"] = resolved
    config["metadata"]["last_updated"] = now_iso()
    write_config(path, config)


def cmd_set_json(args: argparse.Namespace) -> None:
    """Write structured JSON data by dotpath."""
    path = resolve_config_path(args.config)
    config = read_config(path)
    try:
        value = json.loads(args.json_value)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON value: {e}", file=sys.stderr)
        sys.exit(1)
    set_by_dotpath(config, args.dotpath, value)
    if args.dotpath == "metadata.analysis_scope" and isinstance(value, str):
        resolved = _resolve_metric_type(value)
        if resolved:
            config["metadata"]["metric_type"] = resolved
    config["metadata"]["last_updated"] = now_iso()
    write_config(path, config)


def _resolve_metric_type(scope: str) -> Optional[str]:
    """Map analysis_scope to expected metric_type."""
    return {
        "frontend-only": "frontend",
        "backend-only": "backend",
        "full-stack": "hybrid",
        "full-stack-monorepo": "hybrid",
    }.get(scope)


def cmd_validate(args: argparse.Namespace) -> None:
    """Validate config structure and value constraints.

    --phase baseline: additionally checks that config is ready for baseline capture.
    Default (no --phase): structural validation only.
    """
    config = read_config(resolve_config_path(args.config))
    errors: List[str] = []
    phase = getattr(args, "phase", None)

    # --- Structural validation (always runs) ---

    required_sections = ["metadata", "repositories", "workflow", "scenarios",
                         "modules", "baseline_settings", "optimization_targets",
                         "analysis_assumptions", "dev_environment", "directories"]
    for section in required_sections:
        if section not in config:
            errors.append(f"Missing required section: {section}")

    if "metadata" in config:
        m = config["metadata"]
        valid_scopes = ["frontend-only", "backend-only", "full-stack", "full-stack-monorepo"]
        scope = m.get("analysis_scope")
        if scope and scope not in valid_scopes:
            errors.append(f"metadata.analysis_scope must be one of {valid_scopes}, got '{scope}'")

        valid_types = ["frontend", "backend", "hybrid", None]
        mt = m.get("metric_type")
        if mt not in valid_types:
            errors.append(f"metadata.metric_type must be one of {valid_types}, got '{mt}'")

        # metric_type ↔ analysis_scope consistency
        if scope and mt:
            expected = _resolve_metric_type(scope)
            if expected and mt != expected:
                errors.append(f"metadata.metric_type '{mt}' inconsistent with analysis_scope '{scope}' (expected '{expected}')")

        valid_targets = ["localhost", "hosted", None]
        ct = m.get("capture_target")
        if ct not in valid_targets:
            errors.append(f"metadata.capture_target must be one of {valid_targets}, got '{ct}'")

    if "baseline_settings" in config:
        bs = config["baseline_settings"]
        iters = bs.get("iterations", 0)
        if not isinstance(iters, int) or iters < 1:
            errors.append(f"baseline_settings.iterations must be a positive integer, got {iters}")

    if "analysis_assumptions" in config:
        aa = config["analysis_assumptions"]
        if aa.get("bandwidth_mbps", 0) <= 0:
            errors.append("analysis_assumptions.bandwidth_mbps must be > 0")
        if aa.get("api_latency_ms", 0) <= 0:
            errors.append("analysis_assumptions.api_latency_ms must be > 0")
        if aa.get("reflow_cost_ms", 0) <= 0:
            errors.append("analysis_assumptions.reflow_cost_ms must be > 0")
        hit_rate = aa.get("cache_hit_rate", -1)
        if not (0.0 <= hit_rate <= 1.0):
            errors.append(f"analysis_assumptions.cache_hit_rate must be 0.0-1.0, got {hit_rate}")
        depth = aa.get("chain_depth", 0)
        if not isinstance(depth, int) or not (1 <= depth <= 5):
            errors.append(f"analysis_assumptions.chain_depth must be int 1-5, got {depth}")
        if aa.get("db_latency_ms", 0) <= 0:
            errors.append("analysis_assumptions.db_latency_ms must be > 0")

    # --- Baseline-readiness validation (--phase baseline) ---

    if phase == "baseline":
        scenarios = config.get("scenarios", [])
        if not scenarios:
            errors.append("scenarios must contain at least 1 entry for baseline capture")
        else:
            for i, s in enumerate(scenarios):
                if not s.get("name"):
                    errors.append(f"scenarios[{i}].name is empty")
                if not s.get("url"):
                    errors.append(f"scenarios[{i}].url is empty")

        dev = config.get("dev_environment", {})
        port = dev.get("port")
        if port is not None:
            if not isinstance(port, int) or port < 1 or port > 65535:
                errors.append(f"dev_environment.port must be integer 1-65535, got {port}")

        bs = config.get("baseline_settings", {})
        iters = bs.get("iterations", 0)
        warmup = bs.get("warmup_runs", 0)
        if isinstance(warmup, int) and warmup < 0:
            errors.append(f"baseline_settings.warmup_runs must be >= 0, got {warmup}")
        if isinstance(warmup, int) and warmup > 10:
            errors.append(f"baseline_settings.warmup_runs must be <= 10, got {warmup}")
        if isinstance(iters, int) and iters < 20:
            print(f"Warning: {iters} iterations — p95 may not be statistically reliable (≥20 recommended).", file=sys.stderr)

        if config.get("metadata", {}).get("workflow_selected"):
            wf = config.get("workflow", {})
            if not wf.get("name"):
                errors.append("workflow.name required when workflow_selected is true")
            if not wf.get("entry_point"):
                errors.append("workflow.entry_point required when workflow_selected is true")
            modules = config.get("modules", [])
            if not modules:
                errors.append("modules must be non-empty when workflow_selected is true")
            else:
                for i, mod in enumerate(modules):
                    if not mod.get("name"):
                        errors.append(f"modules[{i}].name is empty")
                    if not mod.get("entry_point"):
                        errors.append(f"modules[{i}].entry_point is empty")

    if errors:
        print("Validation FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print("Validation passed")


def cmd_resolve_scope(args: argparse.Namespace) -> None:
    """Resolve analysis_scope into capability flags."""
    config = read_config(resolve_config_path(args.config))
    scope = config.get("metadata", {}).get("analysis_scope", "frontend-only")

    flags = {
        "scope": scope,
        "frontend_capture": scope in ("frontend-only", "full-stack", "full-stack-monorepo"),
        "backend_capture": scope in ("backend-only", "full-stack", "full-stack-monorepo"),
        "browser_metrics": scope in ("frontend-only", "full-stack", "full-stack-monorepo"),
        "api_metrics": scope in ("backend-only", "full-stack", "full-stack-monorepo"),
        "same_repo": scope == "full-stack-monorepo",
    }
    print(json.dumps(flags))


def cmd_resolve_module_path(args: argparse.Namespace) -> None:
    """Pick the module directory containing the most handler files.

    Precondition: config must have workflow_selected=true and modules populated.
    Returns empty string if no modules found.
    """
    config = read_config(resolve_config_path(args.config))
    handlers = config.get("modules", [])
    if not handlers:
        print("")
        return

    dirs: List[str] = []
    for h in handlers:
        entry = h.get("entry_point", "")
        parts = entry.split("/")
        if len(parts) > 1:
            dir_path = "/".join(parts[:-1])
            dirs.append(dir_path)

    if not dirs:
        print("")
        return

    counts = Counter(dirs)
    print(counts.most_common(1)[0][0])


# --- CLI ---


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="perf-config.py",
        description="Performance configuration manager for sdlc-workflow",
    )
    parser.add_argument("--config", "-c", help=f"Config file path. Default: walks up from CWD to find {DEFAULT_CONFIG_PATH}")
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = sub.add_parser("init", help="Create a new performance config")
    p_init.add_argument("--analysis-scope", choices=["frontend-only", "backend-only", "full-stack", "full-stack-monorepo"])
    p_init.add_argument("--frontend-path")
    p_init.add_argument("--frontend-framework")
    p_init.add_argument("--frontend-name")
    p_init.add_argument("--bundler")
    p_init.add_argument("--backend-path")
    p_init.add_argument("--backend-framework")
    p_init.add_argument("--backend-name")
    p_init.add_argument("--api-base-path")
    p_init.add_argument("--serena-instance")
    p_init.add_argument("--serena-status")
    p_init.add_argument("--lcp-target", type=float)
    p_init.add_argument("--fcp-target", type=float)
    p_init.add_argument("--dom-target", type=float)
    p_init.add_argument("--total-target", type=float)
    p_init.add_argument("--resp-p95-target", type=float)
    p_init.add_argument("--resp-p99-target", type=float)
    p_init.add_argument("--throughput-target", type=float)
    p_init.add_argument("--error-rate-target", type=float)
    p_init.add_argument("--db-query-time-target", type=float)
    p_init.add_argument("--iterations", type=int)
    p_init.add_argument("--warmup-runs", type=int)
    p_init.add_argument("--force", action="store_true", help="Overwrite existing config")

    # get
    p_get = sub.add_parser("get", help="Read a value by dotpath")
    p_get.add_argument("dotpath", help="Dot-separated path (e.g., metadata.baseline_mode)")
    p_get.add_argument("--default", default=None, dest="default_value",
                       help="Value to print if dotpath not found (instead of exiting 1)")

    # get-section
    p_gs = sub.add_parser("get-section", help="Dump a top-level section as JSON")
    p_gs.add_argument("section", help="Section name (e.g., workflow, scenarios)")

    # set
    p_set = sub.add_parser("set", help="Write a scalar value")
    p_set.add_argument("dotpath", help="Dot-separated path")
    p_set.add_argument("value", help="Value to set (auto-typed: null, true, false, int, float, string)")

    # set-json
    p_sj = sub.add_parser("set-json", help="Write structured JSON data")
    p_sj.add_argument("dotpath", help="Dot-separated path")
    p_sj.add_argument("json_value", help="JSON string to set")

    # validate
    p_val = sub.add_parser("validate", help="Validate config structure and constraints")
    p_val.add_argument("--phase", choices=["baseline"], default=None,
                       help="Additional phase-specific checks (baseline: ready-to-capture)")

    # resolve-scope
    sub.add_parser("resolve-scope", help="Resolve analysis_scope to capability flags")

    # resolve-module-path
    sub.add_parser("resolve-module-path", help="Pick module directory with most handlers")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "init": cmd_init,
        "get": cmd_get,
        "get-section": cmd_get_section,
        "set": cmd_set,
        "set-json": cmd_set_json,
        "validate": cmd_validate,
        "resolve-scope": cmd_resolve_scope,
        "resolve-module-path": cmd_resolve_module_path,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
