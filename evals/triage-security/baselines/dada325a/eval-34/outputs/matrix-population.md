# TC-8001 — On-Demand Matrix Population Review (2.1.x stream)

**Status: PROPOSAL NOT WRITTEN — image evidence UNRESOLVED — NOT VERIFIED**

Mode: interactive (on-demand population requested by engineer). Fullsend restrictions
do not apply, but the write gate in `version-impact-analysis.md` ("On-demand matrix
population", step 6, and "Local matrix write safety") blocks any write because one
image record has unresolved evidence.

No external tools were called (no Jira MCP, `git show`, registry API, cosign). All
evidence below is the synthetic release/image evidence supplied with the task.
No project files were modified.

## 1. Gap detection

Source snapshot: `security-matrix-mock.md`, Stream 1 `rhtpa-release.0.3.z` (2.1.x),
`Last-Updated: 2026-06-28T10:00:00Z`.

| Gap | Detail |
|---|---|
| Missing released-version row | 2.1.3 (build 0.3.15, released 2026-07-01) is absent from the Supportability Matrix — released after the matrix was last updated |
| Missing Container Images section | The stream has no `#### Container Images` section, so no `(Product Version, Component)` pairs are recorded at all |
| Missing component pair | `(2.1.3, api-rhel10)` is required by the supplied release evidence and has no row |
| Not covered by supplied evidence | Container Images rows for 2.1.0 and 2.1.1 (and any other 2.1.3 components) — no image evidence was supplied, so they cannot be proposed; see Section 6 |

Note: there is no 2.1.2 in the existing matrix or in the supplied evidence. No 2.1.2 row is
inferred; please confirm whether 2.1.2 was skipped or still needs evidence.

## 2. Collected evidence for (2.1.3, api-rhel10)

The values are kept separate, as step 3 requires.

| Field | Value | Source |
|---|---|---|
| Product Version | 2.1.3 | supplied release evidence |
| Build / Build Date | 0.3.15 / 2026-07-01 | supplied release evidence |
| backend source pin | `v0.3.15` | supplied release evidence (pinning method: `artifacts.lock.yaml`, unchanged) |
| Konflux Release Tag | `v0.3.15` | supplied release evidence |
| Resolved Release Commit SHA (from tag) | `abcdef0123456789abcdef0123456789abcdef01` | supplied tag resolution |
| Image Reference | `registry.example.test/trustify/api:2.1.3-rhel10` | supplied image evidence |
| Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | supplied image evidence |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` | supplied image evidence |
| `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` | supplied image evidence |

## 3. Revision-label comparison (kept out of the Container Images table)

| Product Version | Component | Resolved Release Commit SHA (tag `v0.3.15`) | Image `org.opencontainers.image.revision` | Result |
|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `abcdef0123456789abcdef0123456789abcdef01` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH — UNRESOLVED — NOT VERIFIED** |

The published image's revision label does not match the commit that release tag `v0.3.15`
resolves to. So I cannot show that image
`registry.example.test/trustify/api:2.1.3-rhel10@sha256:cccc…cccc` was built from the
`v0.3.15` source that the matrix would record. Neither SHA was substituted for the other or
inferred. Either value could be the wrong one: the tag may have moved, the image may have been
built from a different commit, or the label may be wrong.

## 4. Proposed matrix — NOT WRITTEN

This is shown for review only. It keeps the existing source columns, Source Pinning Method,
Ecosystem Mappings and Forward Pointer, and adds rows without replacing any. It will **not**
be written while the image row is unresolved.

```markdown
<!-- Last-Updated: 2026-06-28T10:00:00Z -->   <!-- unchanged: proposal NOT WRITTEN -->

# Stream 1: rhtpa-release.0.3.z (2.1.x stream)

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | PROPOSED — NOT WRITTEN |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

<!-- UNRESOLVED — NOT VERIFIED: (2.1.3, api-rhel10) revision label
     fedcba9876543210fedcba9876543210fedcba98 != resolved release SHA
     abcdef0123456789abcdef0123456789abcdef01 -->

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

## 5. Decision

- **Write: BLOCKED.** One image record is UNRESOLVED (the revision label does not match). Under
  step 6, no part of the proposal is written. That includes the 2.1.3 Supportability Matrix
  row, even though its source-pin evidence is internally consistent.
- **Current matrix:** left unchanged, including `Last-Updated: 2026-06-28T10:00:00Z`. Local
  matrix write safety was not reached, so no re-read/compare or create-if-absent write was
  attempted.
- **Engineer confirmation:** not requested yet. Confirmation is only valid once every image
  row is verified.
- **Effect on triage of TC-8001:** 2.1.3 cannot yet be treated as a verified matrix row for
  version impact analysis. If triage goes ahead before this is fixed, report 2.1.3 as
  *not verified / matrix coverage incomplete* and do not draw an affected or not-affected
  conclusion from unverified image evidence. Mock lock-file data for `v0.3.15` is also absent
  from the supplied evidence, so 2.1.3 dependency versions cannot be determined either way.

## 6. Corrected evidence requested from the engineer

1. **Fix the revision mismatch for (2.1.3, api-rhel10).** Provide one of:
   - confirmation that `v0.3.15` should resolve to
     `fedcba9876543210fedcba9876543210fedcba98` (that is, the tag resolution was wrong or the
     tag was moved), with the corrected tag-to-SHA resolution; or
   - a corrected image reference and digest whose `org.opencontainers.image.revision`
     equals `abcdef0123456789abcdef0123456789abcdef01`; or
   - an explanation of the build (for example, a rebuild from a different commit) and the
     correct release tag/commit for the published image.
2. **Complete the component inventory.** Confirm whether 2.1.3 ships other image components
   besides `api-rhel10` (for example, other platform variants). Each needs its own
   `(Product Version, Component)` evidence.
3. **Backfill existing versions.** Provide image evidence (release tag, resolved SHA, image
   reference, digest, CPE, revision label) for the 2.1.0 and 2.1.1 components, so the new
   Container Images section covers every released version.
4. **Confirm 2.1.2.** Was it skipped, or does it need a row?

Once corrected evidence verifies every image row, I will present the full updated proposal
again for confirmation. I will then write it only under Local matrix write safety (re-read and
compare against the snapshot above, merge or abort if the file changed), and update
`Last-Updated` only after the write succeeds.
