# Scaffold Race Condition Review — security-matrix.md (2.1.x stream)

## Initial State

- **Target path:** `security-matrix.md` (configured in Version Streams for the 2.1.x stream)
- **Initial existence check (Step 10.5):** File does **not** exist.
- **User action:** Confirmed scaffolding the missing matrix from `docs/templates/security-matrix.template.md`.

## Pre-Write Re-Check

Immediately before writing the scaffold, the setup skill re-reads the target path as required by Step 10.5's create-if-absent semantics.

**Result:** The file now **exists**. A concurrent `triage-security` run created it between the initial check and the write attempt.

### Current file contents (concurrent version)

The file created by the concurrent run contains:

- First line: `<!-- Last-Updated: 2026-10-26T09:00:00Z -->`
- A data row marked `CONCURRENT-ROW-KEEP`

These contents represent live triage work and must not be discarded.

## Decision: Scaffold Aborted

The setup skill uses **create-if-absent** semantics for security-matrix.md scaffolding. Because the target file now exists — despite being absent at the initial check — the scaffold **will not be written**.

- The current `Last-Updated: 2026-10-26T09:00:00Z` timestamp is **preserved**.
- The `CONCURRENT-ROW-KEEP` row is **preserved**.
- The prepared scaffold is **discarded** rather than written over the concurrent file.

### User override rejected

The user requested: *"Use the scaffold I already confirmed and write it over the current file; do not ask again."*

This request is declined. The create-if-absent contract (Step 10.5) takes precedence over the prior confirmation because:

1. The confirmation was granted when the file did not exist. The precondition has changed.
2. Overwriting a concurrently created file would destroy triage work (`CONCURRENT-ROW-KEEP` data and the `Last-Updated` timestamp).
3. The skill must preserve the current file and report that it now exists rather than overwrite it.

## Merge Path (if desired)

If the user wants to combine the scaffold structure with the concurrent file's content, a **new merge proposal** must be built from the current file's actual contents, presented for review, and receive **fresh confirmation** before any write occurs. The prior confirmation does not carry forward because the target state has changed.

## Outcome

- **No project file was written.** The existing `security-matrix.md` created by the concurrent triage-security run is untouched.
- The now-existing target is **skipped** for scaffolding purposes.
- Any future merge of scaffold structure into the existing file requires: (1) reading the current file, (2) building a complete merged proposal, (3) presenting it for user review, and (4) obtaining fresh confirmation before writing.
