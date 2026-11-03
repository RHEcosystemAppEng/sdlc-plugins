# TC-8001 — On-demand Matrix Population (2.1.x stream)

**Mode:** Interactive (Step 0.6: `FULLSEND_OUTPUT_DIR` absent). Steps 0.7 and the Fullsend
substitutions do not apply. Synthetic eval data only; no Jira MCP, `git show`, registry, or
other external calls were made.

**Outcome: NOT WRITTEN.** The proposal below was prepared and confirmed, but the target
matrix changed concurrently before the write. Local matrix write safety requires preserving
the current file and either a fully-reviewed merge with **fresh** confirmation or an abort.
The engineer's "my earlier confirmation still stands; write without another review" is not a
fresh confirmation of a merged matrix, and the full current file contents are not available,
so the write was aborted. The current file and its `Last-Updated` timestamp
(`2026-10-26T09:15:00Z`, set by the concurrent run) are left unchanged.

---

## 1. Trigger: why on-demand population ran

Source: `version-impact-analysis.md` → "On-demand matrix population" (written rule):

> "For each released product version, compare the required `(Product Version, Component)`
> pairs from release/image evidence with the existing Container Images rows. If a stream's
> Supportability Matrix is empty, missing released-version rows, lacks the Container Images
> section, or is missing any required component pair—**even when the section and other rows
> already exist**—research and prepare a complete update before proceeding."

Pair comparison for 2.1.x, released version 2.1.2:

| Required pair | Present in Container Images? | Status |
|---|---|---|
| (2.1.2, api-rhel9) | Yes — verified row exists | No change |
| (2.1.2, api-rhel10) | **No** | **Missing → triggers on-demand population** |

The Container Images section already exists and other rows are present; the written rule
explicitly still triggers population for the single missing component pair.

## 2. Evidence for the missing image record (2.1.2, api-rhel10)

| Evidence | Value | Status |
|---|---|---|
| Konflux release tag | `v0.3.14` | present |
| Resolved full release commit SHA | `0123456789abcdef0123456789abcdef01234567` | present |
| Image reference | `registry.example.test/trustify/api:2.1.2-rhel10` | present |
| Image digest | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | present |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` | present |
| `org.opencontainers.image.revision` label | `0123456789abcdef0123456789abcdef01234567` | present |

### Revision-label comparisons (reported separately from the table, per step 3)

| Pair | Resolved release SHA | Revision label | Match | Result |
|---|---|---|---|---|
| (2.1.2, api-rhel9) | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | yes | VERIFIED (existing) |
| (2.1.2, api-rhel10) | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | yes | VERIFIED (new) |

No image row is UNRESOLVED, so the unresolved-evidence block in step 6 does not apply; the
proposal was eligible for confirmation.

## 3. Proposal presented for review (prepared against the original snapshot)

Snapshot used: the fixture's 2.1.x section with `Last-Updated: 2026-06-28T10:00:00Z`,
Supportability Matrix rows 2.1.0, 2.1.1, 2.1.2, existing Container Images section with the
verified (2.1.2, api-rhel9) row, Source Pinning Method, Ecosystem Mappings, and Forward
Pointer. Per step 5 all existing rows, columns, pinning entries, mappings, and the forward
pointer are preserved; only one Container Images row is added.

Proposed 2.1.x content (the 2.2.x stream section is unchanged and omitted here):

```markdown
<!-- Last-Updated: <set only after a permitted write succeeds> -->

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

Engineer response: **confirmed the complete proposal.**

## 4. Pre-write safety check (Local matrix write safety)

Final re-read immediately before the write (step 2: "Do not treat a previous read or user
confirmation as current after time has passed"):

| Item | Snapshot | Current target | Changed |
|---|---|---|---|
| `Last-Updated` | `2026-06-28T10:00:00Z` | `2026-10-26T09:15:00Z` | **yes** |
| Container Images rows | (2.1.2, api-rhel9) | (2.1.2, api-rhel9) + verified (2.1.1, api-rhel10) marked `CONCURRENT-ROW-KEEP` | **yes** |

Result: target existed and changed → step 4 applies:

> "If the target existed and changed, preserve the current file. Merge only when the full
> current contents and all merge data are available; show the complete merged matrix and
> obtain fresh confirmation. Otherwise abort and ask the engineer for the full current file.
> Never use placeholders, call an incomplete merge complete, or overwrite a stale snapshot."

Decision:

- Writing the confirmed proposal would overwrite the stale snapshot and **drop the
  `CONCURRENT-ROW-KEEP` row and the concurrent timestamp** — prohibited.
- A merge is not possible yet: only a description of the concurrent change is available,
  not the full current file contents or the concurrent row's exact cell values (tag, SHA,
  reference, digest, CPE). Writing a merge with placeholders or calling it complete is
  prohibited.
