# Step 2 -- Version Impact Analysis for CVE-2026-48901

## Enriched Fix Threshold

From Step 1.5 cross-validation: **h2 >= 0.4.8 is fixed** (both MITRE CVE API and OSV.dev agree).

Versions of h2 below 0.4.8 are AFFECTED.

## Stream Scope

This issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`). However, per SKILL.md Rule 4 ("Check ALL supported versions"), the version impact table covers all streams. Affects Versions correction (Step 3) will be scoped to 2.2.x only.

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Tag | h2 version | Affected? | Notes |
|--------|---------|-----|------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  Ecosystem: Cargo (Rust crate via crates.io)
  Library: h2
  Lock file: Cargo.lock
  Repository: backend (rhtpa-backend)

  All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold.
  All 2.1.x versions ship h2 0.4.5, which is below the fix threshold.
```

## Summary by Stream

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | YES | All versions (2.1.0, 2.1.1) ship h2 0.4.5 (< 0.4.8) |
| 2.2.x | NO | All versions ship h2 >= 0.4.8 (at or above fix threshold) |

## Cross-Stream Impact

The issue is scoped to stream 2.2.x, and **no versions in the 2.2.x stream are affected**. However, the 2.1.x stream IS affected (h2 0.4.5 < 0.4.8 in both versions). This is a cross-stream finding that would be reported in the post-triage summary. The 2.1.x stream has its own Konflux release repo and would need its own CVE Jira or preemptive remediation task (see Step 7 Case B).

## Proposed Triage Outcome

Since **no versions in the scoped 2.2.x stream are affected**, the recommendation for TC-8030 is:

- **Case C: Close as Not a Bug** -- no supported versions within the issue's 2.2.x scope ship a vulnerable version of h2.
- All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold.
- VEX Justification: **Component not Present** (the vulnerable version of h2 is not present in any 2.2.x release).
- The 2.1.x cross-stream impact should be noted in a comment for PSIRT awareness.
