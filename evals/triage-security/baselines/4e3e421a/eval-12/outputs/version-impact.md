# Step 2 – Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

Fix threshold: **h2 < 0.4.8 affected, >= 0.4.8 fixed** — the enriched, cross-validated value from
Step 1.5 (MITRE `lessThan 0.4.8`, OSV `fixed 0.4.8`). The Jira description ("versions prior to the
fix") was not usable as a threshold.

## 2.1 Matrix

Loaded both streams from `security-matrix-mock.md` (2.1.x → `rhtpa-release.0.3.z`,
2.2.x → `rhtpa-release.0.4.z`). Ecosystem: Cargo, repository `backend`, lock file `Cargo.lock`.

## 2.2 Development stream

No Jira version metadata (unreleased versions) is available in the fixture, so no separate
development stream could be identified. 2.2.x is the latest configured stream (no forward pointer);
its latest release 2.2.4 is used as the newest data point. (Interactive mode would query Jira for
unreleased `RHTPA` versions and check branch HEAD.)

## 2.3 / 2.4 Version impact table

Lock file data from simulated `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`.

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Backend tag | h2 | Affected? | Notes |
|--------|---------|-------------|----|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.4.8 | NO | 0.4.8 = fixed version (not < 0.4.8) |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.4.8 | NO | 0.4.8 = fixed version |
| 2.2.x | 2.2.2 | `v0.4.8` | — | NO | same as 2.2.1 (backend retag of 2.2.1) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.9 | NO | 0.4.9 > 0.4.8 |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.9 | NO | 0.4.9 > 0.4.8 |

Boundary note: 2.2.0 and 2.2.1 ship exactly h2 0.4.8. Because MITRE uses `lessThan` (exclusive)
and OSV marks 0.4.8 as `fixed`, 0.4.8 is **not** affected.

### Summary

- **In-scope stream 2.2.x (issue suffix `[rhtpa-2.2]`): NOT affected** — every 2.2.x release ships
  h2 >= 0.4.8.
- **Out-of-scope stream 2.1.x: AFFECTED** — 2.1.0 and 2.1.1 ship h2 0.4.5.

## 2.3.5 Dependency chain context (affected versions: 2.1.0, 2.1.1)

```
Dependency chain for h2 (2.1.x, tags v0.3.8 / v0.3.12):
  backend (workspace) → [HTTP stack, e.g. hyper / reqwest / tonic] → h2
  Type: most likely transitive (h2 is normally pulled in via hyper); exact
        chain not determinable from the fixture (only the lock-file version
        line was supplied, not the dependency graph or Cargo.toml)
  Profile: production (HTTP/2 server/client stack is a runtime dependency)
  Present in all versions of both streams; 2.2.x moved to h2 0.4.8+.
```

Limitation: the fixture provides only the resolved h2 version per tag. The remediation task must
direct the implementer to confirm direct vs transitive with `cargo tree -i h2` on `release/0.3.z`.

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | unknown (no fixture data; latest release tag `v0.3.12` ships 0.4.5) | Not confirmed → treat as NOT fixed |
| 2.2.x | Cargo | `release/0.4.z` | >= 0.4.9 (latest release tag `v0.4.12`) | YES (not affected) |

Remediation path for 2.1.x: upstream backport (bump h2 to >= 0.4.8 on `release/0.3.z`) followed by
downstream propagation in `rhtpa-release.0.3.z`. The fixed crate version 0.4.8 is already published
(2.2.x consumes it), so the backport is expected to be a semver-compatible `cargo update -p h2`
within the 0.4.x line.

## Steps 3–6 (Jira triage operations, recommendations only)

- **Step 3 – Affects Versions correction (scoped to 2.2.x)**: Current: `[RHTPA 2.2.0]` →
  Proposed: `[]` (no 2.2.x version is affected). PSIRT's RHTPA 2.2.0 is incorrect: 2.2.0 ships
  h2 0.4.8, which is the fixed version. The 2.1.x versions are not added here because the issue is
  scoped to 2.2.x; they belong to a 2.1.x sibling issue / preemptive remediation.
- **Step 4 – Siblings**: JQL (not executed) would be
  `project = TC AND labels = 'CVE-2026-48901' AND issuetype = 10024 AND key != TC-8030`.
  No sibling data in the fixture → assume no 2.1.x CVE Jira exists (must be verified before
  creating preemptive tasks).
- **Step 5 – Lifecycle**: lifecycle page not queried; 2.1.x assumed still supported (it is listed
  in the supportability matrix).
- **Step 6 – Already fixed**: no resolved siblings known.

Awaiting engineer confirmation of this table before Steps 3+ (eval: proceeding).