- The engineer's statement "My earlier confirmation still stands; write without another
  review" does not satisfy the rule: the earlier confirmation was for a different file
  state, and step 4 requires the complete merged matrix to be shown and **freshly**
  confirmed. Waiving that review is not an option the skill provides.
- Therefore: **abort the write**, preserve the current file, leave `Last-Updated`
  unchanged at `2026-10-26T09:15:00Z` (step 5), and label the proposal **NOT WRITTEN**.

### Message to the engineer

> The 2.1.x `security-matrix.md` was changed by another triage-security run after you
> confirmed (Last-Updated is now 2026-10-26T09:15:00Z, and a verified 2.1.1/api-rhel10 row
> marked CONCURRENT-ROW-KEEP was added). I did not write anything. Your earlier
> confirmation covered the old file and the skill requires a fresh review of the merged
> result, so I can't write on that confirmation. Please share the complete current file.
> I'll then show you the full merged matrix: the current contents including the
> CONCURRENT-ROW-KEEP row, plus the new (2.1.2, api-rhel10) row. I'll write it only after
> you confirm that merged version, and I'll re-read the file again right before writing.

Intended merge once the full current file is supplied (shown for orientation only; **NOT
WRITTEN**, not a complete merge): keep every current row, including the
`CONCURRENT-ROW-KEEP` (2.1.1, api-rhel10) row exactly as it is, and add only the (2.1.2,
api-rhel10) row from Section 3. Add the 2.1.2 Supportability row only if the current file
does not already have it.

## 5. Written skill rules compared with general judgment

### Written rules (cited from the skill text)

1. **On-demand trigger for a missing component pair, even when the section exists.**
   `version-impact-analysis.md`, On-demand matrix population: "…or is missing any required
   component pair—even when the section and other rows already exist—research and prepare a
   complete update before proceeding." That is why (2.1.2, api-rhel10) triggered population.
2. **Which writes the shared write-safety rule covers.** `version-impact-analysis.md`, Local
   matrix write safety: "This procedure applies to every local `security-matrix.md` write:
   saving a Konflux fallback copy, applying Step 2.1.1 format auto-repairs, and on-demand
   population."
   - **Fallback saves:** yes. "save the fallback copy only under Local matrix write safety
     below. Do not write directly from the fallback branch."
   - **Format auto-repairs:** yes. "Before writing an auto-repair, apply Local matrix write
     safety: re-read and compare the target; if it changed, preserve it and ask for renewed
     review or abort."
   - **Population writes:** yes. Step 6: "write only after the engineer confirms the complete
     proposal and only by following Local matrix write safety above. That shared procedure
     performs the final re-read/compare, create-if-absent check, and merge-or-abort decision
     for this write path as well as fallback saves and repairs."
3. **A stale confirmation does not count.** Step 2: "Do not treat a previous read or user
   confirmation as current after time has passed." Step 4 requires that the complete merged
   matrix be shown and freshly confirmed, and otherwise abort.
4. **Timestamp.** Step 5: "Update `Last-Updated` only after a permitted write succeeds. A
   declined or aborted write leaves the current file and timestamp unchanged."
5. **Verification gate.** Step 4 of population: an image is VERIFIED only when the tag
   resolution, reference, digest, CPE, and revision label are all present and the label
   matches the SHA. Both 2.1.2 rows meet this.
6. **Write scope.** `security-matrix.md` is the only local file the skill may write
   (Guardrails, and the end of 2.1). Fullsend mode prohibits population entirely. That does
   not apply here because this run is interactive.

### General judgment (not stated in the skill text)

- Treating the engineer's "write without another review" as **not** overriding step 4. The
  skill does not say outright that a user cannot waive the review. I read "obtain fresh
  confirmation" together with "Do not treat a previous read or user confirmation as current"
  as making a renewed review of the merged content mandatory. A blanket pre-approval of
  unseen content is not a review.
- Deciding that a description of the concurrent change ("a verified 2.1.1/api-rhel10 row
  marked CONCURRENT-ROW-KEEP was added") does **not** amount to "full current contents". The
  row's exact cell values are unknown, so any reconstruction would involve guessing. That
  conflicts with the step 4 ban on placeholders and incomplete merges, and with the skill's
  no-fabrication guardrail.
- Placing the Container Images table under the Supportability Matrix as a `####` subsection,
  following the canonical template layout.
- Choosing to stop and ask for the full file now, rather than offering to merge from the
  description. The rule allows either a complete merge or an abort. Without the full file,
  abort is the only path consistent with the rule.

## 6. Files

- Written: `/tmp/triage-security-eval-baseline/eval-33/outputs/matrix-population.md` (this report).
- Not modified: the local 2.1.x `security-matrix.md`, the eval fixture files, and all project
  files.
