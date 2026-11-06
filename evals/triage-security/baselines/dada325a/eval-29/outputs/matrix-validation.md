# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812, quinn-proto)
**Template**: `docs/templates/security-matrix.template.md`
**Matrix source**: `security-matrix-mock.md` (contains two stream matrices)

## Template-derived checks

- **Required section headings** (enforced):
  - `## Supportability Matrix`
  - `### Source Pinning Method`
  - `## Ecosystem Mappings`
  - `## Forward Pointer`
- `## Version Stream` — informational, not enforced.
- `#### Container Images` — level-4 heading, not part of the required `##`/`###` set.
- **Expected Ecosystem Mappings columns** (exact names, exact order):
  `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Supportability Matrix columns**: product-specific; only parsability is checked.

---

## Stream 2.1.x — `rhtpa-release.0.3.z`

| Check | Result | Details |
|---|---|---|
| `## Supportability Matrix` present | PASS | Found |
| `### Source Pinning Method` present | PASS | Found |
| `## Ecosystem Mappings` present | PASS | Found |
| `## Forward Pointer` present | PASS | Found (`Next stream: 2.2.x at git.example.com/rhtpa/rhtpa-release.0.4.z`) |
| Ecosystem Mappings columns | PASS | Actual: `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch`. Matches the template exactly, in order, with no extra whitespace |
| Supportability Matrix parsable | PASS | Header (`Version \| Build \| Build Date \| backend \| Notes`), separator row, 2 data rows (2.1.0, 2.1.1) |
| Ecosystem Mappings parsable | PASS | Header, separator row, 2 data rows (Cargo, RPM) |

**Auto-repairs**: none needed
**Warnings**: none
**Outcome**: **Pass**. Proceeds silently and is included in aggregation.

---

## Stream 2.2.x — `rhtpa-release.0.4.z`

| Check | Result | Details |
|---|---|---|
| `## Supportability Matrix` present | PASS | Found |
| `### Source Pinning Method` present | PASS | Found |
| `## Ecosystem Mappings` present | PASS | Found |
| `## Forward Pointer` present | PASS | Found (`This is the latest stream — no forward pointer.`) |
| Ecosystem Mappings columns | PASS | Actual: `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch`. Matches the template exactly, in order, with no extra whitespace |
| Supportability Matrix parsable | PASS | Header (`Version \| Build \| Build Date \| backend \| Notes`), separator row, 5 data rows (2.2.0 through 2.2.4) |
| Ecosystem Mappings parsable | PASS | Header, separator row, 2 data rows (Cargo, RPM) |

**Auto-repairs**: none needed
**Warnings**: none
**Outcome**: **Pass**. Proceeds silently and is included in aggregation.

---

## Summary

| Stream | Matrix | Result | Auto-repairs | Warnings | Included in aggregation |
|---|---|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | Pass | 0 | 0 | Yes |
| 2.2.x | rhtpa-release.0.4.z | Pass | 0 | 0 | Yes |

Both matrices pass validation, so there is no user prompt (no continue/abort choice is needed).
No local matrix file was written or changed during validation.
Aggregated working matrix: 7 product versions (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4).

### Informational notes (not enforced by Step 2.1.1)

- The Supportability Matrix first column is `Version`, but the template uses `Product Version`. The skill does not check Supportability Matrix column names because they are product-specific, so this is not a warning.
- Neither matrix has a `#### Container Images` subsection. This does not affect format validation. It is relevant to the on-demand matrix population check that follows Step 2.1.1.
- The Version Streams table in the project CLAUDE.md has no `Security Matrix Path` column. For this eval, both stream matrices were loaded from the supplied mock file.
- Both matrices use the shared `Last-Updated: 2026-06-28T10:00:00Z` timestamp. Staleness is evaluated in Step 0.3, not here.
