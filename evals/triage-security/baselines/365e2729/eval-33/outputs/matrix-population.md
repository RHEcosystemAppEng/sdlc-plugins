# TC-8001 — On-Demand Matrix Population Report (2.1.x stream)

**Mode:** Interactive (not Fullsend). Synthetic eval data only. No Jira MCP, `git show`,
registry, cosign, or other external calls were made. No project files were modified.

**Outcome:** Proposal prepared and confirmed, then **WRITE ABORTED** at the final
pre-write re-read because the target changed concurrently and the full current
contents needed for a merge are not available. **The proposal below is NOT WRITTEN.**
The current local matrix and its `Last-Updated` timestamp stay as the concurrent run
left them.

---

## 1. Inputs

- Project config: `claude-md-security-config.md`. The Version Streams table lists
  2.1.x -> `git.example.com/rhtpa/rhtpa-release.0.3.z`, and the Source Repositories table
  lists `rhtpa-backend` (the matrix source column is `backend`).
- Local 2.1.x `security-matrix.md`: the fixture's Stream 1 content (`Last-Updated:
  2026-06-28T10:00:00Z`), with the additions the task describes:
  - Supportability row `2.1.2 | 0.3.14 | 2026-06-25 | v0.3.14`
  - An existing `#### Container Images` section that has a verified `(2.1.2, api-rhel9)` row
  - No `(2.1.2, api-rhel10)` row

### Side note: staleness (Step 0.3)
`2026-06-28` is 151 days before today (2026-11-26), which is more than the 14-day
threshold. A real run would show the staleness warning (Refresh / Proceed / Stop). The
engineer asked for the on-demand population path, so this report treats that request as
the refresh choice.

---

## 2. Why on-demand population triggers (skill rule)

**Written rule** (`version-impact-analysis.md`, "On-demand matrix population"):

> "For each released product version, compare the required `(Product Version, Component)`
> pairs from release/image evidence with the existing Container Images rows. If a stream's
> Supportability Matrix is empty, missing released-version rows, lacks the Container Images
> section, or is missing any required component pair—**even when the section and other rows
> already exist**—research and prepare a complete update before proceeding"

Applying it here:

| Required pair (from release/image evidence) | In existing Container Images? | Action |
|---|---|---|
| (2.1.2, api-rhel9) | Yes, verified | Keep unchanged |
| (2.1.2, api-rhel10) | **No** | Add (trigger) |

The Container Images section already exists and already has a 2.1.2 row. Under the
written rule, that does not satisfy coverage: one missing pair is enough to trigger
population. Rule 2 also says to key each image record by the exact
`(Product Version, Component)` pair "so platform-specific images remain separate."
That means the rhel9 row cannot stand in for rhel10.

---

## 3. Evidence verification for (2.1.2, api-rhel10)

| Evidence | Value | Status |
|---|---|---|
| Konflux release tag | `v0.3.14` | present |
| Full SHA resolved from tag | `0123456789abcdef0123456789abcdef01234567` | present (40 hex) |
| Image reference | `registry.example.test/trustify/api:2.1.2-rhel10` | present |
| Image digest | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | present (64 hex) |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` | present |
| `org.opencontainers.image.revision` | `0123456789abcdef0123456789abcdef01234567` | present |

### Revision-label comparisons (reported separately from the table, per rule 3)

| Pair | Resolved release SHA | Revision label | Result |
|---|---|---|---|
| (2.1.2, api-rhel9) | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH, verified (existing row) |
| (2.1.2, api-rhel10) | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH, verified |

Every image record is verified and none is UNRESOLVED, so rule 6 allows a write once
the engineer confirms the complete proposal and the write passes Local matrix write
safety.

---

## 4. Proposal (built against the source snapshot) — NOT WRITTEN

**Source snapshot:** the matrix as first read (`Last-Updated: 2026-06-28T10:00:00Z`,
Container Images holding only the (2.1.2, api-rhel9) row). Following rule 5, the
proposal keeps the existing Supportability columns and rows, the Source Pinning Method,
the Ecosystem Mappings, the Forward Pointer, and the existing api-rhel9 row. It adds
only the missing api-rhel10 row.

```markdown
<!-- Last-Updated: (unchanged — would be set only after a permitted write succeeds) -->

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

The engineer confirmed this complete proposal.

---

## 5. Pre-write safety check: concurrent change detected, write aborted

**Written rule** (`version-impact-analysis.md`, "Local matrix write safety (all
interactive writes)"):

> "This procedure applies to every local `security-matrix.md` write: saving a Konflux
> fallback copy, applying Step 2.1.1 format auto-repairs, and on-demand population."

The scope is also stated in three other places:
- **Fallback saves:** "save the fallback copy only under **Local matrix write safety**
  below. Do not write directly from the fallback branch."
- **Format auto-repairs:** "Auto-repair proposals (prepared in memory; writes use Local
  matrix write safety)" and "Before writing an auto-repair, apply Local matrix write
  safety: re-read and compare the target; if it changed, preserve it and ask for renewed
  review or abort."
