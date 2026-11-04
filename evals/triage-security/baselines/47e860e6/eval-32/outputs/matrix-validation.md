# Step 2.1.1 — Matrix Format Validation: TC-8001

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (not Fullsend; no `triage-security-input.json` bundle supplied)
**Canonical template**: `docs/templates/security-matrix.template.md`

## Matrix Under Validation

| Stream | Konflux Release Repo | Matrix File | Last-Updated |
|--------|----------------------|-------------|--------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | `security-matrix-no-forward-pointer-mock.md` (eval fixture standing in for the stream's `security-matrix.md`) | 2026-06-28T10:00:00Z |

Notes:
- The mock CLAUDE.md Version Streams table has no **Security Matrix Path** column, so the
  supplied fixture is treated as the 2.2.x stream's matrix. The 2.1.x stream
  (rhtpa-release.0.3.z) has no matrix fixture, so it is out of scope for this validation.
  In a live run its matrix would be read through the Konflux `git show` fallback.
- The issue summary names `[rhtpa-2.2]`, which maps to the 2.2.x stream validated here.

## Requirements Extracted from Template

**Required section headings** (all `##` and `###` headings in the template; `## Version Stream`
is informational and not enforced. `#### Container Images` is a level-4 heading, so it is not
in the required set):

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

**Ecosystem Mappings columns** (exact names and order):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Check Results

### Check 1 — Required sections present

| Required Section | Present in Matrix | Result |
|------------------|-------------------|--------|
| `## Supportability Matrix` | Yes (line 10) | PASS |
| `### Source Pinning Method` | Yes (line 17) | PASS |
| `## Ecosystem Mappings` | Yes (line 21) | PASS |
| `## Forward Pointer` | **No** | **FAIL, auto-repairable** |
| `## Version Stream` (informational) | Yes (line 6) | not enforced |

### Check 2 — Ecosystem Mappings column structure

| Position | Expected | Actual | Result |
|----------|----------|--------|--------|
| 1 | Ecosystem | Ecosystem | match |
| 2 | Repository | Repository | match |
| 3 | Lock File | Lock File | match |
| 4 | Check Command | Check Command | match |
| 5 | Upstream Branch | Upstream Branch | match |

Result: **PASS**. All 5 columns match, in the expected order, with no extra whitespace in the headers.

### Check 3 — Table parsability

| Table | Header Row | Separator Row (`---`) | Data Rows | Result |
|-------|------------|-----------------------|-----------|--------|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 (2.2.0, 2.2.1) | PASS |
| Ecosystem Mappings | Yes | Yes | 1 (Cargo / backend) | PASS |

The Supportability Matrix columns are product-specific. Only parsability is checked, not the
column names, so a first column named `Version` instead of `Product Version` is acceptable.

## Auto-Repairs

| # | Issue | Repair | Log |
|---|-------|--------|-----|
| 1 | Missing `## Forward Pointer` section | Append `## Forward Pointer` with content `None` to the end of the proposed matrix | Auto-repaired: appended missing Forward Pointer section to `security-matrix-no-forward-pointer-mock.md`. |

No column-header whitespace needed normalizing.

### Proposed repaired tail of the matrix

```markdown
## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Forward Pointer

None
```

The value `None` matches the template's guidance for the latest stream: 2.2.x is the newest
configured stream, so there is no next-stream matrix to point to.

### Write handling (Local matrix write safety)

- The repair was prepared in memory against a snapshot of the matrix as read. The matrix was
  not changed in place during validation.
- In a live run, the target would be re-read and compared with the snapshot just before the
  write. The appended section would be written only if the file is unchanged, and
  `Last-Updated` would be bumped only after that write succeeds. If the file had changed, it
  would be preserved and the repair would go back for review or be aborted.
- **In this eval, no repository file was written**, per the task constraints. The repair is
  recorded here only.

## Warnings (non-repairable)

None:
- No critical section is missing (Supportability Matrix and Ecosystem Mappings are both present).
- The Ecosystem Mappings columns are correct.
- No table is malformed.

## Validation Outcome

**Status: REPAIRED**

Only auto-fixable issues were found (1 auto-repair: the missing Forward Pointer). Per Step 2.1.1,
the repairs are reported and triage **continues without prompting the user**, and no
continue/abort choice is shown. The 2.2.x stream stays in the aggregated working matrix:

| Version | Build | Build Date | backend ref | Stream |
|---------|-------|------------|-------------|--------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | 2.2.x |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | 2.2.x |

Ecosystem used for the quinn-proto (Cargo) lookup: `Cargo.lock` in `backend`, checked with
`git show <tag>:Cargo.lock`, upstream branch `release/0.4.z`. The next step is Step 2.2 and the
version impact analysis against fix threshold `quinn-proto >= 0.11.14`.
