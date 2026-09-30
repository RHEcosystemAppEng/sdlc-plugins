---
generated_by: {skill-name}
timestamp: {iso-8601-timestamp}
repository: {repository-name}
capture_mode: {capture-mode}
---

# Performance Baseline Report

## Configuration Summary

- **Capture Date:** {capture-date}
- **Iterations:** {iterations}
- **Warmup Runs:** {warmup-runs}
- **Scenarios Measured:** {scenario-count}

## Capture Mode

**Mode:** {capture-mode}

{mode-description}

**Mode descriptions:**
- **cold-start:** Direct URL navigation with cold cache. Measures worst-case/first-visit performance.

---

## Summary Metrics

**Capture Mode:** {capture-mode}

**Frontend Performance Metrics** (if capture-mode includes "cold-start" or "hybrid"):

Mean of per-scenario values (not a statistically pooled aggregate).

| Metric | Mean | p50 (Median) | p95 | p99 | Unit |
|---|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | {lcp-mean} | {lcp-p50} | {lcp-p95} | {lcp-p99} | ms |
| **FCP** (First Contentful Paint) | {fcp-mean} | {fcp-p50} | {fcp-p95} | {fcp-p99} | ms |
| **DOM Interactive** | {domInteractive-mean} | {domInteractive-p50} | {domInteractive-p95} | {domInteractive-p99} | ms |
| **Total Load Time** | {total-mean} | {total-p50} | {total-p95} | {total-p99} | ms |

**Backend API Performance Metrics** (if capture-mode includes "api-benchmark" or "hybrid"):

Overall API performance across all endpoints.

| Metric | Mean | p50 (Median) | p95 | p99 | Unit |
|---|---|---|---|---|---|
| **Response Time** | {response-mean} | {response-p50} | {response-p95} | {response-p99} | ms |
| **Throughput** | - | - | {throughput-p95} | - | req/sec |
| **Error Rate** | - | - | {error-rate-p95} | - | % |
| **Cache Effectiveness** | - | - | {cache-improvement-pct} | - | % improvement |

## API Correlation

**Included when:** capture-mode = "hybrid" AND workflow.traced_api_endpoints is non-empty.

Frontend routes and their traced backend API calls for the selected workflow.

| Frontend Route | Route Load p95 (ms) | Traced APIs | Slowest Traced API | In-Page Fetch Time (ms) | Isolated API p95 (ms) |
|---|---|---|---|---|---|
| {route-url} | {route-load-p95} | {api-count} | {slowest-api-path} | {fetch-resource-timing-ms} | {benchmark-p95-ms} |

**Notes:**
- "In-Page Fetch Time" is from Playwright resource timing (Fetch/XHR entries) — actual duration during page load.
- "Isolated API p95" is from perf-benchmark.sh — latency without browser overhead.
- Large gap between in-page and isolated time may indicate parallel API loading or frontend processing overhead.
- APIs are not necessarily sequential — do not sum API times to explain route load time.

## Per-Scenario Metrics

{per-scenario-sections}

## Resource Timing Breakdown

Top resources by load duration across all scenarios:

| Resource | Type | Duration (ms) | Size (KB) | Scenario |
|---|---|---|---|---|
| {resource-1-name} | {resource-1-type} | {resource-1-duration} | {resource-1-size} | {resource-1-scenario} |
| {resource-2-name} | {resource-2-type} | {resource-2-duration} | {resource-2-size} | {resource-2-scenario} |
| {resource-3-name} | {resource-3-type} | {resource-3-duration} | {resource-3-size} | {resource-3-scenario} |

## Waterfall Visualization

Resource load timeline for {waterfall-scenario-name}:

```
{waterfall-ascii-chart}
```

**Legend:**
- `[====]` Script
- `[----]` Stylesheet
- `[****]` Image
- `[++++]` Fetch/XHR

## Comparison with Previous Baseline

{comparison-section}

## Known Limitations

**Frontend Baselines** (if capture-mode = "cold-start" or "hybrid"):

This baseline measures **cold-start performance** (initial page load with empty cache). It does **not** capture:

- **Interactive workflow performance:** Multi-step user journeys (e.g., login → search → view details → edit)
- **Client-side navigation:** Route transitions within single-page applications
- **Runtime performance:** JavaScript execution time, memory usage, or long tasks
- **User interaction latency:** Click-to-response time, form submission delays, or scroll performance
- **Progressive enhancement:** Performance improvements from service workers, prefetching, or caching strategies

**What frontend baselines are useful for:**

✅ First-visit experience (e.g., users arriving from search engines, direct links, or bookmarks)  
✅ Bundle size analysis (identifying large scripts, stylesheets, or vendor libraries)  
✅ Resource loading waterfall (detecting sequential loading or render-blocking resources)  

**What frontend baselines don't measure:**

❌ **Interactive workflows:** Use Chrome DevTools Performance panel or Lighthouse User Flows  
❌ **Runtime performance:** Use Chrome DevTools Performance profiler or Web Vitals library  
❌ **Repeat-visit performance:** Re-run baseline with warm cache mode (future enhancement)

**Backend Baselines** (if capture-mode = "api-benchmark" or "hybrid"):

This baseline measures **API endpoint performance** under controlled load (curl/bc HTTP benchmarking). It does **not** capture:

- **Database query-level profiling:** Individual query execution times (use database slow query logs or APM tools)
- **Connection pool saturation:** Maximum concurrent connection limits or pool exhaustion behavior
- **Memory profiling:** Heap usage, garbage collection pauses, or memory leaks
- **Actual cache hit rates:** Only measures latency difference between cold and warm, not true cache effectiveness
- **Concurrent load behavior:** Uses serial requests (c=1) for consistent measurement, not realistic concurrent traffic

**What backend baselines are useful for:**

✅ API response time percentiles (p50, p95, p99) for each endpoint  
✅ Throughput capacity baseline (requests/second per endpoint)  
✅ Error rate baseline (4xx/5xx response percentages)  
✅ Cache effectiveness (cold vs warm latency comparison)

**What backend baselines don't measure:**

❌ **Query-level profiling:** Use database APM tools (Prometheus, DataDog, New Relic, etc.)  
❌ **Resource profiling:** Use runtime profilers (perf for Rust/C++, pprof for Go, py-spy for Python, etc.)  
❌ **Realistic load patterns:** Use dedicated load testing tools (k6, Gatling, JMeter) for production-like traffic

**Percentile Method Note:**

Frontend metrics use linear interpolation percentiles (capture-baseline.mjs); backend metrics (perf-benchmark.sh) use nearest-rank. Values are not directly comparable across frontend and backend legs in hybrid baselines.

## Next Steps

1. Review scenarios with LCP > 2.5s or DOM Interactive > 3.5s
2. Identify heavy resources (> 500KB scripts, > 200KB stylesheets)
3. Run module-level analysis for your selected workflow: `/sdlc-workflow:performance-analyze-module`
