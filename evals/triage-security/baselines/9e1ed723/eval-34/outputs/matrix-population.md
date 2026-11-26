# TC-8001 — On-Demand Matrix Population Review (2.1.x stream)

**Skill:** triage-security (interactive mode; `FULLSEND_OUTPUT_DIR` absent)
**Procedure:** SKILL.md Step 0.3 (staleness) → Step 2.1 / 2.1.1 → Step 2.1 "On-demand matrix population" + "Local matrix write safety" (`version-impact-analysis.md`)
**Evidence source:** only the synthetic release/image evidence supplied with the task. No Jira MCP, `git show`, registry API, cosign, or other external calls were made.

---

## Decision

**UNRESOLVED — NOT VERIFIED. The proposal is NOT WRITTEN.**

- The `(2.1.3, api-rhel10)` image record has a **revision-label mismatch**. Its
  `org.opencontainers.image.revision` label (`fedcba9876543210fedcba9876543210fedcba98`)
  does not match the full SHA that the `v0.3.15` release tag resolves to
  (`abcdef0123456789abcdef0123456789abcdef01`).
- Step 2.1 item 4 says any revision-label mismatch is unresolved evidence. Item 6 says no part
  of the proposal may be written while any image row is unresolved.
- The current 2.1.x `security-matrix.md` and its
  `<!-- Last-Updated: 2026-06-28T10:00:00Z -->` timestamp stay **unchanged**.
- Neither SHA was inferred or substituted, and the image was not marked verified.
- Version impact analysis for TC-8001 (Step 2.3 onward) is **paused** until the engineer
  sends corrected evidence (see "Corrected evidence requested" below). The 2.1.x matrix is
  missing a released version, so running impact analysis now would break the rule to
  check every supported version.

---

## 1. Pre-checks

### Step 0 — Configuration (claude-md-security-config.md)

| Item | Value | Status |
|---|---|---|
| Project key / Cloud ID | TC / 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | present |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | present |
| Jira version prefix | RHTPA | present |
| Vulnerability issue type ID | 10024 | present |
| Component label pattern | `pscomponent:` | present |
| VEX Justification field | customfield_12345 | present |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z | present |
| Source Repositories | rhtpa-backend (no Deployment Context column → defaults to `upstream`) | present |

Observation: the Version Streams table has no **Security Matrix Path** column. For this
eval the supplied `security-matrix-mock.md`, which holds both streams, is used as the
matrix source.

### Step 0.3 — Staleness

- `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-23, so the matrix is **148 days
  old**, well past the 14-day threshold.
- The engineer has already asked for on-demand population, which is the "Refresh now" option.
  The refresh below targets the 2.1.x stream, where the gap was reported.

### Step 2.1.1 — Format validation (2.1.x section)

| Check | Result |
|---|---|
| `## Supportability Matrix` | present |
| `### Source Pinning Method` | present (`backend`: `artifacts.lock.yaml`) |
| `## Ecosystem Mappings` columns | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch`, which matches the template |
| `## Forward Pointer` | present (`2.2.x`) |
| Table parsability | both tables valid |
| **Result** | **Pass**. No repairs proposed. |

---

## 2. Gap analysis: required vs existing `(Product Version, Component)` pairs

| Item | Existing matrix | Release/image evidence | Gap |
|---|---|---|---|
| Supportability row 2.1.3 | absent (only 2.1.0, 2.1.1) | 2.1.3 / build 0.3.15 / 2026-07-01 / backend `v0.3.15` | **missing released-version row** |
| `#### Container Images` section | **absent** | — | **section missing** |
| `(2.1.3, api-rhel10)` | absent | supplied (see §3) | missing pair, and its evidence is unresolved |
| `(2.1.0, *)`, `(2.1.1, *)` image rows | absent | **no image evidence supplied** | missing pairs, unresolved (no evidence) |

Note on 2.1.2: no 2.1.2 release evidence was supplied. The skill does not assume whether 2.1.2
exists. Item 1 of population (Konflux tag/branch history) would normally settle this, but
that query is out of scope here. **2.1.2 status is UNRESOLVED.** The engineer must confirm
whether a 2.1.2 release exists, for example as a skipped or unshipped version number.

---

## 3. Image evidence record — `(2.1.3, api-rhel10)`

Each value is kept separate, exactly as supplied:

| Field | Value |
|---|---|
| Product Version | 2.1.3 |
| Component | api-rhel10 |
| Konflux Release Tag | `v0.3.15` |
| Resolved Release Commit SHA (from tag) | `abcdef0123456789abcdef0123456789abcdef01` |
| Image Reference | `registry.example.test/trustify/api:2.1.3-rhel10` |
| Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |
| `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` |

