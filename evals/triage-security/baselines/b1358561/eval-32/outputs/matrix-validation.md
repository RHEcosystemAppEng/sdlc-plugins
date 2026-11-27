# Step 2.1.1 — Matrix Format Validation: TC-8001

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Stream**: 2.2.x (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
**Matrix file**: `security-matrix-no-forward-pointer-mock.md` (stands in for the stream's `security-matrix.md`)
**Template**: `docs/templates/security-matrix.template.md`
**Mode**: Interactive (simulated; no Jira, git, or external calls made)

> Pre-step note (Step 0.3 staleness): the matrix has `Last-Updated: 2026-06-28T10:00:00Z`,
> which is 152 days before today (2026-11-27). That is over the 14-day threshold, so a real
> run would warn and offer Refresh / Proceed / Stop. For this eval I assume **Proceed anyway**
> so that format validation can be shown.
>
> Configuration note: the Security Configuration Version Streams table in the mock CLAUDE.md
> has no `Security Matrix Path` column. The supplied fixture file is used as the matrix for
> the 2.2.x stream.

## Template extraction

**Required section headings** (`##`/`###` from the template, minus the informational `## Version Stream`):

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

(`#### Container Images` is a level-4 heading, so it is not part of the Step 2.1.1 required-heading set. Container Images coverage is handled by on-demand matrix population.)

**Ecosystem Mappings columns** (expected, in order):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Check 1 — Required sections present

| Required Section | Present in Matrix | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | **No** | **MISSING — auto-repairable** |
| `## Version Stream` (informational, not enforced) | Yes | n/a |

## Check 2 — Ecosystem Mappings column structure

- Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- Actual:   `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- Result: **PASS** (same names, same order, no extra whitespace to normalize)

## Check 3 — Table parsability

| Table | Header Row | Separator Row (`---`) | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | `Version \| Build \| Build Date \| backend \| Notes` | Yes | 2 (2.2.0, 2.2.1) | PASS |
| Ecosystem Mappings | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | Yes | 1 (Cargo / backend) | PASS |

Supportability Matrix column names depend on the product (here `Version` rather than the template's `Product Version`), so the step checks only that the table parses, not the column names.

## Auto-repairs

| # | Issue | Repair |
|---|---|---|
| 1 | Missing `## Forward Pointer` section | Append `## Forward Pointer` with content `None` to the end of the proposed matrix |

Log:

> Auto-repaired: appended missing Forward Pointer section to `security-matrix-no-forward-pointer-mock.md`.

The repair is built in memory first. The source matrix is not edited during validation.

### Proposed repaired matrix (tail)

```markdown
## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Forward Pointer

None
```

### Local matrix write safety (applied to the repair write)

1. Snapshot: the full fixture contents as read for validation.
2. Immediately before writing, re-read the target and compare it in full with the snapshot.
3. If the contents are unchanged, write the repaired matrix, then update `Last-Updated`, but only after the write succeeds.
4. If the contents changed, keep the current file and ask for renewed review, or abort. Never overwrite a stale snapshot.

In this eval the input fixture is **not** changed. The repair is recorded here only.

## Warnings (non-repairable)

None. Both critical sections are present (Supportability Matrix, Ecosystem Mappings), the Ecosystem Mappings columns match, and both tables parse.

## Validation result

**Status: REPAIRED**

- 1 auto-repair: appended the missing `## Forward Pointer` section with content `None`.
- 0 warnings.
- Per Step 2.1.1, a Repaired result is reported and triage continues **without a user prompt**.
- Stream 2.2.x is **included** in the aggregated working matrix (versions 2.2.0 → backend `v0.4.5`, 2.2.1 → backend `v0.4.8`; Cargo lock file `Cargo.lock`, upstream branch `release/0.4.z`). It then goes on to Step 2.2+ for the quinn-proto (< 0.11.14) impact check.
