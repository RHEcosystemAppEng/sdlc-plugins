## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory model structs (`AdvisorySummary` and `AdvisoryDetails`) to use the new `status` enum field directly instead of deriving the status from a join with the `advisory_status` table. The models should expose the status as a string (matching the current API response shape) by converting the enum variant to its string representation.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` to source the `status` field from the advisory entity's enum column instead of joining `advisory_status`; remove any `advisory_status` join logic in the `From` or constructor implementation
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` to source the `status` field from the advisory entity's enum column instead of joining `advisory_status`
- `modules/fundamental/src/advisory/model/mod.rs` -- remove any re-export or reference to `advisory_status` types if present

## Implementation Notes
- The `AdvisorySummary` struct currently includes a `status` field populated via a join. Replace the join-based population with direct field access from the advisory entity's `status: AdvisoryStatusEnum` field.
- Convert the enum to a string using `.to_string()` or a match expression to maintain the same API response shape (status is still a string in the JSON response).
- Follow the pattern used in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for struct field population from entity data.
- The `PaginatedResults<AdvisorySummary>` response wrapper in `common/src/model/paginated.rs` does not need changes -- it is generic over `T`.
- Per docs/constraints.md section 2 (Commit Rules): commit messages must follow Conventional Commits format, reference TC-9005 in the footer, and include the `--trailer="Assisted-by: Claude Code"`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- reference for model struct population pattern from SeaORM entities
- `entity/src/advisory.rs::AdvisoryStatusEnum` -- the new enum type defined in Task 3

## Acceptance Criteria
- [ ] `AdvisorySummary` populates `status` from the advisory entity's enum field, not from a join
- [ ] `AdvisoryDetails` populates `status` from the advisory entity's enum field, not from a join
- [ ] No remaining references to `advisory_status` entity or join in the model layer
- [ ] The API response shape for advisory list and detail endpoints is unchanged (status is still a string)

## Test Requirements
- [ ] Verify model construction from an advisory entity with each enum variant produces the correct string status
- [ ] Verify the JSON serialization of `AdvisorySummary` and `AdvisoryDetails` matches the existing format

## Verification Commands
- `cargo check -p fundamental` -- fundamental module compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions
