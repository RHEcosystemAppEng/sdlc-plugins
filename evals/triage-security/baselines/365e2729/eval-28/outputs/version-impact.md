# TC-8060 — Step 2: Version Impact Analysis

CVE-2026-99010, h2 < 0.4.5 (fixed in 0.4.5). Issue scope: **2.2.x** (`[rhtpa-2.2]`).

## 2.1 — Supportability matrix (2.2.x, rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem mapping: Cargo / backend / `Cargo.lock` / `git show <tag>:Cargo.lock` / upstream branch `release/0.4.z`.
Format validation: required sections present (Supportability Matrix, Ecosystem Mappings, Source Pinning Method, Forward Pointer) — pass.

## 2.2 — Development stream

Not determined: requires `getJiraIssueTypeMetaWithFields` (unreleased RHTPA versions), which was not
called in this eval. 2.2.x is the latest configured stream (no forward pointer). Development-HEAD
check of `release/0.4.z` is covered indirectly in 2.5 below.

## 2.3 / 2.4 — Version impact table

Lock-file evidence source: the simulated Step 2.3.5 Cargo.lock output in the issue fixture
(`Cargo.lock (versions 2.2.0 through 2.2.2)`: h2 0.4.4; `Cargo.lock (versions 2.2.3+)`: h2 0.4.5).

```
Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | backend tag | h2    | Affected? | Notes                                   |
|---------|-------------|-------|-----------|-----------------------------------------|
| 2.2.0   | v0.4.5      | 0.4.4 | YES       | via reqwest 0.12.5 -> hyper 1.4.1 -> h2 |
| 2.2.1   | v0.4.8      | 0.4.4 | YES       | via reqwest 0.12.5 -> hyper 1.4.1 -> h2 |
| 2.2.2   | v0.4.8      | —     | YES       | same as 2.2.1 (backend retag)           |
| 2.2.3   | v0.4.11     | 0.4.5 | NO        | fixed version shipped                   |
| 2.2.4   | v0.4.12     | 0.4.5 | NO        | fixed version shipped                   |
```

Summary for 2.2.x: **affected = 2.2.0, 2.2.1, 2.2.2**; not affected = 2.2.3, 2.2.4.

### Data discrepancy flagged for engineer review

The shared `security-matrix-mock.md` "h2 versions by tag" table lists different h2 versions for
the same tags (v0.4.5/v0.4.8 -> 0.4.8, v0.4.11/v0.4.12 -> 0.4.9, v0.3.x -> 0.4.5), all of which
would be >= 0.4.5 (NOT affected, implying Case C close). That conflicts with the CVE-specific
Cargo.lock evidence in the TC-8060 fixture (0.4.4 in 2.2.0–2.2.2). This analysis uses the
CVE-specific lock-file evidence from the issue fixture, which is what Step 2.3.5 was instructed to
simulate. In a real run this would be resolved by the actual `git show <tag>:Cargo.lock` output;
the engineer must confirm before Step 3.

### Cross-stream check (2.1.x, out of scope — for Case A only)

| Version | backend tag | h2 | Affected? | Notes |
|---------|-------------|----|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | NO | from matrix mock h2 table |
| 2.1.1 | v0.3.12 | 0.4.5 | NO | from matrix mock h2 table |

The issue fixture says the reqwest -> hyper -> h2 chain is present since 2.1.0, but gives no 2.1.x
h2 version; the only available 2.1.x data (matrix mock) shows 0.4.5 = fixed. No cross-stream impact
-> Case A not triggered.

## 2.3.5 — Dependency chain context

```
Dependency chain for h2:
  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency in [dependencies])

Manifest evidence (backend/Cargo.toml, all versions):
  [dependencies]
  reqwest = { version = "0.12", features = ["json"] }
  h2 is NOT a direct dependency.

Lock evidence (affected 2.2.0–2.2.2):
  reqwest 0.12.5 -> hyper 1.4.1 -> h2 0.4.4
Lock evidence (fixed 2.2.3+):
  h2 0.4.5

First appeared: 2.1.0 (initial project setup — reqwest has always depended on hyper/h2)
Present in: all versions (vulnerable range only in 2.2.0–2.2.2)

Dependency scope: production runtime dependency — not dev/build-only, not feature-gated
  -> standard remediation, no `dev-dependency` label, no priority override, no VEX option.

Remediation (two-tier):
  1. Preferred: bump the direct dependency (reqwest, and with it hyper) so the resolved
     transitive closure contains h2 >= 0.4.5 (e.g. `cargo update -p reqwest` / `cargo update -p hyper`;
     h2 0.4.5 is semver-compatible with hyper 1.4.x's `h2 = "0.4"` requirement, so
     `cargo update -p h2` also resolves it without a manifest change).
  2. Fallback: pin the transitive dep directly — `cargo add h2@0.4.5` in backend/Cargo.toml —
     if the reqwest/hyper bump is not viable (breaking API change, or an intermediate crate pins h2 < 0.4.5).
     May require coordination with reqwest/hyper maintainers if they pin the vulnerable version.
```

## 2.5 — Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | not read directly (no `git show` in eval); tags v0.4.11 and v0.4.12 cut from this line ship h2 0.4.5 | YES (inferred from released tags; confirm at HEAD) |

Implication: the fix is already on the upstream branch and already shipped in 2.2.3 / 2.2.4. The
dependency-bump variant applies (not an upstream backport). See remediation.md.

## Step 3 — Affects Versions correction (proposed, not executed)

| | Versions |
|---|---|
| Current (PSIRT) | RHTPA 2.2.0 |
| Proposed (lock-file evidence) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Change | add RHTPA 2.2.1, RHTPA 2.2.2 |

Version IDs to be discovered dynamically via `getJiraIssueTypeMetaWithFields`; correction comment
must include the Comment Footnote.

## Steps 4–7 (not executable in eval — require Jira/lifecycle access)

- Step 4 duplicate/sibling search (JQL on label CVE-2026-99010): not run; no siblings known.
  4.3 cross-CVE overlap skipped (Upstream Affected Component field not configured).
- Step 5 lifecycle: product pages not queried; 2.2.0–2.2.2 assumed in support pending check.
- Step 6 already-fixed: no resolved siblings known. Note: 2.2.3+ already ship the fix.
- Step 7 concurrent triage: skipped (Upstream Affected Component field not configured).
- Step 7.5 release Jira orchestration: not queried; release Epic/Task linkage left as placeholders.
