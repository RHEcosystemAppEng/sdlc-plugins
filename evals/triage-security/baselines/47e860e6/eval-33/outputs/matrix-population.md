# TC-8001 — On-demand Matrix Population (2.1.x stream)

**Mode:** Interactive (not Fullsend). Synthetic data only. No Jira MCP, `git show`,
registry API, or other external calls were made. No project files were modified.

**Outcome:** **NOT WRITTEN.** The write was aborted at the final re-read/compare
because the target changed concurrently after the engineer confirmed the
proposal. The earlier confirmation does not authorize writing over, or merging
into, the changed file. The local 2.1.x `security-matrix.md` stays as it currently
is, including the concurrent run's `Last-Updated: 2026-10-26T09:15:00Z` and its
`CONCURRENT-ROW-KEEP` row. This run did not touch the timestamp.

---

## 1. Source snapshot (state used to prepare the proposal)

Snapshot = fixture 2.1.x stream section (`security-matrix-mock.md`) plus the
supplemental state from the task:

- `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`
- Supportability Matrix rows: 2.1.0 / 0.3.8 / `v0.3.8`, 2.1.1 / 0.3.12 / `v0.3.12`,
  **2.1.2 / 0.3.14 / 2026-06-25 / `v0.3.14`**
- Container Images section exists, with one verified row: `(2.1.2, api-rhel9)`
- Source Pinning Method (backend: `artifacts.lock.yaml`), Ecosystem Mappings
  (Cargo/backend `release/0.3.z`, RPM `rpms.lock.yaml`), and the Forward Pointer to
  2.2.x are all present.

Staleness note (Step 0.3): the snapshot timestamp 2026-06-28 is 129 days before
today (2026-11-04), which is past the 14-day threshold.

## 2. Trigger: why population ran even though the section exists

**Written rule** (`version-impact-analysis.md`, "On-demand matrix population"):

> "For each released product version, compare the required `(Product Version, Component)`
> pairs from release/image evidence with the existing Container Images rows. If a stream's
> Supportability Matrix is empty, missing released-version rows, lacks the Container Images
> section, **or is missing any required component pair—even when the section and other rows
> already exist**—research and prepare a complete update before proceeding."

Comparison of required and existing pairs:

| Product Version | Component | Required by evidence | Present in Container Images | Result |
|---|---|---|---|---|
| 2.1.2 | api-rhel9 | yes | yes (verified) | keep as is |
| 2.1.2 | api-rhel10 | yes | **no** | **missing pair, which triggers population** |

The missing `(2.1.2, api-rhel10)` pair triggers population on its own. The rule
says explicitly that an existing section and existing rows do not suppress it.
The rule also keys each row by the exact `(Product Version, Component)` pair, so
the api-rhel9 row does not cover api-rhel10.

## 3. Evidence for the missing image record

| Field | Value |
|---|---|
| Konflux release tag | `v0.3.14` |
| Resolved full release commit SHA | `0123456789abcdef0123456789abcdef01234567` |
| Image reference | `registry.example.test/trustify/api:2.1.2-rhel10` |
| Image digest | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |

The tag, SHA, reference, and digest are kept as separate values. None of them was
inferred from another.

### Revision-label comparison (reported separately from the table, per rule step 3)

| Product Version | Component | `org.opencontainers.image.revision` | Resolved release SHA | Match | Status |
|---|---|---|---|---|---|
| 2.1.2 | api-rhel9 | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | yes | VERIFIED |
| 2.1.2 | api-rhel10 | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | yes | VERIFIED |

All evidence fields are present and both labels match. No row is UNRESOLVED, so the
proposal was eligible for confirmation.

## 4. Proposed update (confirmed by the engineer, then **NOT WRITTEN**)

Existing rows, source columns, Source Pinning Method, Ecosystem Mappings, and
Forward Pointer are kept unchanged (rule step 5). The only addition is the
api-rhel10 Container Images row.

```markdown
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
(unchanged — Cargo/backend/`release/0.3.z`; RPM/`rpms.lock.yaml`)

## Forward Pointer
(unchanged — Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
```

The engineer confirmed this complete proposal.

## 5. Write-time safety check: concurrent change detected, write aborted

Step 2 of **Local matrix write safety** requires a re-read just before the write.
That re-read found that the target no longer matches the snapshot:

| Item | Snapshot | Current target |
|---|---|---|
| `Last-Updated` | `2026-06-28T10:00:00Z` | `2026-10-26T09:15:00Z` |
| Container Images rows | (2.1.2, api-rhel9) | (2.1.2, api-rhel9) **+ verified (2.1.1, api-rhel10) row marked `CONCURRENT-ROW-KEEP`** |

The engineer then said: *"My earlier confirmation still stands; write without
another review."* **That request was declined.** The reasons:

- Rule step 2: "Do not treat a previous read or user confirmation as current after
  time has passed." The confirmation applied to a proposal built on a snapshot that
  is now stale.
