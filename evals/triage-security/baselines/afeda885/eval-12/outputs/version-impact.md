# Step 2 -- Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

## Enriched Fix Threshold

From Step 1.5 cross-validation: **h2 >= 0.4.8** (versions below 0.4.8 are affected)

Both MITRE CVE API and OSV.dev agree on this threshold. The Jira description was imprecise and did not provide a concrete version.

## Version Impact Table

| Stream | Version | Build Tag | h2 Version | Affected? | Notes |
|--------|---------|-----------|------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.1 | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Affected Versions | Status |
|--------|-------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | AFFECTED -- all versions ship h2 0.4.5 |
| 2.2.x | (none) | NOT AFFECTED -- all versions ship h2 >= 0.4.8 |

## Issue Stream Scope Analysis

This issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`).

Within the scoped stream (2.2.x): **No versions are affected.** All 2.2.x versions ship h2 0.4.8 or later, which is at or above the fix threshold.

## Cross-Stream Impact

Stream 2.1.x IS affected (h2 0.4.5 in all versions), but that stream is outside this issue's scope. Cross-stream impact should be noted and handled via companion issue or preemptive remediation per Step 7 Case B.

## Dependency Chain Context

The h2 crate is a Cargo (Rust) dependency in the backend repository. It provides HTTP/2 protocol support and is typically pulled in transitively through the hyper HTTP library (e.g., backend -> reqwest -> hyper -> h2). As a network protocol crate, it is a production runtime dependency (not dev-only).

## Recommendation

For the scoped stream (2.2.x): **Close as Not a Bug** -- no supported 2.2.x versions ship a vulnerable version of h2. All versions ship h2 >= 0.4.8, which is at or above the fix threshold established by both MITRE and OSV.dev.

For the cross-stream impact (2.1.x): The 2.1.x stream ships h2 0.4.5 (affected). This should be reported as cross-stream impact. Check for an existing 2.1.x companion CVE issue; if none exists, create preemptive remediation tasks per Step 7 Case B.
