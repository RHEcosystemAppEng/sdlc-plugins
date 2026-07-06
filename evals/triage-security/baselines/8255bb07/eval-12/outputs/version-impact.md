# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

h2 < 0.4.8 is vulnerable (from Step 1.5 cross-validated enrichment).
h2 >= 0.4.8 is fixed.

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.2.x (issue scope -- rhtpa-release.0.4.z)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |

**Scoped stream result: NO versions in 2.2.x are affected.**

All versions in the 2.2.x stream ship h2 >= 0.4.8, which is at or above the fix threshold.

### Stream 2.1.x (cross-stream check -- rhtpa-release.0.3.z)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (vulnerable) |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (vulnerable) |

**Cross-stream result: ALL versions in 2.1.x are affected.**

Both versions in the 2.1.x stream ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  Ecosystem: Cargo (Rust crate on crates.io)
  Lock file: Cargo.lock
  h2 is a dependency in the backend workspace

  Stream 2.1.x: h2 0.4.5 — vulnerable (< 0.4.8)
  Stream 2.2.x: h2 0.4.8+ — fixed (>= 0.4.8)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at latest released tag | Fixed? |
|--------|-----------|-----------------|---------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (at v0.4.12) | YES |
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (at v0.3.12) | NO |

The upstream fix PR is available at: https://github.com/hyperium/h2/pull/800

## Summary

- **Scoped stream (2.2.x)**: NOT affected. All 2.2.x versions ship h2 >= 0.4.8.
- **Cross-stream (2.1.x)**: AFFECTED. All 2.1.x versions ship h2 0.4.5 (< 0.4.8).

### Triage Outcome

For TC-8030 (scoped to 2.2.x): **Case C -- Close as Not a Bug**. No versions in the scoped stream ship a vulnerable version of h2. All 2.2.x versions include h2 0.4.8 or later, which is at or above the fix threshold.

Cross-stream impact: The 2.1.x stream IS affected and requires separate remediation (Case B -- cross-stream impact). Preemptive remediation tasks should be created for the 2.1.x stream if no stream-specific CVE Jira exists.
