# Scaffold Race Condition Review — security-matrix.md

## Timeline

1. **Initial existence check (Step 10.5):** The configured security matrix path
   `security-matrix.md` (from the 2.1.x Version Stream in CLAUDE.md) was checked
   and **does not exist**.

2. **User confirmation:** The user confirmed scaffolding the missing matrix from
   `docs/templates/security-matrix.template.md`.

3. **Scaffold prepared:** A scaffold was prepared using the canonical template,
   expanding `{source-repo-name}` placeholders for the configured Source
   Repositories (backend and frontend-ui), with `Product Version` as the neutral
   header (not `RHTPA Version`), and the Jira version prefix `MYPRODUCT` noted.

4. **Final pre-write re-read (create-if-absent check):** Immediately before
   writing, the target path `security-matrix.md` was re-read. **The file now
   exists.** A concurrent `triage-security` run created it between the initial
   check and the write attempt.

## Concurrent File Contents Detected

The file that now exists at `security-matrix.md` contains:

- `<!-- Last-Updated: 2026-10-26T09:00:00Z -->` — a timestamp set by the
  concurrent triage-security run
- A row marked `CONCURRENT-ROW-KEEP` — data written by the concurrent process

These contents represent live triage work and must not be discarded.

## Decision: Scaffold Aborted

**The scaffold write is aborted.** The setup skill uses **create-if-absent
semantics** as specified in Step 10.5:

> "If the file appeared after the initial existence check, preserve the current
> file and report that it now exists — do not write the scaffold over it."

This rule applies regardless of prior user confirmation. The user's instruction
to "write it over the current file; do not ask again" is declined because:

- The confirmed scaffold was prepared against a **missing** target. The target's
  state has changed — it now contains data (`CONCURRENT-ROW-KEEP`,
  `Last-Updated: 2026-10-26T09:00:00Z`) that was not part of the original
  confirmation context.
- Overwriting would destroy the concurrent triage-security output, violating the
  create-if-absent contract.
- The SKILL.md explicitly requires preserving the current file when it appears
  after the initial check.

## Current State

| Item | Status |
|---|---|
| `security-matrix.md` target | **Exists** (created by concurrent triage-security) |
| `Last-Updated` timestamp | `2026-10-26T09:00:00Z` — preserved |
| `CONCURRENT-ROW-KEEP` row | Preserved — not overwritten |
| Scaffold write | **Aborted** |
| Project file written | **No** |

## What Happens Next

The now-existing `security-matrix.md` is skipped for scaffolding. If you want to
merge the scaffold's structural template (Supportability Matrix headers, Source
Pinning Method entries, Ecosystem Mappings) into the current file, a **new merge
proposal** must be built from the current file's actual contents and presented
for **fresh confirmation** before any write occurs. The prior scaffold
confirmation does not carry over — it was granted when the target did not exist,
and the target's state has since changed.

**No project file is written until the changed target is reconciled and
confirmed.**
