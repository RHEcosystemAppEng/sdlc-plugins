<!-- SYNTHETIC TEST DATA — Mock baseline report for eval -->
# Performance Baseline Report

## Configuration Summary
- **Capture Date:** 2026-06-01T10:00:00Z
- **Iterations:** 20
- **Warmup Runs:** 2
- **Scenarios Measured:** 1

## Summary Metrics

| Metric | Mean | p50 | p95 | p99 | Unit |
|---|---|---|---|---|---|
| **LCP** | 2800 | 2600 | 3200 | 3500 | ms |
| **FCP** | 1900 | 1800 | 2100 | 2300 | ms |
| **DOM Interactive** | 4000 | 3800 | 4500 | 4800 | ms |
| **Total Load Time** | 5200 | 5000 | 5800 | 6200 | ms |

## Per-Scenario Metrics

### /dashboard
| Metric | Mean | p50 | p95 | p99 | Unit |
|---|---|---|---|---|---|
| LCP | 2800 | 2600 | 3200 | 3500 | ms |
| FCP | 1900 | 1800 | 2100 | 2300 | ms |
| DOM Interactive | 4000 | 3800 | 4500 | 4800 | ms |
| Total Load Time | 5200 | 5000 | 5800 | 6200 | ms |

## Resource Timing Breakdown

| Resource | Type | Duration (ms) | Size (KB) | Scenario |
|---|---|---|---|---|
| /assets/vendor.js | Script | 1200 | 450 | /dashboard |
| /assets/app.js | Script | 800 | 280 | /dashboard |
| /assets/chart-lib.js | Script | 600 | 350 | /dashboard |
| /api/v2/products | Fetch/XHR | 320 | 12 | /dashboard |
| /assets/styles.css | Stylesheet | 150 | 45 | /dashboard |
