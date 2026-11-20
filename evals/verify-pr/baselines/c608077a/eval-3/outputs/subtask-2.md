# Sub-task 2 (proposed; not created in Jira, offline eval)

- **Issue Type:** Sub-task
- **Parent:** TC-9103
- **Summary:** Add include_deleted support to GET /api/v2/sbom/{id}
- **Labels:** `ai-generated-jira`, `review-feedback`
- **Link:** this sub-task Blocks TC-9103
- **Source:** the Intent Alignment sub-agent's `create-sub-task` action. Scope Containment FAILED because `modules/fundamental/src/sbom/endpoints/get.rs`, which TC-9103's Files to Modify requires, is not changed. Review comment 30004 (a question) raised the same issue.

---

## Repository
trustify-backend

## Target Branch
main

## Description
TC-9103 says a soft-deleted SBOM is hidden from normal queries but "remains accessible via direct GET with a `?include_deleted=true` parameter". It lists `modules/fundamental/src/sbom/endpoints/get.rs` under Files to Modify. PR #744 does not change `get.rs`, so `GET /api/v2/sbom/{id}` ignores `deleted_at` and returns soft-deleted SBOMs unconditionally. This task adds an `include_deleted` query parameter to the direct GET endpoint:
- Without the parameter (or with `include_deleted=false`), the endpoint returns 404 for a soft-deleted SBOM.
- With `include_deleted=true`, it returns the soft-deleted SBOM.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/get.rs` — accept an optional `include_deleted` query parameter and return 404 for soft-deleted SBOMs unless it is `true`
- `modules/fundamental/src/sbom/service/sbom.rs` — let the fetch path optionally exclude soft-deleted SBOMs, without breaking the DELETE handler's 409 check
- `tests/api/sbom_delete.rs` — add tests for direct GET of soft-deleted SBOMs

## API Changes
- `GET /api/v2/sbom/{id}` — MODIFY: add optional query parameter `include_deleted` (bool, default `false`). A soft-deleted SBOM returns 404 unless `include_deleted=true`.

## Implementation Notes
- Use the same pattern PR #744 introduced in `modules/fundamental/src/sbom/endpoints/list.rs`: an `include_deleted: Option<bool>` field on a `Deserialize` params struct, extracted with `Query(params)` and defaulted with `params.include_deleted.unwrap_or(false)`.
- Filter on `sbom::Column::DeletedAt.is_null()` when soft-deleted rows should be excluded. This mirrors `SbomService::list` in `modules/fundamental/src/sbom/service/sbom.rs`.
- `delete_sbom` (`modules/fundamental/src/sbom/endpoints/mod.rs`) relies on `SbomService::fetch` returning soft-deleted SBOMs so it can return 409. Do not change the default behavior of `fetch` used by the DELETE handler. Either add a parameter or a separate method, or apply the filter in the GET handler.
- Return `AppError::NotFound` (`common/src/error.rs`) for an excluded soft-deleted SBOM, and keep `.context()` error wrapping as the project's error-handling convention requires.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs::SbomListParams` — existing `include_deleted: Option<bool>` query-parameter pattern
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::list` — existing `DeletedAt.is_null()` filtering logic
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::fetch` — the fetch method used by the GET and DELETE handlers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}` returns 404 for a soft-deleted SBOM when `include_deleted` is absent or `false`
- [ ] `GET /api/v2/sbom/{id}?include_deleted=true` returns 200 with the soft-deleted SBOM
- [ ] `GET /api/v2/sbom/{id}` behaves as before for SBOMs that are not deleted
- [ ] `DELETE /api/v2/sbom/{id}` still returns 409 for an already-deleted SBOM

## Test Requirements
- [ ] Test that direct GET of a soft-deleted SBOM without `include_deleted` returns 404
- [ ] Test that direct GET of a soft-deleted SBOM with `include_deleted=true` returns 200 and the SBOM
- [ ] Existing tests in `tests/api/sbom_delete.rs` and `tests/api/sbom.rs` keep passing

## Review Context
- **Origin:** a verify-pr Scope Containment finding. TC-9103 Files to Modify lists `modules/fundamental/src/sbom/endpoints/get.rs — add include_deleted parameter support`, and the file is missing from PR #744's diff.
- **Related reviewer question (comment 30004, reviewer-a), `modules/fundamental/src/sbom/endpoints/get.rs`, line 1:**
  > Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Dependencies
- None