- Rule step 4: "If the target existed and changed, preserve the current file. Merge
  only when the full current contents and all merge data are available; show the
  complete merged matrix and **obtain fresh confirmation**. Otherwise abort and ask
  the engineer for the full current file. Never ... overwrite a stale snapshot."
- Merge is not possible at this point. I know that a `CONCURRENT-ROW-KEEP` row for
  (2.1.1, api-rhel10) was added and that the timestamp changed. I do not have the
  full current file or that row's exact field values (tag, SHA, reference, digest,
  CPE). Building a merge from that would mean using placeholders or calling an
  incomplete merge complete, and the rule forbids both.
- Writing the proposal as confirmed would overwrite the stale snapshot. That would
  drop the concurrent `CONCURRENT-ROW-KEEP` row and roll `Last-Updated` back or
  replace it.
- Rule step 5: "A declined or aborted write leaves the current file and timestamp
  unchanged."

**Result:** write aborted. The current file is kept exactly as the concurrent run
left it, with `Last-Updated: 2026-10-26T09:15:00Z` and the `CONCURRENT-ROW-KEEP`
row intact. This run did not set any new `Last-Updated`.

### Next step requested from the engineer

> The 2.1.x security matrix changed after you confirmed (Last-Updated is now
> 2026-10-26T09:15:00Z and a verified 2.1.1/api-rhel10 row marked
> CONCURRENT-ROW-KEEP was added). I cannot reuse the earlier confirmation, and I
> have not written anything. Please provide the full current contents of the
> 2.1.x security-matrix.md. I will then show the complete merged matrix (keeping
> CONCURRENT-ROW-KEEP and adding the verified 2.1.2/api-rhel10 row) for a fresh
> confirmation before any write.

Triage of TC-8001 can continue in memory with the current matrix data. The
(2.1.2, api-rhel10) row is still not persisted.

## 6. Written rules vs. general judgment

### What the skill's written rules state

| Question | Written rule | Source |
|---|---|---|
| Does a missing component pair trigger population when the Container Images section exists? | **Yes.** "...or is missing any required component pair—even when the section and other rows already exist." | `version-impact-analysis.md`, On-demand matrix population |
| Does the shared write-safety rule apply to **fallback saves**? | **Yes.** "save the fallback copy only under Local matrix write safety ... Do not write directly from the fallback branch." Its scope line lists "saving a Konflux fallback copy". | Fallback to Konflux repos; Local matrix write safety |
| Does it apply to **format auto-repairs**? | **Yes.** It lists "applying Step 2.1.1 format auto-repairs". Also: "Before writing an auto-repair, apply Local matrix write safety: re-read and compare the target; if it changed, preserve it and ask for renewed review or abort." A Repaired result proceeds without a prompt only if the final comparison is unchanged. | Local matrix write safety; 2.1.1 |
| Does it apply to **population writes**? | **Yes.** It lists "on-demand population". Population step 6: "write only after the engineer confirms ... and only by following Local matrix write safety ... That shared procedure performs the final re-read/compare, create-if-absent check, and merge-or-abort decision for this write path as well as fallback saves and repairs." | Local matrix write safety; population step 6 |
| Can a prior confirmation authorize a write after the target changed? | **No.** Step 2 ("Do not treat a previous read or user confirmation as current") and step 4 (fresh confirmation for a merge; otherwise abort and ask for the full current file). | Local matrix write safety, steps 2 and 4 |
| Timestamp on abort? | Unchanged. `Last-Updated` is updated only after a permitted write succeeds. | Step 5; population step 6 |
| Is the matrix the only local file the skill writes? | Yes. | End of population section |

### Where I used general judgment (no specific written rule)

- **Treating the engineer's "write without another review" as non-binding.** The
  rules require fresh confirmation of a merged matrix and do not offer an override.
  Reading the user's statement as unable to waive that requirement is my
  interpretation of the rule's mandatory wording. No clause says "even if the user
  insists".
- **Deciding the full current contents were unavailable.** The task described the
  concurrent change only in summary, without the CONCURRENT-ROW-KEEP row's field
  values. Concluding that this blocks a complete merge, so the rule's "otherwise
  abort" branch applies instead of "show merged matrix", is a judgment about how
  complete the evidence is.
- **Keeping the 2.1.x Supportability Matrix header `Version` and not renaming it
  to `Product Version`.** The rules say Supportability Matrix columns are
  product-specific and existing columns must be preserved. Leaving the header alone
  is consistent with that, but the choice is mine.
- **Continuing TC-8001 triage in memory** while the matrix write is pending. The
  rules do not explicitly cover this case after a write abort.
- **Mentioning the 129-day staleness of the snapshot.** The Step 0.3 threshold is
  written, but the simulated scenario skipped the staleness prompt. Raising it here
  as a note is my choice.
