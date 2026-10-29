# Matrix Population Analysis — TC-8001 (2.1.x Stream)

## 1. On-Demand Population Trigger

### Trigger condition (written rule)

The on-demand population procedure in `version-impact-analysis.md` (Step 2.1,
"On-demand matrix population") states:

> For each released product version, compare the required `(Product Version,
> Component)` pairs from release/image evidence with the existing Container
> Images rows. If a stream's Supportability Matrix is empty, missing
> released-version rows, lacks the Container Images section, **or is missing
> any required component pair -- even when the section and other rows already
> exist** -- research and prepare a complete update before proceeding.

**Application to this scenario:** The 2.1.x stream's `security-matrix.md`
already contains a Container Images section with a verified `(2.1.2,
api-rhel9)` row. However, the `(2.1.2, api-rhel10)` component pair is missing
from that section. The written rule explicitly covers this case with the clause
"even when the section and other rows already exist." Therefore, on-demand
population fires for the missing `(2.1.2, api-rhel10)` pair despite the
section's existence and despite other rows being present.

This is a **written rule**, not general judgment. The skill text is explicit
and deterministic: a missing component pair is a sufficient trigger regardless
of the section's overall state.

## 2. Current Matrix State (Pre-Population Snapshot)

The 2.1.x stream's `security-matrix.md` contains the following state at the
time of triage, used as the **source snapshot** for write-safety comparison:

**Last-Updated:** `2026-06-28T10:00:00Z`

### Supportability Matrix

| Product Version | Build | Build Date | backend | Notes |
|---|---|---|---|---|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.2 | 0.3.14 | 2026-06-25 | `v0.3.14` | |

### Container Images (existing section)

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.2 | api-rhel9 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |

### Missing pair

| Product Version | Component | Status |
|---|---|---|
| 2.1.2 | api-rhel10 | **MISSING** -- triggers on-demand population |

## 3. Evidence for Missing (2.1.2, api-rhel10) Row

The following evidence was provided for the missing component pair:

| Evidence field | Value |
|---|---|
| Konflux Release Tag | `v0.3.14` |
| Resolved Release Commit SHA | `0123456789abcdef0123456789abcdef01234567` |
| Image Reference | `registry.example.test/trustify/api:2.1.2-rhel10` |
| Image Digest | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |
| `org.opencontainers.image.revision` label | `0123456789abcdef0123456789abcdef01234567` |

### Revision label comparison

Per on-demand population step 3 in `version-impact-analysis.md`:

> Compare the published image's `org.opencontainers.image.revision` label with
> the resolved full release SHA; report the comparison separately from the
> Container Images table.

| Image | Resolved Release Commit SHA | Revision Label | Match? |
|---|---|---|---|
| `registry.example.test/trustify/api:2.1.2-rhel9` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | **YES** -- verified |
| `registry.example.test/trustify/api:2.1.2-rhel10` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | **YES** -- verified |

Both image rows have matching revision labels. No unresolved evidence exists.

## 4. Proposed Matrix Update

All image rows are verified. The proposed update adds the `(2.1.2, api-rhel10)`
row to the existing Container Images section.

### Proposed Container Images section (complete)

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.2 | api-rhel9 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |
| 2.1.2 | api-rhel10 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |

**Engineer confirmation:** The user confirmed the complete proposal.

## 5. Concurrent Change Detection and Write-Safety Analysis

### 5.1 Concurrent change detected

Immediately before writing (per Local matrix write safety step 2), the target
file was re-read and compared against the source snapshot from Section 2 above.
The following differences were found:

| Field | Snapshot value | Current value |
|---|---|---|
| `Last-Updated` | `2026-06-28T10:00:00Z` | `2026-10-26T09:15:00Z` |
| Container Images rows | 1 row (2.1.2, api-rhel9) | 2 rows: (2.1.2, api-rhel9) + **(2.1.1, api-rhel10) CONCURRENT-ROW-KEEP** |

A concurrent triage-security run modified the target between the user's
confirmation and the write attempt.

### 5.2 Write-safety rule application (written rule)

The Local matrix write safety procedure in `version-impact-analysis.md`
(Step 2.1) applies here. The rule states:

> This procedure applies to **every** local `security-matrix.md` write: saving
> a Konflux fallback copy, applying Step 2.1.1 format auto-repairs, and
> on-demand population.

This is a **written rule**: the shared write-safety procedure governs all three
write types (fallback saves, format auto-repairs, and population writes)
without exception. The current write is an on-demand population write and is
therefore covered.

### 5.3 Merge-or-abort decision (written rule)

Write-safety step 4 states:

> If the target existed and changed, preserve the current file. Merge only when
> the full current contents and all merge data are available; show the complete
> merged matrix and obtain fresh confirmation. Otherwise abort and ask the
> engineer for the full current file. Never use placeholders, call an incomplete
> merge complete, or overwrite a stale snapshot.

**Analysis:**

1. The target existed and **changed** -- the concurrent run updated
   `Last-Updated` and added a `(2.1.1, api-rhel10)` row. The snapshot no
   longer matches the current file.

2. **Full current contents and all merge data are available:**
   - The current file has been re-read in its entirety.
   - The concurrent `(2.1.1, api-rhel10)` CONCURRENT-ROW-KEEP row is visible.
   - The proposed `(2.1.2, api-rhel10)` row's evidence is complete and verified.
   - No placeholders or missing data exist.

   Therefore, a merge is feasible.

