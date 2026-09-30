<!-- SYNTHETIC TEST DATA — DO NOT USE IN PRODUCTION -->

# Performance Analysis Report

**Generated:** 2026-06-09T11:00:00Z
**Workflow:** package-listing
**Baseline Date:** 2026-06-08T14:00:00Z
**Validation Artifact:** `performance/analysis/findings-validation.json`
**Validation Status:** passed

---

## Workflow Metrics

| Metric | Current (p95) | Target | Status |
|---|---|---|---|
| LCP (Largest Contentful Paint) | 2400 ms | 2500 ms | Good |
| FCP (First Contentful Paint) | 1700 ms | 1800 ms | Good |
| DOM Interactive | 3300 ms | 3500 ms | Good |
| Total Load Time | 3800 ms | 4000 ms | Good |

---

## Bundle Composition

**Total JavaScript Size:** 680 KB
**Third-Party Libraries:** 420 KB (62%)
**Application Code:** 260 KB (38%)

**Top Third-Party Libraries by Size:**

| Library | Size | Used In |
|---|---|---|
| react-dom | 130 KB | /packages, /packages/:id |
| date-fns | 45 KB | /packages |

---

## Finding Validation Summary

**Validation Step:** Step 9.1 re-verified all findings against source code before report generation.

| # | Finding | Anti-Pattern | Step | Disposition | Confidence | Severity | Timeline | Notes |
|---|---|---|---|---|---|---|---|---|
| F1 | API response includes 50KB of unused advisory metadata | Over-Fetching | 8.A | Discarded | Low | Low | 1-4 hours | Source file was refactored since baseline capture |
| F2 | Unused utility function formatCurrency | Unused Code | 6.5 | Discarded | Low | Low | < 1 hour | Function referenced in test files and storybook |
| F3 | PackageCard component missing React.memo | Missing Memoization | 6.2 | Discarded | Low | Low | < 1 hour | Component already wrapped in React.memo |

**Validation Statistics:**
- Findings submitted: 3
- Confirmed: 0 (0%)
- Confirmed (Low Confidence): 0 (0%)
- Downgraded: 0 (0%)
- Discarded: 3 (100%)

### Discarded Findings (Audit Trail)

| # | Original Claim | Step | File:Line | Discard Reason |
|---|---|---|---|---|
| F1 | Over-fetching in advisory response | 8.A | src/handlers/packages.rs:87 | FAILED: code pattern not found at recorded location -- handler refactored |
| F2 | Unused formatCurrency function | 6.5 | src/utils/formatters.ts:12 | FAILED: function is referenced in test files and storybook |
| F3 | PackageCard missing memoization | 6.2 | src/components/PackageCard.tsx:15 | FAILED: component already wrapped in React.memo at line 45 |

---

## Anti-Pattern Analysis

No confirmed anti-patterns detected after validation.

---

## Recommended Optimizations

No optimizations recommended -- all findings were discarded during validation.

---

## Executive Summary

**Overall Performance Rating:** Good

**Key Findings:**
- All 3 initial findings were discarded during validation (source changes, false positives)
- Current metrics meet all target thresholds
- No performance issues identified after validation

---

## Next Steps

1. No immediate optimization actions required
2. Consider re-running analysis after next significant feature addition
3. Continue monitoring performance baselines with `/sdlc-workflow:performance-baseline`
