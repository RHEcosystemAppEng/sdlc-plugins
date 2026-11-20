# Step 2 – Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

**Fix threshold used:** h2 `< 0.4.8` is affected and `0.4.8` is fixed. This is the enriched,
cross-validated threshold from Step 1.5 (MITRE `lessThan 0.4.8` and OSV `fixed 0.4.8`). The
Jira description's "versions prior to the fix" was not used.

## 2.1 – Supportability matrix (from security-matrix-mock.md)

- Stream 2.1.x (`rhtpa-release.0.3.z`): 2.1.0 → backend `v0.3.8`, 2.1.1 → backend `v0.3.12`
- Stream 2.2.x (`rhtpa-release.0.4.z`): 2.2.0 → `v0.4.5`, 2.2.1 → `v0.4.8`, 2.2.2 → `v0.4.8` (backend retag of 2.2.1), 2.2.3 → `v0.4.11`, 2.2.4 → `v0.4.12`
- Ecosystem mapping (both streams): Cargo, repo `backend`, `Cargo.lock`, `git show <tag>:Cargo.lock`
- Format: required sections are present (Supportability Matrix, Source Pinning Method, Ecosystem Mappings, Forward Pointer). Validation passed.
- Staleness (Step 0.3): Last-Updated is 2026-06-28. On 2026-11-20 that is more than 14 days old. In interactive mode the engineer would get the Refresh / Proceed / Stop options. For this eval, triage proceeds with the provided matrix.

## 2.2 – Development stream

No Jira version metadata (unreleased versions) is in the fixture, so no separate development
stream could be identified. 2.2.x is the latest stream (no forward pointer). Its upstream branch HEAD
(`release/0.4.z`) is not in the mock data, so no dev-HEAD row is reported. No value was fabricated.

## 2.3 – Dependency versions (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`)

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | Stream | Backend tag | h2 | Affected? | Notes |
|---------|--------|-------------|----|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8`  | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5`  | 0.4.8 | NO | 0.4.8 = fixed version (not < 0.4.8) |
| 2.2.1 | 2.2.x | `v0.4.8`  | 0.4.8 | NO | 0.4.8 = fixed version |
| 2.2.2 | 2.2.x | `v0.4.8`  | —     | NO | same as 2.2.1 (backend retag, lock file check skipped) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | 0.4.9 > 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | 0.4.9 > 0.4.8 |

### Summary

- **Issue stream 2.2.x (scope of TC-8030): NOT affected.** Every 2.2.x release ships h2 >= 0.4.8.
  The PSIRT-assigned Affects Version `RHTPA 2.2.0` is wrong: 2.2.0 ships h2 0.4.8, which is the fixed version.
- **Stream 2.1.x: AFFECTED.** 2.1.0 and 2.1.1 ship h2 0.4.5. This is a cross-stream impact outside this issue's scope.

## 2.3.5 – Dependency chain context (2.1.x)

```
Dependency chain for h2:
  backend (workspace) → ... → h2 0.4.5
  Type: not determinable from the provided mock data (only Cargo.lock version lines are given;
        Cargo.toml / full lock graph not available). h2 is commonly pulled in transitively via
        hyper / reqwest / tonic. The engineer must verify with `cargo tree -i h2` on v0.3.12.
  Profile: assumed production (HTTP/2 stack), to be verified. There is no evidence of a dev-only scope.
  Introduction point: h2 is present in all 2.1.x and 2.2.x builds. It was upgraded 0.4.5 → 0.4.8 between
                      2.1.1 (v0.3.12) and 2.2.0 (v0.4.5).
```

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | not available in mock data | UNKNOWN |
| 2.2.x | Cargo | `release/0.4.z` | not available (latest release v0.4.12 has 0.4.9) | n/a (stream not affected) |

Because no evidence shows that `release/0.3.z` already ships h2 >= 0.4.8, the 2.1.x remediation
uses the **upstream backport** path, not the dependency-bump variant. If the engineer confirms
that `release/0.3.z` HEAD already has h2 >= 0.4.8, switch to the dependency-bump template.

## Step 3 – Affects Versions correction (proposed, not executed)

Scoped to stream 2.2.x per issue suffix:

`Current: [RHTPA 2.2.0] → Proposed: []` (no 2.2.x version ships a vulnerable h2)

Because nothing in scope is affected, the 2.2.0 value is removed and the issue is closed (see remediation.md).
The 2.1.x versions (RHTPA 2.1.0, 2.1.1) belong to a 2.1.x sibling or companion issue, not to TC-8030.

## Step 4 – Siblings

There is no sibling search data in the fixture, so no 2.1.x companion Vulnerability issue for CVE-2026-48901
is known. 2.1.x is therefore treated as a stream without its own CVE Jira, and preemptive tasks apply.

## Steps 5–7

- Step 5 (lifecycle): no lifecycle data in the fixture. 2.1.x is assumed supported because it is in the Version Streams table. Verify on the product pages.
- Step 6 (already fixed): no resolved siblings, so this check does not apply.
- Step 7 (concurrent triage): skipped because the Upstream Affected Component field is not configured.
