# Step 2 – Version Impact Analysis: TC-8050 (CVE-2026-99001, criterion < 0.5.2)

## 2.1 – Supportability matrix

Loaded both streams from `security-matrix-mock.md` (Last-Updated 2026-06-28T10:00:00Z).
Format validation: both streams contain Supportability Matrix, Source Pinning Method,
Ecosystem Mappings (expected columns `Ecosystem | Repository | Lock File | Check Command |
Upstream Branch`), and Forward Pointer → **Pass**.

## 2.2 – Development stream

No Jira version metadata (unreleased RHTPA versions) is available in this eval — Jira was
not queried. The 2.2.x stream is the latest stream ("no forward pointer"). Development
stream HEAD could not be checked; noted as **not determined** rather than assumed.

## 2.3 – Dependency versions at pinned commits

Lock-file data taken from the mock `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'`
output in the fixture. Compared against threshold < 0.5.2 (Jira description; external
enrichment unavailable).

### Version Impact for CVE-2026-99001 (criterion < 0.5.2) — issue scope: 2.2.x

| Version | Build | backend tag | criterion | Affected? | Notes |
|---------|-------|-------------|-----------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.5.1 | YES | dev-dependency only (not shipped) |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.5.1 | YES | dev-dependency only (not shipped) |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | YES | same as 2.2.1 (backend retag of 2.2.1) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.5.1 | YES | dev-dependency only (not shipped) |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.5.1 | YES | dev-dependency only (not shipped) |
| 2.2.x dev (branch HEAD) | — | `release/0.4.z` HEAD | not determined | not determined | No HEAD lock data / Jira unreleased versions available in eval |

### Cross-stream (outside issue scope — for Case A reporting only)

| Version | Build | backend tag | criterion | Affected? | Notes |
|---------|-------|-------------|-----------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.5.1 | YES | dev-dependency only (not shipped) |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.5.1 | YES | dev-dependency only (not shipped) |

All released versions in both streams ship criterion 0.5.1 in `Cargo.lock`, which is
inside the affected range (< 0.5.2). Lock-file presence alone means "affected" per
Step 2.3, but see the dependency chain context below: the crate is not part of production
builds.

## 2.3.5 – Dependency chain context

```
Dependency chain for criterion:
  backend (workspace) → criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds — used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions (2.1.0 – 2.2.4)

Manifest evidence (backend/Cargo.toml, all versions):
  [dev-dependencies]
  criterion = "0.5.1"

Remediation: bump criterion to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
and Cargo.lock (direct dependency — simple version bump, no transitive pinning needed).
```

### Dependency scope decision tree result

- Classification: **Dev-only dependency** (Cargo `[dev-dependencies]` — tests/benchmarks
  only; NOT shipped in the production binary or container image).
- Risk: no production exposure; residual **supply chain risk** only (the path traversal
  could be triggered only when running benchmarks in a dev/CI environment).
- Handling: **still create remediation tasks**, with:
  - `dev-dependency` label added to each remediation task
  - Priority overridden to **Normal** regardless of CVE severity (CVSS 5.3 Medium) — the
    CVE priority is not inherited
  - Description note: "This dependency is dev/build-only and is not shipped in
    production. Remediation priority is Normal (supply chain risk only)."
- Not feature-gated → the VEX "Vulnerable Code not in Execute Path" prompt does not apply.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.2.x | Cargo | backend | `release/0.4.z` | not available (no `git show` in eval) | Not confirmed |
| 2.1.x (cross-stream) | Cargo | backend | `release/0.3.z` | not available | Not confirmed |

Because the upstream branch is not confirmed to ship criterion >= 0.5.2, the remediation
path is **upstream backport (dependency bump PR on `release/0.4.z`) + downstream
propagation** in the Konflux release repo, not the "fix available" bump variant.

## Step 3 preview – Affects Versions correction (scoped to 2.2.x)

```
Current:  [RHTPA 2.2.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, RHTPA 2.2.3, RHTPA 2.2.4]
```

PSIRT version is correct but incomplete. 2.1.x versions are excluded (belong to a
sibling/companion issue for the 2.1.x stream). Jira version IDs would be discovered via
`getJiraIssueTypeMetaWithFields` (not queried in this eval). Correction would be applied
only after engineer confirmation, with a comment including the Comment Footnote.

## Steps 4–7 notes (not executed against Jira)

- Step 4: sibling search for `labels = CVE-2026-99001` not run; a 2.1.x companion issue
  could not be confirmed. Step 4.3 (cross-CVE overlap) skipped — Upstream Affected
  Component field not configured.
- Step 5: lifecycle not queried; all 2.2.x versions assumed in support pending check of
  https://access.example.com/product-life-cycle/rhtpa.
- Step 6: no resolved siblings known → not already fixed.
- Step 7: skipped — Upstream Affected Component field not configured.
- Step 7.5: release Epic/Task ("RHTPA <version> Release Tasks" / "RHTPA <version> CVE
  triage") would be found or created with individual confirmation; not queried here.

Outcome: 2.2.x is affected (dev-only) → **Case B** (create remediation tasks for 2.2.x),
plus **Case A** cross-stream impact for 2.1.x.
