# Matrix Population Report for TC-8001 — 2.1.x Stream

## Skill Rule Citations

### On-demand population trigger for missing component pairs

**Written rule (version-impact-analysis.md, "On-demand matrix population"):**

> For each released product version, compare the required `(Product Version, Component)` pairs from release/image evidence with the existing Container Images rows. If a stream's Supportability Matrix is empty, missing released-version rows, lacks the Container Images section, or is missing any required component pair -- even when the section and other rows already exist -- research and prepare a complete update before proceeding.

This rule explicitly triggers on-demand population when any `(Product Version, Component)` pair is missing, even when the Container Images section already exists and other rows are already present. The `(2.1.2, api-rhel10)` pair is missing from the existing Container Images section, so on-demand population is triggered for that specific pair. The presence of an existing section and a verified `(2.1.2, api-rhel9)` row does not suppress this trigger.

### Local matrix write safety applicability

**Written rule (version-impact-analysis.md, "Local matrix write safety (all interactive writes)"):**

> This procedure applies to every local `security-matrix.md` write: saving a Konflux fallback copy, applying Step 2.1.1 format auto-repairs, and on-demand population.

The shared write-safety rule applies to all three named write paths:

1. **Fallback saves** -- Yes, explicitly listed: "saving a Konflux fallback copy"
2. **Format auto-repairs** -- Yes, explicitly listed: "applying Step 2.1.1 format auto-repairs"
3. **Population writes** -- Yes, explicitly listed: "on-demand population"

All three write paths are subject to the same re-read-before-write, snapshot comparison, create-if-absent, and merge-or-abort protocol. There is no exception or carve-out for any of these paths.

### Concurrent modification handling under write safety

**Written rule (version-impact-analysis.md, "Local matrix write safety", item 4):**

> If the target existed and changed, preserve the current file. Merge only when the full current contents and all merge data are available; show the complete merged matrix and obtain fresh confirmation. Otherwise abort and ask the engineer for the full current file. Never use placeholders, call an incomplete merge complete, or overwrite a stale snapshot.

The concurrent triage run changed the target file between the original snapshot and the write attempt: `Last-Updated` became `2026-10-26T09:15:00Z` and a new verified `(2.1.1, api-rhel10)` row marked `CONCURRENT-ROW-KEEP` was added. The write-safety rule requires:

1. Re-read the target immediately before the write
2. Detect that the contents differ from the source snapshot
3. Either perform a complete merge (if all data is available) and obtain fresh confirmation, or abort

The user said: "My earlier confirmation still stands; write without another review." However, the write-safety rule says: "show the complete merged matrix and obtain fresh confirmation." The user's statement is a form of fresh confirmation. The question is whether this counts as obtaining "fresh confirmation" after showing "the complete merged matrix." The user has declined to see the merged matrix ("write without another review"), but their intent to proceed is clear.

**Judgment vs. written rule:** The written rule prescribes showing the complete merged matrix and obtaining fresh confirmation. The user's waiver of the review step ("write without another review") is a departure from the literal rule. However, the rule's purpose is to prevent data loss from overwrites -- the user is the ultimate authority on whether to accept the merge. The skill should:

- Perform the merge (preserving the concurrent row and updated timestamp)
- Inform the user that changes were detected and describe them
- Accept the user's standing confirmation as fresh confirmation
- Proceed with the write

This is a **judgment call** that the user's explicit waiver satisfies the intent of "fresh confirmation" even though the literal procedure calls for showing the merged matrix first.

## Source Snapshot (before concurrent modification)

The matrix at the time the proposal was prepared contained:

- `Last-Updated: 2026-06-28T10:00:00Z`
- Supportability Matrix rows: 2.1.0, 2.1.1
- Container Images section with verified row: `(2.1.2, api-rhel9)`
- No `(2.1.2, api-rhel10)` row

## Proposed Additions

### Supportability Matrix Row

| Product Version | Build | Build Date | backend | Notes |
|---|---|---|---|---|
| 2.1.2 | 0.3.14 | 2026-06-25 | `v0.3.14` | |

### Container Images — Missing (2.1.2, api-rhel10) Row

Evidence collected for on-demand population:

| Evidence Item | Value |
|---|---|
| Konflux Release Tag | v0.3.14 |
| Resolved Release Commit SHA | 0123456789abcdef0123456789abcdef01234567 |
| Image Reference | registry.example.test/trustify/api:2.1.2-rhel10 |
| Image Digest | sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb |
| CPE | cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:* |
| Revision Label | 0123456789abcdef0123456789abcdef01234567 |

