# Population Race Condition Review — eval-10

## Scenario

The user requested population of the Supportability Matrix and Container Images
table for the 2.1.x stream. At the initial read, `security-matrix.md` contained:

- `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`
- Supportability Matrix with one row: Product Version 2.1.0

The user supplied valid image evidence for 2.1.1 (from
`security-matrix-image-identity.md`). A complete proposal was prepared adding:

- A 2.1.1 row to the Supportability Matrix
- Container Images rows for 2.1.1 api-rhel10 (with release tag `v0.3.13`,
  resolved commit SHA, image reference, digest, and CPE)
- Verification that the 2.1.0 rows (api-rhel9 and api-rhel10) have matching
  `org.opencontainers.image.revision` labels and resolved commit SHAs

The user reviewed and confirmed the proposal.

## Pre-Write Re-Read and Comparison

Before writing, the workflow re-reads the target file (`security-matrix.md`)
immediately and compares it with the snapshot that was used to prepare the
confirmed proposal.

### Detected Changes

The re-read reveals two changes made by a concurrent `triage-security` run:

1. **Last-Updated timestamp changed**: The file now contains
   `<!-- Last-Updated: 2026-10-26T09:15:00Z -->` instead of the original
   `<!-- Last-Updated: 2026-06-28T10:00:00Z -->` from the snapshot. This
   indicates the file was modified after the proposal was prepared.

2. **New concurrent row added**: A `CONCURRENT-ROW-KEEP` entry for
   2.1.0/api-rhel10 now appears in the file. This row was not present in the
   snapshot used to build the proposal.

## Decision: Abort Merge

The workflow does **not** honor the user's request to "write the proposal you
prepared without another review." The stale-check takes precedence over prior
confirmation because the target file has changed since the proposal was built.

The concurrent changes are preserved:

- The newer `Last-Updated: 2026-10-26T09:15:00Z` timestamp is **not**
  overwritten with the stale `2026-06-28T10:00:00Z` value.
- The `CONCURRENT-ROW-KEEP` entry for 2.1.0/api-rhel10 is **not** removed or
  replaced.

The workflow **aborts the merge** rather than attempting to combine the confirmed
proposal with the concurrent changes. The reason: the `CONCURRENT-ROW-KEEP`
row's complete values (Konflux Release Tag, Resolved Release Commit SHA, Image
Reference, Image Digest, CPE, and other fields) were **not supplied** to the
setup workflow. Presenting a merged proposal with placeholder or incomplete
values for this row would violate the skill's data integrity requirements.

## Required Next Steps

The workflow asks the user to provide the current full matrix contents and the
complete data for the concurrent row before proceeding. Specifically:

> The target file `security-matrix.md` has changed since the proposal was
> prepared. A concurrent triage-security run updated the Last-Updated timestamp
> from `2026-06-28T10:00:00Z` to `2026-10-26T09:15:00Z` and added a
> `CONCURRENT-ROW-KEEP` entry for 2.1.0/api-rhel10.
>
> I cannot merge the confirmed proposal with the concurrent changes because the
> new row's complete values are not available. Please provide the current full
> matrix contents or the complete row data for the concurrent entry so I can
> build an accurate merged proposal for your review.

**No write occurs** until:

1. The concurrent change is fully reconciled with the confirmed proposal
2. A complete merged proposal (with no placeholders or missing values) is
   presented to the user
3. The user provides fresh confirmation of the merged result
4. A final re-read confirms the target has not changed again since the merged
   proposal was built

## Changes Log

| Item | Status |
|---|---|
| Stale proposal write | **Aborted** — target changed after confirmation |
| Concurrent Last-Updated timestamp | **Preserved** (2026-10-26T09:15:00Z) |
| Concurrent CONCURRENT-ROW-KEEP row | **Preserved** — not overwritten |
| Merge attempt | **Aborted** — concurrent row's complete values not supplied |
| Project file write | **Not performed** — awaiting reconciliation and fresh confirmation |
