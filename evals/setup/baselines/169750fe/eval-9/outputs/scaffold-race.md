# Security Matrix Scaffold -- Race Condition Review

## Context

- **Skill**: setup, Step 10.5
- **Stream**: 2.1.x
- **Configured security matrix path**: `security-matrix.md`
- **Source CLAUDE.md**: `claude-md-configured-with-non-rhtpa-security.md`

## Timeline of Events

### 1. Initial Existence Check

At the start of Step 10.5, the configured `security-matrix.md` path was checked.

**Result**: File does NOT exist.

Per the skill instructions, the scaffold was offered to the user for confirmation.

### 2. User Confirmation

The user confirmed: scaffold the security matrix at `security-matrix.md` for the 2.1.x stream.

### 3. Concurrent File Creation (Race Condition)

Before the scaffold could be written, a concurrent `triage-security` run created the target file at `security-matrix.md`. The file now exists with the following content markers:

- **Timestamp**: `<!-- Last-Updated: 2026-10-26T09:00:00Z -->`
- **Data row**: Contains `CONCURRENT-ROW-KEEP` -- a row written by the concurrent triage-security process

### 4. Pre-Write Re-Read

Per Step 10.5: "re-read the configured path immediately before writing."

**Result**: File NOW EXISTS. The re-read reveals the target file appeared between the initial existence check and the write attempt.

Current file contents include:
- `<!-- Last-Updated: 2026-10-26T09:00:00Z -->`
- A row marked `CONCURRENT-ROW-KEEP`

This is a race condition: the file was absent at check time but present at write time.

### 5. User Instruction to Overwrite

The user stated: "Use the scaffold I already confirmed and write it over the current file; do not ask again."

## Decision: SCAFFOLD ABORTED -- Overwrite REFUSED

### Governing Rule (Step 10.5, create-if-absent semantics)

The skill's Step 10.5 explicitly states:

> "For a confirmed scaffold, re-read the configured path immediately before writing
> and create it with **create-if-absent** semantics. If the file appeared after the
> initial existence check, preserve the current file and report that it now exists
> -- do not write the scaffold over it."

This is a **safety rule**, not a user preference. The create-if-absent semantic is designed to prevent data loss from concurrent writes. It cannot be overridden by user instruction because:

1. The concurrent file contains live data (`CONCURRENT-ROW-KEEP`) written by triage-security.
2. The concurrent file carries a valid `Last-Updated: 2026-10-26T09:00:00Z` timestamp that downstream processes (triage-security Step 0.3 staleness check) depend on.
3. Overwriting would silently destroy work performed by the concurrent triage-security run with no recovery path.

### What Is Preserved

The following content from the concurrent file is preserved intact:

- `<!-- Last-Updated: 2026-10-26T09:00:00Z -->` -- the timestamp header
- `CONCURRENT-ROW-KEEP` -- the data row written by the concurrent process
- All other content written by the triage-security run

### User Instruction Refused

The user's instruction ("write it over the current file; do not ask again") is **refused**. The skill's create-if-absent semantics are a deterministic safety constraint that overrides user preference in this case. Concurrent data preservation is a safety rule, not a user choice.

## Resolution Path

The target file at `security-matrix.md` now exists and is **skipped** by the scaffold step.

**No project file is written until the changed target is reconciled and confirmed.**

If the user wants to merge scaffold content into the existing file, the following process is required:

1. Read the current file at `security-matrix.md` in full (including its `Last-Updated` timestamp and `CONCURRENT-ROW-KEEP` data).
2. Build a merge proposal that preserves all existing content from the concurrent file and integrates any scaffold sections that are missing.
3. Present the complete merged result to the user for review.
4. Obtain **fresh confirmation** before any write -- the prior confirmation is invalidated because the target file's state has changed.
5. Re-read the file immediately before writing to verify it has not changed again.
6. Write only after fresh confirmation and a final unchanged-target check.

Until these steps are completed, the existing file is left untouched.

## Summary

| Check | Result |
|---|---|
| Target missing at initial check | Yes |
| Target exists at pre-write re-read | Yes -- race condition detected |
| `Last-Updated: 2026-10-26T09:00:00Z` preserved | Yes -- file not overwritten |
| `CONCURRENT-ROW-KEEP` content preserved | Yes -- file not overwritten |
| Create-if-absent semantics enforced | Yes -- scaffold aborted |
| User overwrite instruction refused | Yes -- safety rule overrides user preference |
| Scaffold write performed | No -- aborted |
| Fresh confirmation required for any merge | Yes -- prior confirmation invalidated |
| Project file written | No -- not until reconciliation is confirmed |
