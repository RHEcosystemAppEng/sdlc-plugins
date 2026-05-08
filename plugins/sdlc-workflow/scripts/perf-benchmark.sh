#!/usr/bin/env bash
#
# perf-benchmark.sh — API endpoint benchmarking with percentile calculation
#
# Runs curl loops against backend endpoints, computes p50/p95/p99 latencies,
# measures cache effectiveness (cold vs warm), and outputs structured JSON.
#
# Usage:
#   perf-benchmark.sh --port PORT --iterations N --manifest PATH --output PATH
#
# Prerequisites: curl, jq (both verified at startup)
# No bc dependency — all floating-point math uses awk.
#
# Manifest schema (JSON, keyed by endpoint path):
#   {
#     "endpoints": {
#       "/api/v2/products": {
#         "test_url": "/api/v2/products",
#         "parameters": {"id": "abc-123"}
#       }
#     }
#   }
#
# Output schema (JSON):
#   {
#     "endpoints": { "<path>": { p50_ms, p95_ms, p99_ms, mean_ms, ... } },
#     "aggregate": { mean_ms, p50_ms, p95_ms, p99_ms },
#     "config": { iterations, warmup_runs },
#     "errors": { failed_count, failed_endpoints: [] }
#   }

set -euo pipefail

# --- Argument parsing ---

usage() {
  cat >&2 <<EOF
Usage: perf-benchmark.sh --port PORT --iterations N --manifest PATH --output PATH

Arguments:
  --port PORT          Localhost port where backend is running
  --iterations N       Number of warm-cache requests per endpoint (default: 20)
  --manifest PATH      Path to test-data manifest JSON
  --output PATH        Path to write results JSON

Example:
  perf-benchmark.sh --port 8080 --iterations 20 \\
    --manifest .claude/performance/test-data/manifest.json \\
    --output .claude/performance/baselines/benchmark-results.json
EOF
  exit 1
}

PORT=""
ITERATIONS=20
MANIFEST=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --port) PORT="$2"; shift 2 ;;
    --iterations) ITERATIONS="$2"; shift 2 ;;
    --manifest) MANIFEST="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --help|-h) usage ;;
    *) echo "Unknown argument: $1" >&2; usage ;;
  esac
done

if [[ -z "$PORT" || -z "$MANIFEST" || -z "$OUTPUT" ]]; then
  echo "Error: --port, --manifest, and --output are required" >&2
  usage
fi

# --- Prerequisite checks ---

for cmd in curl jq; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "Error: $cmd not found. Install it and retry." >&2
    exit 1
  fi
done

if ! timeout 2 bash -c "</dev/tcp/localhost/$PORT" 2>/dev/null; then
  echo "Error: Nothing listening on localhost:$PORT" >&2
  exit 1
fi

if [[ ! -f "$MANIFEST" ]]; then
  echo "Error: Manifest not found at $MANIFEST" >&2
  exit 1
fi

# --- Percentile function ---
# Uses nearest-rank method: p = sorted[ceil(n * percentile/100) - 1]
# Input: sorted array (via nameref), percentile (0-100)
# Correct for n=20: p95 = sorted[ceil(20*0.95)-1] = sorted[18] (second-highest)

percentile_index() {
  local n="$1"
  local pct="$2"
  # ceil(n * pct / 100) - 1, clamped to [0, n-1]
  local idx
  idx=$(awk -v n="$n" -v p="$pct" 'BEGIN {
    raw = n * p / 100
    ceiled = (raw == int(raw)) ? raw : int(raw) + 1
    idx = ceiled - 1
    if (idx < 0) idx = 0
    if (idx >= n) idx = n - 1
    printf "%d", idx
  }')
  echo "$idx"
}

# --- Benchmark loop ---

endpoint_results='{}' # jq accumulator
failed_endpoints='[]'
failed_count=0
total_endpoints=0