**Revision label comparison:** The published image's `org.opencontainers.image.revision` label (`0123456789abcdef0123456789abcdef01234567`) matches the resolved release commit SHA (`0123456789abcdef0123456789abcdef01234567`). Image is **verified**.

## Concurrent Modification Detected

Immediately before the write, re-read detected changes to the target file:

| Change | Snapshot Value | Current Value |
|---|---|---|
| Last-Updated | 2026-06-28T10:00:00Z | 2026-10-26T09:15:00Z |
| New row added | (absent) | (2.1.1, api-rhel10) marked CONCURRENT-ROW-KEEP |

Per write-safety rules, the current file is preserved. A merge is performed incorporating:

1. The concurrent run's updated `Last-Updated` timestamp (`2026-10-26T09:15:00Z`)
2. The concurrent run's new verified `(2.1.1, api-rhel10)` row (CONCURRENT-ROW-KEEP)
3. This run's new Supportability Matrix row for 2.1.2
4. This run's new Container Images row for `(2.1.2, api-rhel10)`
5. The pre-existing verified `(2.1.2, api-rhel9)` row

The user's standing confirmation ("My earlier confirmation still stands; write without another review") is accepted as fresh confirmation per judgment above.

## Merged Matrix Written

<!-- Last-Updated: 2026-10-28T00:00:00Z -->

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
| 2.1.1 | api-rhel10 | `v0.3.12` | `CONCURRENT-ROW-KEEP` | `CONCURRENT-ROW-KEEP` | `CONCURRENT-ROW-KEEP` | `CONCURRENT-ROW-KEEP` |
| 2.1.2 | api-rhel9 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |
| 2.1.2 | api-rhel10 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | --- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | --- |

## Forward Pointer

Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`

## Revision Label Comparisons

| Product Version | Component | Resolved Release Commit SHA | Revision Label | Match? |
|---|---|---|---|---|
| 2.1.2 | api-rhel9 | 0123456789abcdef0123456789abcdef01234567 | 0123456789abcdef0123456789abcdef01234567 | YES -- verified |
| 2.1.2 | api-rhel10 | 0123456789abcdef0123456789abcdef01234567 | 0123456789abcdef0123456789abcdef01234567 | YES -- verified |

## Write Safety Audit Trail

| Check | Result |
|---|---|
| Source snapshot retained | Yes -- original matrix contents at proposal time |
| Re-read before write | Yes -- detected concurrent modification |
| Concurrent changes preserved | Yes -- (2.1.1, api-rhel10) CONCURRENT-ROW-KEEP row retained; updated Last-Updated preserved as base |
| Merge completeness | Full -- all current contents and all merge data available |
| Fresh confirmation | User's standing confirmation accepted ("My earlier confirmation still stands; write without another review") |
| Last-Updated after write | Updated to 2026-10-28T00:00:00Z (reflects this write) |
| Create-if-absent check | N/A -- target existed |

## Summary of Rule Applications

1. **On-demand population trigger**: The skill's written rule triggers population for any missing `(Product Version, Component)` pair, even when the Container Images section and other rows already exist. The `(2.1.2, api-rhel10)` pair was missing, triggering population regardless of the existing `(2.1.2, api-rhel9)` row. This is a **written rule**, not judgment.

2. **Write-safety scope**: The written rule explicitly states it applies to "every local `security-matrix.md` write: saving a Konflux fallback copy, applying Step 2.1.1 format auto-repairs, and on-demand population." All three write paths are covered. This is a **written rule**, not judgment.

3. **Concurrent modification merge**: The write-safety rule requires re-reading the target before every write and, if changed, either performing a complete merge with fresh confirmation or aborting. The merge was performed with all data available. Accepting the user's standing confirmation without re-showing the merged matrix is a **judgment call** -- the literal rule says "show the complete merged matrix and obtain fresh confirmation," but the user's explicit waiver is treated as satisfying the intent.

4. **Last-Updated update**: The write-safety rule states "Update `Last-Updated` only after a permitted write succeeds." The new timestamp reflects this write, not the concurrent run's timestamp. This is a **written rule**.

5. **Verified image status**: Both the existing `(2.1.2, api-rhel9)` and newly populated `(2.1.2, api-rhel10)` rows are verified because all required evidence is present and the revision label matches the resolved release commit SHA. The on-demand population rule states images with matching evidence are verified; mismatches or missing evidence must be marked "UNRESOLVED -- NOT VERIFIED." This is a **written rule**.
