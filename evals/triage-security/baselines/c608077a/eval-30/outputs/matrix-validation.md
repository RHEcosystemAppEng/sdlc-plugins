# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (no Fullsend bundle provided)
**Canonical template**: `docs/templates/security-matrix.template.md`

## Template Requirements Extracted

**Required section headings** (`##` / `###` from template; `## Version Stream` is informational and not enforced):

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

**Expected Ecosystem Mappings columns** (exact names, in order):

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Streams Validated

| Stream | Konflux Release Repo | Matrix File |
|---|---|---|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | `security-matrix-missing-section-mock.md` |

The issue targets the 2.2.x stream (`[rhtpa-2.2]` summary suffix). Only the 2.2.x matrix was supplied for this eval; the 2.1.x stream (rhtpa-release.0.3.z) matrix was not provided and is not validated here.

## Stream 2.2.x — `security-matrix-missing-section-mock.md`

### Check 1: Required sections present

| Required Section | Status |
|---|---|
| `## Supportability Matrix` | Present |
| `### Source Pinning Method` | Present |
| `## Ecosystem Mappings` | **MISSING** (critical) |
| `## Forward Pointer` | Present |
| `## Version Stream` (informational, not enforced) | Present |

### Check 2: Ecosystem Mappings column structure

**Not evaluable.** The `## Ecosystem Mappings` section does not exist, so there is no table to compare with the expected columns `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`.

### Check 3: Table parsability

| Table | Header Row | Separator Row | Data Rows | Status |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 (2.2.0, 2.2.1) | Parsable |
| Ecosystem Mappings | — | — | — | Not evaluable (section missing) |

Supportability Matrix column names are product-specific, so they are not checked against the template. The table parses correctly.

### Auto-repair proposals

None apply. Forward Pointer is present, and no column headers have extra whitespace. A missing Ecosystem Mappings section **cannot be auto-repaired**: the ecosystem, lock file, check command, and upstream branch values are deployment-specific and must come from the user. No file was modified.

### Warnings

> ⚠️ Matrix file `security-matrix-missing-section-mock.md` is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

**Stream result: WARNING (critical). Stream 2.2.x is halted.** Without Ecosystem Mappings, triage cannot find the lock file (e.g., `Cargo.lock` for the `cargo` ecosystem that `quinn-proto` belongs to), the check command used to inspect pinned refs, or the upstream branch used to check whether a fix is available. Version lookups for 2.2.0 and 2.2.1 cannot proceed.

## Overall Validation Result

| Stream | Result | Issues |
|---|---|---|
| 2.2.x | **Warnings (critical)** | Missing required section `## Ecosystem Mappings` |

## User Prompt

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):

**If 1 (continue):** stream 2.2.x is left out of aggregation. 2.2.x is the only supplied stream and the stream this issue targets, so the aggregated working matrix would contain no versions. Version impact analysis (Step 2) for TC-8001 could not produce affected/not-affected verdicts for 2.2.0 or 2.2.1.

**If 2 (abort, recommended):** add an `## Ecosystem Mappings` section to the 2.2.x matrix that matches the template, for example:

```markdown
## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| cargo | backend | `Cargo.lock` | `git show <commit>:Cargo.lock` | `<upstream-branch>` |
```

(Values are illustrative. The engineer must confirm the actual repository short name, lock file path, and upstream branch.) Then re-run `/sdlc-workflow:triage-security TC-8001`.

## Additional Observations (outside Step 2.1.1 scope)

- **Step 0.3 staleness:** the matrix file has no `Last-Updated` timestamp. Step 0.3 would already have warned that the matrix predates staleness tracking.
- **Container Images:** the matrix has no `#### Container Images` table. This is a level-4 heading, so the 2.1.1 section check does not enforce it, but on-demand population (after 2.1.1) would flag it as missing component pairs.
- **Affects Versions:** TC-8001 lists `RHTPA 2.0.0`, which is not in the 2.2.x stream (2.2.0, 2.2.1). Correcting it depends on version impact analysis, which is blocked by the warning above.

## Actions Taken

- No Jira MCP calls, `git show` commands, or external tools were used.
- No matrix file was modified.