3. **Merged matrix would contain:**
   - `Last-Updated`: `2026-10-26T09:15:00Z` (preserve the newer concurrent
     timestamp; update after this write succeeds per step 5)
   - Supportability Matrix: rows for 2.1.0, 2.1.1, 2.1.2 (unchanged)
   - Container Images: three rows:
     - `(2.1.2, api-rhel9)` -- existing, unchanged
     - `(2.1.1, api-rhel10)` CONCURRENT-ROW-KEEP -- concurrent addition, preserved
     - `(2.1.2, api-rhel10)` -- our proposed addition
   - All other sections preserved from current file

4. **Fresh confirmation is required.** The written rule says "show the complete
   merged matrix **and** obtain fresh confirmation." This is a conjunctive
   requirement: both showing and confirming are mandatory.

### 5.4 User instruction conflict

The user states: "My earlier confirmation still stands; write without another
review."

**Written rule verdict:** The Local matrix write safety procedure requires
**fresh** confirmation of the **complete merged** matrix after a concurrent
change is detected. The rule does not provide an override mechanism or permit
the engineer to waive the re-confirmation step. The word "fresh" in the rule
distinguishes this confirmation from a prior one; it must be a new confirmation
given after the merged matrix has been presented.

**Outcome:** The skill must **not** write the file based on the stale
confirmation. The correct behavior is:

1. Preserve the current file unchanged (including the concurrent
   `(2.1.1, api-rhel10)` row and the `2026-10-26T09:15:00Z` timestamp).
2. Present the complete merged matrix to the engineer (showing all three
   Container Images rows and the preserved concurrent timestamp).
3. Wait for the engineer to provide fresh confirmation of that specific
   merged state.
4. Only then write, following the remainder of the write-safety procedure.

This is a **written rule** determination, not general judgment. The skill text
is deterministic: "show the complete merged matrix and obtain fresh
confirmation" admits no shortcut.

### 5.5 Proposed merged matrix (for fresh confirmation)

The following merged matrix would be presented to the engineer for fresh
confirmation:

```
<!-- Last-Updated: <to-be-set-after-write> -->

# Stream 1: rhtpa-release.0.3.z (2.1.x stream)

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Product Version | Build | Build Date | backend | Notes |
|---|---|---|---|---|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.2 | 0.3.14 | 2026-06-25 | `v0.3.14` | |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.1 | api-rhel10 | (CONCURRENT-ROW-KEEP -- preserved from concurrent run) | | | | |
| 2.1.2 | api-rhel9 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |
| 2.1.2 | api-rhel10 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

## Forward Pointer

Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
```

Note: The `(2.1.1, api-rhel10)` CONCURRENT-ROW-KEEP row is preserved exactly
as written by the concurrent run. Its internal fields are retained as-is. The
`Last-Updated` timestamp would be set after the write succeeds, per write-safety
step 5.

## 6. Rule Citations Summary

### Written rules applied

| Rule | Source | Application |
|---|---|---|
| On-demand trigger for missing component pairs | `version-impact-analysis.md`, Step 2.1, "On-demand matrix population" | Fires for `(2.1.2, api-rhel10)` even though the Container Images section exists and the `(2.1.2, api-rhel9)` row is present. The clause "even when the section and other rows already exist" is explicit. |
| Write-safety scope | `version-impact-analysis.md`, Step 2.1, "Local matrix write safety" | "This procedure applies to **every** local `security-matrix.md` write: saving a Konflux fallback copy, applying Step 2.1.1 format auto-repairs, and on-demand population." All three write types are covered without exception. |
| Write-safety concurrent-change handling | `version-impact-analysis.md`, Step 2.1, "Local matrix write safety", step 4 | "If the target existed and changed, preserve the current file. Merge only when the full current contents and all merge data are available; show the complete merged matrix and obtain fresh confirmation." |
| Revision label comparison | `version-impact-analysis.md`, Step 2.1, "On-demand matrix population", step 3 | "Compare the published image's `org.opencontainers.image.revision` label with the resolved full release SHA; report the comparison separately from the Container Images table." |
| Last-Updated timing | `version-impact-analysis.md`, Step 2.1, "Local matrix write safety", step 5 | "Update `Last-Updated` only after a permitted write succeeds. A declined or aborted write leaves the current file and timestamp unchanged." |
| Unresolved evidence block | `version-impact-analysis.md`, Step 2.1, "On-demand matrix population", step 6 | "If any image evidence is unresolved, keep the current matrix and its `Last-Updated` timestamp unchanged... Do not write any part of the proposal while an image row is unresolved." (Not triggered here -- all evidence is resolved.) |

### General judgment (not rule-dictated)

| Decision | Rationale |
|---|---|
| Row ordering in merged Container Images table | Sorted by (Product Version, Component) for readability. The template does not prescribe row ordering within the table. |
| Preserving the concurrent run's newer `Last-Updated` timestamp in the merge base | The write-safety rule says "preserve the current file" when it has changed; the newer timestamp is part of the current file's state. |
| Interpretation of "fresh confirmation" as incompatible with the user's "earlier confirmation still stands" | The word "fresh" in the rule explicitly distinguishes it from a prior confirmation. This is a direct textual reading, but the determination that the user's statement does not satisfy "fresh" is an interpretive judgment anchored in the rule's plain language. |

## 7. Final Status

**Write status:** NOT WRITTEN

The on-demand population write was blocked by Local matrix write safety. A
concurrent change was detected between proposal confirmation and the write
attempt. The written rule requires showing the complete merged matrix and
obtaining fresh confirmation. The user's instruction to skip re-review does
not satisfy the "fresh confirmation" requirement.

**Next action required:** Present the merged matrix (Section 5.5 above) to
the engineer and obtain explicit fresh confirmation before writing.
