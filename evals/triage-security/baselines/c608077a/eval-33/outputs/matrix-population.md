# Matrix Population — TC-8001 (stream 2.1.x, interactive on-demand path)

**Result: NOT WRITTEN — write aborted under Local matrix write safety.**
The target `security-matrix.md` (2.1.x) changed between the snapshot and the write, so
the user's earlier confirmation no longer applies. The current file and its
`Last-Updated` timestamp (`2026-10-26T09:15:00Z`, set by the concurrent run) were left
as they are.

Mode: interactive (not Fullsend). Only the synthetic data in the task was used. No Jira
MCP, `git show`, registry, or cosign calls were made, and no project file was changed.

---

## 1. Source snapshot (what the proposal was built from)

The 2.1.x stream from `security-matrix-mock.md`, plus the extra state given in the task:

- `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`
- Supportability Matrix rows: `2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8`, `2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12`, **`2.1.2 | 0.3.14 | 2026-06-25 | v0.3.14`**
- Container Images section exists, with one verified row: `(2.1.2, api-rhel9)`
- Source Pinning Method (backend: `artifacts.lock.yaml`), Ecosystem Mappings (Cargo/backend `release/0.3.z`; RPM `rpms.lock.yaml`), Forward Pointer (`2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`)

Notes from Step 0.3 and Step 2.1.1:
- **Staleness (Step 0.3):** at the snapshot, Last-Updated `2026-06-28` was 145 days
  before today (2026-11-20), well past the 14-day threshold. The concurrent value
  `2026-10-26` is 25 days old, which is still stale.
- **Format validation (Step 2.1.1):** Pass. All required headings are present, the
  Ecosystem Mappings columns match the template, and both tables parse. No
  auto-repair is needed.

## 2. Why population ran

The **on-demand trigger** in `version-impact-analysis.md` > *On-demand matrix population*
runs population when a stream "is missing any required component pair — **even when the
section and other rows already exist**". Here the Container Images section and the
`(2.1.2, api-rhel9)` row exist, but the required pair **`(2.1.2, api-rhel10)` is missing**.
That alone triggers population. A section that already exists does not stop it.

## 3. Evidence for the missing image record

Each record is keyed by its exact `(Product Version, Component)` pair, so rhel9 and
rhel10 stay separate.

| Field | (2.1.2, api-rhel10) |
|---|---|
| Konflux Release Tag | `v0.3.14` |
| Resolved Release Commit SHA | `0123456789abcdef0123456789abcdef01234567` |
| Image Reference | `registry.example.test/trustify/api:2.1.2-rhel10` |
| Image Digest | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |

### Revision-label comparisons (reported separately from the table, as required)

| Pair | `org.opencontainers.image.revision` | Resolved release SHA | Result |
|---|---|---|---|
| (2.1.2, api-rhel9) | `0123456789abcdef0123456789abcdef01234567` (matching) | `0123456789abcdef0123456789abcdef01234567` | MATCH — VERIFIED (existing row) |
| (2.1.2, api-rhel10) | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH — VERIFIED |

Every required field is present and no label mismatches, so no row is
UNRESOLVED. The proposal was allowed to go to the confirmation step.

## 4. Proposal the user confirmed (against the snapshot) — NOT WRITTEN

