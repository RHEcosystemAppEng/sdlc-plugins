# Step 2.1.1 — Matrix Format Validation (TC-8001)

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Stream under validation**: 2.2.x (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
**Matrix file**: `security-matrix-no-forward-pointer-mock.md` (stands in for the 2.2.x stream's `security-matrix.md`)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Matrix Last-Updated**: 2026-06-28T10:00:00Z

> Note: the Security Configuration Version Streams table in the project CLAUDE.md has no
> `Security Matrix Path` column, so the matrix path was taken from the eval fixture.
> In a live run, a missing path means asking the user which matrix to use (or falling back to the Konflux repo).

## Template extraction

**Required section headings** (`##` and `###` headings in the template, not counting the informational `## Version Stream`):

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

(`#### Container Images` is a level-4 heading. Step 2.1.1 does not enforce it. Gaps in Container Images coverage are handled by on-demand matrix population, not by format validation.)

**Ecosystem Mappings columns (expected)**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Check 1 — Required sections present

| Required Section | Present in Matrix | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | **No** | **MISSING (auto-repairable)** |
| `## Version Stream` (informational, not enforced) | Yes | n/a |

## Check 2 — Ecosystem Mappings column structure

- Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- Actual:   `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- Column count: 5 / 5, same order, no extra whitespace in the headers.
- Result: **PASS**

## Check 3 — Table parsability

| Table | Header Row | Separator Row (`---`) | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | Yes | 2 (2.2.0, 2.2.1) | PASS |
| Ecosystem Mappings | Yes | Yes | 1 (Cargo / backend) | PASS |

The Supportability Matrix columns are product-specific, so only parsability is checked, not the column names.

## Auto-repair

**Issue detected**: missing `## Forward Pointer` section.

**Repair (prepared in memory, with no in-place change during validation)**: append this section to the end of the proposed matrix:

```markdown

## Forward Pointer

None
```

The content is `None`, as the rule requires. 2.2.x is the latest configured stream (the Version Streams table lists 2.1.x and 2.2.x), so there is no next-stream matrix to point to.

**Log**:

> Auto-repaired: appended missing Forward Pointer section to `security-matrix-no-forward-pointer-mock.md`.

**Write safety (Local matrix write safety)**:
1. Snapshot: the exact matrix contents loaded above (Last-Updated 2026-06-28T10:00:00Z).
2. Right before writing, re-read the target and compare its full contents with the snapshot.
3. If unchanged: write the repaired matrix, then update `Last-Updated` only after the write succeeds.
4. If changed: keep the current file, and either ask for a fresh review of a full merge or abort the repair write. Never overwrite a stale snapshot.

(In this eval, no write was made to the fixture file. The repair is recorded here only.)

### Repaired matrix (proposed contents)

```markdown
<!-- Last-Updated: 2026-06-28T10:00:00Z -->   (timestamp is updated only after a permitted write succeeds)

# Stream 1: rhtpa-release.0.4.z (2.2.x stream)

## Version Stream

This Konflux release repo covers the **2.2.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.8`)

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Forward Pointer

None
```

## Warnings (non-repairable)

None. No critical sections are missing, the Ecosystem Mappings columns match, and no table is malformed.

## Validation result

**Status: REPAIRED**

- Auto-repairs performed: 1 (appended missing `## Forward Pointer` section with content `None`).
- Warnings: 0.
- Per the Step 2.1.1 rules, a Repaired result is reported and triage **continues without prompting the user**, provided the write-safety re-read finds the file unchanged.
- The 2.2.x stream (versions 2.2.0 and 2.2.1) goes into the aggregated working matrix for Step 2 version impact analysis of quinn-proto (fixed in 0.11.14) through the Cargo / backend / `Cargo.lock` mapping.
