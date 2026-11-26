# Step 2 – Version Impact Analysis: TC-8004 (CVE-2026-33501, h2 < 0.4.8)

Evidence source: the "h2 versions by tag" table in `security-matrix-mock.md`. In this
eval it stands in for the output of
`git show <tag>:Cargo.lock | grep -A2 'name = "h2"'` at each pinned backend tag. No
values were inferred.

## 2.1 – Supportability matrix (all streams enumerated from Version Streams)

| Stream | Konflux release repo | Versions | Cargo repo / upstream branch |
|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`) | backend / `release/0.3.z` |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (`v0.4.8`, retag of 2.2.1), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`) | backend / `release/0.4.z` |

Format validation (2.1.1): both streams contain Supportability Matrix, Source Pinning
Method, Ecosystem Mappings (expected columns) and Forward Pointer. Result: Pass.

## 2.2 – Development stream

The development stream is found through unreleased `RHTPA` Jira versions
(`getJiraIssueTypeMetaWithFields`). Jira was not called in this eval, so no unreleased
version or dev-stream branch-HEAD evidence is available. 2.2.x is the latest
configured stream (it has no forward pointer). **The dev-stream row is left out. In a
live run, it must be checked at branch HEAD before the triage is finalized.**

## 2.4 – Version impact table

```
Version Impact for CVE-2026-33501 (h2 < 0.4.8):
```

| Stream | Version | Backend tag | h2 | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.4.8 | NO | 0.4.8 is the fixed version (not < 0.4.8) |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.4.8 | NO | fixed version |
| 2.2.x | 2.2.2 | `v0.4.8` | — | NO | same as 2.2.1 (backend retag; lock check skipped, result carried forward) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.9 | NO | > 0.4.8 |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.9 | NO | > 0.4.8 |

### Per-stream summary (mixed impact)

| Stream | Affected versions | Not-affected versions | Stream verdict |
|---|---|---|---|
| **2.1.x** | 2.1.0, 2.1.1 | — | **AFFECTED.** Every released 2.1.x version ships h2 0.4.5. |
| **2.2.x** | — | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NOT AFFECTED.** Every 2.2.x version, starting with 2.2.0, ships h2 >= 0.4.8. |

PSIRT's Affects Versions include **RHTPA 2.2.0**, but lock file evidence shows 2.2.0
already ships the patched h2 0.4.8. PSIRT also leaves out **RHTPA 2.1.1**, which is
affected.

## 2.3.5 – Dependency chain context (2.1.x)

```
Dependency chain for h2 (Cargo):
  Present in: 2.1.0, 2.1.1 at h2 0.4.5 (backend tags v0.3.8, v0.3.12)
  Bumped to 0.4.8 by: 2.2.0 (backend v0.4.5), so the 2.2.x line already carries the fix
  Type: NOT DETERMINED. The mock evidence only has the resolved Cargo.lock version,
        not the dependency graph or Cargo.toml manifests. h2 is usually pulled in
        transitively (e.g. backend -> hyper/reqwest/tonic -> h2), but this needs
        verification with `git show v0.3.12:Cargo.lock` / `cargo tree -i h2`.
  Profile: assumed production (h2 is an HTTP/2 runtime library). No dev-only or
           feature-gated evidence, so the dev-dependency handling does not apply.
```

Remediation implication: if h2 is transitive, use the two-tier approach (bump the
direct dependency that pulls in h2; otherwise pin `h2@0.4.8` with `cargo add`). The
remediation task lists both approaches.

## 2.5 – Upstream fix status (affected streams only)

| Stream | Ecosystem | Repository | Upstream Branch | h2 at HEAD | Fixed? |
|---|---|---|---|---|---|
| 2.1.x | Cargo | backend (rhtpa-backend) | `release/0.3.z` | unknown (`git show release/0.3.z:Cargo.lock` not run in eval) | **Not confirmed** |

The latest 2.1.x release tag (`v0.3.12`) still ships h2 0.4.5, and there is no evidence
that `release/0.3.z` has been fixed. The **upstream backport + downstream propagation**
path is therefore used for 2.1.x. If a live check shows `release/0.3.z` HEAD already
has h2 >= 0.4.8, switch the first task to the dependency-bump variant.

2.2.x is not affected, so no upstream fix check is needed there.

## Steps 4–7 results (feeding Steps 3 and 8)

| Step | Result |
|---|---|
| 4 – Sibling search (`labels = 'CVE-2026-33501' AND issuetype = 10024 AND key != TC-8004`) | Empty (as stated by the eval). No duplicates, no companion trackers, no Related links. |
| 4.3 – Cross-CVE overlap | Skipped (Upstream Affected Component field not configured). |
| 4.4 – Preemptive task reconciliation (`labels = 'security-preemptive' AND labels = 'CVE-2026-33501'`) | Assumed empty (no siblings or prior triages). No reconciliation needed. |
| 5 – Lifecycle | Product pages not fetched in eval. 2.1.x is assumed supported. **Verify in a live run**: if 2.1.x is EOL, close as Won't Do instead of remediating. |
| 6 – Already fixed | No resolved siblings, so it does not apply. |
| 7 – Concurrent triage | Skipped (Upstream Affected Component field not configured). |