### Revision-label comparison (reported separately from the Container Images table)

| Product Version | Component | Resolved Release Commit SHA (`v0.3.15`) | Image revision label | Match? | Status |
|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `abcdef0123456789abcdef0123456789abcdef01` | `fedcba9876543210fedcba9876543210fedcba98` | **NO** | **UNRESOLVED — NOT VERIFIED** |

**Conflict:** the published image says it was built from commit `fedcba98…`, but the 2.1.3
release tag `v0.3.15` resolves to `abcdef01…`. Possible causes include a mis-tagged release,
an image rebuilt from a different commit, a wrong image reference, or a moved tag. The skill
does not choose between these explanations. Neither SHA may stand in for the other.
Because it is unclear which source was shipped in this image, lock-file results at `v0.3.15`
cannot yet be assumed to describe the shipped `api-rhel10` image.

Other evidence for this record (tag resolution, image reference, digest, CPE) is present. The
only blocker for this record is the mismatch.

---

## 4. Proposed 2.1.x matrix (NOT WRITTEN, for review only)

> **NOT WRITTEN.** This proposal includes an unresolved image row and missing image
> evidence for 2.1.0/2.1.1. Under Step 2.1 item 6, no part of it may be written, including
> the supportability row. The `Last-Updated` timestamp is not changed.

Existing source columns, Source Pinning Method, Ecosystem Mappings, and Forward Pointer are
kept as they are. The only additions are the 2.1.3 supportability row and the Container
Images section.

```markdown
<!-- Last-Updated: 2026-06-28T10:00:00Z -->   <- unchanged; would be updated only after a permitted write

# Stream 1: rhtpa-release.0.3.z (2.1.x stream)

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | PROPOSED — image evidence unresolved (revision-label mismatch); NOT WRITTEN |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.0 | UNRESOLVED — NOT VERIFIED (no image evidence supplied) | `v0.3.8` | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED |
| 2.1.1 | UNRESOLVED — NOT VERIFIED (no image evidence supplied) | `v0.3.12` | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED |
| 2.1.3 | api-rhel10 — UNRESOLVED — NOT VERIFIED (revision label ≠ release SHA) | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | — | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | — |

## Forward Pointer

Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
```

The 2.2.x stream is not changed by this proposal.

---

## 5. Write-safety status

| Step | Status |
|---|---|
| Source snapshot retained | Yes. The exact current `security-matrix-mock.md` contents (Last-Updated 2026-06-28T10:00:00Z) were kept as the proposal's snapshot. |
| Engineer confirmation of the complete proposal | Not requested. Confirmation is only possible once every image row is verified. |
| Final re-read/compare, create-if-absent, merge-or-abort | Not reached. Writing is blocked by unresolved evidence. |
| File written | **No.** No project file was modified. |
| `Last-Updated` updated | **No.** |

---

## 6. Corrected evidence requested from the engineer

1. **`(2.1.3, api-rhel10)` revision conflict.** Provide one of the following:
   - the correct published image reference and digest, whose
     `org.opencontainers.image.revision` equals `abcdef0123456789abcdef0123456789abcdef01`, or
   - corrected release-tag evidence showing that `v0.3.15` (the tag the 2.1.3 build is
     pinned to) resolves to `fedcba9876543210fedcba9876543210fedcba98`, along with an
     explanation of the tag move, or
   - confirmation that 2.1.3 is pinned to a different tag/commit, with its full resolved SHA.
2. **Other 2.1.3 components.** Confirm whether `api-rhel10` is the only shipped image for 2.1.3.
   If not, supply tag, resolved SHA, image reference, digest, CPE, and revision label for each
   remaining `(2.1.3, <component>)` pair.
3. **2.1.0 and 2.1.1 Container Images.** Supply the same evidence for every shipped component of
   these released versions. The Container Images section is currently missing for them.
4. **2.1.2.** Confirm whether a 2.1.2 release exists. If it does, supply its build, date,
   backend pin, retag status, and image evidence.

Once every image row is verified, the skill will present the complete updated proposal for
confirmation. It will write only through Local matrix write safety, update `Last-Updated`
only after a successful write, and then resume TC-8001 at Step 2.2/2.3 with 2.1.3 included.

---

## 7. Jira actions

None. Triage of TC-8001 stopped before Step 3. No Affects Versions change, comment, link,
transition, or remediation task is proposed yet, and no Jira tool was called.