```markdown
<!-- Last-Updated: (to be set only after a permitted write succeeds) -->

# Stream 1: rhtpa-release.0.3.z (2.1.x stream)

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.2 | 0.3.14 | 2026-06-25 | `v0.3.14` | |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.2 | api-rhel9 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |
| 2.1.2 | api-rhel10 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |

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

The existing columns, Source Pinning Method, Ecosystem Mappings, Forward Pointer, and the
`(2.1.2, api-rhel9)` row are kept unchanged. The only addition is the
`(2.1.2, api-rhel10)` row.

## 5. Final write-safety check — target changed, write aborted

Under Local matrix write safety step 2, the target was re-read immediately before the
write and compared in full with the snapshot:

| Item | Snapshot | Current target | Changed? |
|---|---|---|---|
| Last-Updated | `2026-06-28T10:00:00Z` | `2026-10-26T09:15:00Z` | **Yes** |
| Container Images row `(2.1.1, api-rhel10)` marked `CONCURRENT-ROW-KEEP` | absent | present, verified | **Yes** |

What happened, rule by rule:
- **Step 2:** "Do not treat a previous read or user confirmation as current after time
  has passed." The earlier confirmation covered the snapshot, not this file.
- **Step 4:** the target existed and changed, so **the current file is kept**. Writing
  the confirmed proposal would overwrite the stale snapshot and **delete the
  `CONCURRENT-ROW-KEEP` row**. That is not allowed.
- **Merge option:** the rule allows a merge only when *the full current contents and all
  merge data are available*, and then only after showing the complete merged matrix and
  getting **fresh confirmation**. Neither condition is met here:
  1. I only have a description of the concurrent change ("a verified 2.1.1/api-rhel10 row
     marked CONCURRENT-ROW-KEEP"). I do not have its tag, SHA, image reference, digest, or
     CPE, so I cannot reproduce the full current file. A merged matrix would need
     placeholders, and the rule forbids that ("Never use placeholders, call an incomplete
     merge complete, or overwrite a stale snapshot").
  2. The user said "My earlier confirmation still stands; write without another review."
     That is a request to skip the fresh confirmation step 4 requires. An earlier
     confirmation cannot stand in for a review of the merged matrix.
- **Step 5:** because the write was aborted, the current file and its
  `Last-Updated: 2026-10-26T09:15:00Z` stay unchanged. I did not set a new timestamp.

### Message to the engineer

> The 2.1.x `security-matrix.md` changed after you confirmed the proposal. Another
> triage-security run set Last-Updated to 2026-10-26T09:15:00Z and added a verified
> `(2.1.1, api-rhel10)` row marked CONCURRENT-ROW-KEEP. I did **not** write: your earlier
> confirmation was for the old snapshot, and the write-safety rules don't let me skip a
> fresh review after the file has changed. To continue, please send the **full current
> file**. I'll then show you the complete merged matrix: the current file plus the
> `(2.1.2, api-rhel10)` row, with the CONCURRENT-ROW-KEEP row kept. I'll write it only
> after you confirm that merged version.

The expected merge, once the full file is provided: take the current file exactly as it
is, including the concurrent row and its timestamp, and add only the verified
`(2.1.2, api-rhel10)` row from Section 3. Set `Last-Updated` only after that write
succeeds.

## 6. Written skill rules vs. general judgment

**Written rules** (in `plugins/sdlc-workflow/skills/triage-security/version-impact-analysis.md`):
- **On-demand trigger:** population runs when any required `(Product Version, Component)`
  pair is missing, "even when the section and other rows already exist". This is why the
  missing `(2.1.2, api-rhel10)` row triggered population.
- **Evidence:** keep tag, SHA, image reference, digest, and CPE as separate fields;
  report the revision-label comparison separately; any missing or mismatched evidence
  means UNRESOLVED — NOT VERIFIED and no write. Here everything was verified.
- **Scope of the write-safety rule:** "This procedure applies to every local
  `security-matrix.md` write: saving a Konflux fallback copy, applying Step 2.1.1 format
  auto-repairs, and on-demand population." Population step 6 says it again: the shared
  procedure "performs the final re-read/compare, create-if-absent check, and
  merge-or-abort decision for this write path as well as fallback saves and repairs."
  - **Fallback saves:** yes. "Do not write directly from the fallback branch."
  - **Format auto-repairs:** yes. "Before writing an auto-repair, apply Local matrix
    write safety." (Not used in this run; validation passed.)
  - **Population writes:** yes. This is the rule that aborted this write.
- Step 2: a previous confirmation does not count as current once time has passed.
- Step 4: keep a changed target; merge only with full contents and fresh confirmation;
  no placeholders; otherwise abort and ask for the full current file.
- Step 5: update `Last-Updated` only after a permitted write. An aborted write leaves
  the file and timestamp unchanged.
- Only `security-matrix.md` may be written, and only interactively. Fullsend forbids it.

**General judgment** (not stated word for word in the skill):
- Treating "My earlier confirmation still stands" as **not** meeting the fresh-confirmation
  requirement. The skill says to obtain fresh confirmation of the *merged* matrix. I read
  a blanket waiver given before any merged matrix was shown as not meeting that.
- Deciding that a one-line description of the concurrent row ("verified … marked
  CONCURRENT-ROW-KEEP") is not the "full current contents". Its field values are unknown,
  so writing it would mean using placeholders.
- Labelling the new Container Images heading `####`, as the template does, and keeping
  the fixture's `Version` column header unchanged (template field names are used only for
  the new Container Images table).
- Pointing out that the concurrent timestamp is also stale (25 days old) as useful
  context. The written staleness check runs at Step 0.3, not at write time.
