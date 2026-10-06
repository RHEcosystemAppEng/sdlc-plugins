# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 external CVE data enrichment:
- **Affected range**: h2 < 0.4.8
- **Fixed version**: h2 >= 0.4.8
- **Source**: MITRE CVE API and OSV.dev (cross-validated, in agreement)

## Version Impact Table for CVE-2026-48901 (h2 < 0.4.8)

### Stream 2.2.x (issue-scoped stream: [rhtpa-2.2])

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (fixed) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (fixed) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 (fixed) |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 (fixed) |

**Result: No 2.2.x versions are affected.** All versions in the scoped stream ship h2 >= 0.4.8, which is at or above the fix threshold.

### Stream 2.1.x (cross-stream analysis)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (vulnerable) |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (vulnerable) |

**Result: All 2.1.x versions are affected.** Both versions ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context (Step 2.3.5)

For affected versions (2.1.x stream):

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (present in Cargo.lock)
  Ecosystem: Cargo (crates.io)
  Profile: production (h2 is a runtime dependency)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml on release/0.3.z branch
```

## Summary

| Stream | Versions Affected | Versions Not Affected | Overall |
|--------|-------------------|-----------------------|---------|
| 2.2.x (scoped) | 0 of 5 | 5 of 5 | NOT AFFECTED |
| 2.1.x (cross-stream) | 2 of 2 | 0 of 2 | AFFECTED |

### Triage Outcome

- **Scoped stream (2.2.x)**: No versions ship a vulnerable h2. Recommend **Case C: Close as Not a Bug** with VEX justification "Component not Present" (vulnerable version not present -- all versions ship h2 >= 0.4.8).
- **Cross-stream (2.1.x)**: All versions ship vulnerable h2 0.4.5. This is a **Case A: Cross-stream impact** finding. Since the issue is scoped to 2.2.x, preemptive remediation tasks should be created for the 2.1.x stream if no sibling CVE Jira exists for that stream.