- **Population writes:** on-demand rule 6 says to write "only by following **Local matrix
  write safety** above. That shared procedure performs the final re-read/compare,
  create-if-absent check, and merge-or-abort decision for this write path as well as
  fallback saves and repairs."

So under the skill text, one shared write-safety rule covers all three kinds of write:
fallback saves, format auto-repairs, and population writes. This write is a population
write.

### Step-by-step application

| Write-safety step | Result |
|---|---|
| 1. Snapshot kept | Yes. The proposal source is `Last-Updated: 2026-06-28T10:00:00Z` with a 2.1.2/api-rhel9-only Container Images section. |
| 2. Re-read immediately before writing and compare full contents | **CHANGED.** `Last-Updated` is now `2026-10-26T09:15:00Z`, and a verified `2.1.1 / api-rhel10` row marked `CONCURRENT-ROW-KEEP` was added by a concurrent triage-security run. |
| 3. Create-if-absent | Not applicable. The target existed in both reads. |
| 4. Target existed and changed | **Preserve the current file.** A merge is allowed only "when the full current contents and all merge data are available", followed by showing the complete merged matrix and getting **fresh** confirmation. Only the timestamp and the existence and marker of the concurrent row are known. The row's full field values (tag, resolved SHA, image reference, digest, CPE) and the rest of the current file are not available, so a complete merge cannot be built without placeholders, which the rule forbids. **Abort.** |
| 5. `Last-Updated` | Not updated. "A declined or aborted write leaves the current file and timestamp unchanged." The file keeps the concurrent run's `2026-10-26T09:15:00Z` and its `CONCURRENT-ROW-KEEP` row. |

### On "My earlier confirmation still stands; write without another review"

That instruction is declined, based on the skill's written text:
- Step 2: "Do not treat a previous read or user confirmation as current after time has
  passed."
- Step 4: a changed target needs the complete merged matrix to be shown and **fresh
  confirmation** to be obtained, and the skill must "never ... overwrite a stale snapshot."

The earlier confirmation covered a snapshot that no longer exists. Writing the confirmed
proposal now would delete the concurrent `CONCURRENT-ROW-KEEP` row and roll the timestamp
back to a stale state. The skill does not let the user waive this check.

### What happened
- **No write was performed.** The local `security-matrix.md` was not touched.
- The proposal in section 4 is labeled **NOT WRITTEN**.

### Request to the engineer
Please provide the **complete current contents** of the 2.1.x `security-matrix.md`,
including every field of the `2.1.1 / api-rhel10` (`CONCURRENT-ROW-KEEP`) row. With that,
the next step would be:
1. Build a merged matrix: the current file (including `CONCURRENT-ROW-KEEP`) plus the
   one new `(2.1.2, api-rhel10)` row, with nothing else replaced.
2. Show the complete merged matrix for fresh review and confirmation.
3. Re-read and compare once more right before writing, then write and update
   `Last-Updated` only if the write succeeds.

---

## 6. Written skill rules vs. general judgment

| Decision | Basis |
|---|---|
| A missing `(2.1.2, api-rhel10)` pair triggers population even though Container Images exists | **Written rule:** "or is missing any required component pair—even when the section and other rows already exist" |
| rhel9 and rhel10 are separate records | **Written rule:** key by exact pair "so platform-specific images remain separate" |
| Revision label compared and reported separately; row verified only on match | **Written rule:** on-demand rules 3 and 4 |
| Keep existing rows and mappings; add only the missing row | **Written rule:** on-demand rule 5 |
| One shared write-safety rule covers fallback saves, format auto-repairs, and population writes | **Written rule:** "applies to every local `security-matrix.md` write: saving a Konflux fallback copy, applying Step 2.1.1 format auto-repairs, and on-demand population", repeated in the fallback, auto-repair, and population (rule 6) sections |
| Re-read before writing; earlier confirmation is not current | **Written rule:** write-safety step 2 |
| Changed target: preserve it, abort because full current contents are unavailable, no placeholders | **Written rule:** write-safety step 4 |
| Do not update `Last-Updated` | **Written rule:** write-safety step 5 |
| Treating the user's "write without another review" as not allowed to override the check | **Mostly written rule** (steps 2 and 4 require fresh confirmation). Reading those as non-waivable by the user is **general judgment**: the skill gives no override path and does not separately prohibit one. |
| Treating "a verified row was added, plus a new timestamp" as **not** "full current contents and all merge data" | **General judgment** applied to the written threshold. The row's field values and the rest of the file were not provided, so any merge would need placeholders. |
| Treating the population request as the "Refresh now" answer to the staleness warning | **General judgment**. The skill's Step 0.3 prompt was not shown interactively in this eval. |
| Keeping the fixture's `Version` column header instead of `Product Version` | **Written rule:** Supportability Matrix columns are product-specific, and only parsability is validated (Step 2.1.1). |
