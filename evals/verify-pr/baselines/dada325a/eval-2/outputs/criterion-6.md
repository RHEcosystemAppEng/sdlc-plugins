# Criterion 6 — PASS

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## What was checked

Whether the SBOM lookup at the start of `advisory_summary` was changed.

## Findings

- The diff leaves the SBOM lookup alone: `SbomService::new(&db).fetch(sbom_id.id)`. The lines after it are context lines (the diff elides them). The lookup still runs before any threshold handling, so a missing SBOM still exits early through the existing `AppError` path, as before.
- The new `Query(params)` extractor has only optional fields, so it cannot cause a different error before the lookup runs.
- The existing 404 behaviour is therefore unchanged.

## Caveat

The Test Requirements include "Test non-existent SBOM ID returns 404". No such test was added, because the test file `tests/api/advisory_summary.rs` was not created. This is a gap in test coverage, not a failure of this criterion.

## Verdict

PASS. The existing 404 behaviour is unchanged, but it is not tested.