while IFS='|' read -r endpoint_path test_url; do
  total_endpoints=$((total_endpoints + 1))
  url="http://localhost:${PORT}${test_url}"

  echo "Benchmarking: $endpoint_path ($url)"

  # 1. Cold-cache request (first request, measures worst-case)
  first_request_s=$(curl -o /dev/null -s -w '%{time_total}' --max-time 30 "$url" 2>/dev/null || echo "")
  if [[ -z "$first_request_s" ]]; then
    echo "  Warning: First request failed, skipping endpoint"
    failed_count=$((failed_count + 1))
    failed_endpoints=$(echo "$failed_endpoints" | jq --arg ep "$endpoint_path" '. + [$ep]')
    continue
  fi
  first_request_ms=$(awk -v t="$first_request_s" 'BEGIN { printf "%.0f", t * 1000 }')

  # 2. Warm-cache requests
  times=()
  for i in $(seq 1 "$ITERATIONS"); do
    t=$(curl -o /dev/null -s -w '%{time_total}' --max-time 30 "$url" 2>/dev/null || echo "")
    if [[ -n "$t" ]]; then
      ms=$(awk -v t="$t" 'BEGIN { printf "%.0f", t * 1000 }')
      times+=("$ms")
    fi
  done

  if [[ ${#times[@]} -eq 0 ]]; then
    echo "  Warning: All warm-cache requests failed, skipping endpoint"
    failed_count=$((failed_count + 1))
    failed_endpoints=$(echo "$failed_endpoints" | jq --arg ep "$endpoint_path" '. + [$ep]')
    continue
  fi

  # 3. Sort and compute percentiles
  sorted=($(printf '%s\n' "${times[@]}" | sort -n))
  n=${#sorted[@]}

  p50_idx=$(percentile_index "$n" 50)
  p95_idx=$(percentile_index "$n" 95)
  p99_idx=$(percentile_index "$n" 99)

  p50=${sorted[$p50_idx]}
  p95=${sorted[$p95_idx]}
  p99=${sorted[$p99_idx]}
  mean=$(printf '%s\n' "${times[@]}" | awk '{ s += $1 } END { printf "%.0f", s/NR }')

  # 4. Cache effectiveness (awk instead of bc)
  cache_improvement="0"
  cache_status="N/A"
  if [[ "$first_request_ms" -gt 0 ]]; then
    cache_improvement=$(awk -v cold="$first_request_ms" -v warm="$mean" \
      'BEGIN { printf "%.2f", (cold - warm) / cold * 100 }')
    cache_status=$(awk -v imp="$cache_improvement" 'BEGIN {
      if (imp + 0 > 50) print "Effective"
      else if (imp + 0 > 20) print "Moderate"
      else print "Minimal"
    }')
  fi

  # 5. Build endpoint result via jq
  endpoint_json=$(jq -n \
    --arg url "$test_url" \
    --argjson iters "$ITERATIONS" \
    --argjson p50 "$p50" \
    --argjson p95 "$p95" \
    --argjson p99 "$p99" \
    --argjson mean "$mean" \
    --argjson first "$first_request_ms" \
    --arg cache_pct "$cache_improvement" \
    --arg cache_stat "$cache_status" \
    --argjson samples "$n" \
    '{
      test_url: $url,
      iterations: $iters,
      samples_collected: $samples,
      p50_ms: $p50,
      p95_ms: $p95,
      p99_ms: $p99,
      mean_ms: $mean,
      first_request_ms: $first,
      subsequent_mean_ms: $mean,
      cache_improvement_pct: $cache_pct,
      cache_status: $cache_stat
    }')

  endpoint_results=$(echo "$endpoint_results" | jq --arg key "$endpoint_path" --argjson val "$endpoint_json" '. + {($key): $val}')

  echo "  p50: ${p50}ms  p95: ${p95}ms  p99: ${p99}ms  cache: ${cache_improvement}% (${cache_status})"

done < <(jq -r '.endpoints | to_entries[] | "\(.key)|\(.value.test_url)"' "$MANIFEST")

# --- Compute aggregate stats ---

if [[ $(echo "$endpoint_results" | jq 'length') -gt 0 ]]; then
  aggregate=$(echo "$endpoint_results" | jq '{
    mean_ms: ([.[].mean_ms] | add / length | floor),
    p50_ms: ([.[].p50_ms] | add / length | floor),
    p95_ms: ([.[].p95_ms] | add / length | floor),
    p99_ms: ([.[].p99_ms] | add / length | floor)
  }')
else
  aggregate='{"mean_ms": 0, "p50_ms": 0, "p95_ms": 0, "p99_ms": 0}'
fi

# --- Write output ---

mkdir -p "$(dirname "$OUTPUT")"

jq -n \
  --argjson endpoints "$endpoint_results" \
  --argjson aggregate "$aggregate" \
  --argjson iterations "$ITERATIONS" \
  --argjson failed_count "$failed_count" \
  --argjson failed_endpoints "$failed_endpoints" \
  --argjson total "$total_endpoints" \
  '{
    endpoints: $endpoints,
    aggregate: $aggregate,
    config: {
      iterations: $iterations,
      warmup_runs: 0,
      mode: "api-benchmark"
    },
    summary: {
      total_endpoints: $total,
      successful_endpoints: ($total - $failed_count),
      failed_endpoints: $failed_endpoints,
      failed_count: $failed_count
    }
  }' > "$OUTPUT"

echo ""
echo "Benchmark complete: $((total_endpoints - failed_count))/$total_endpoints endpoints profiled"
echo "Results: $OUTPUT"
if [[ $failed_count -gt 0 ]]; then
  echo "Warning: $failed_count endpoint(s) failed"
fi
