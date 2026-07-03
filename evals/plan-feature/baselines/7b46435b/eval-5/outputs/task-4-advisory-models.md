# Task 4 — Update advisory model structs for direct enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the `AdvisorySummary` and `AdvisoryDetails` model structs to use the advisory status enum directly from the entity instead of resolving status through a join with the `advisory_status` lookup table. The status field should be populated from the advisory entity's `status` enum column, eliminating the need for a separate status resolution step.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to use enum status field; remove any status join/resolution logic in the `From` impl or constructor
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to use enum status field; remove any status join/resolution logic
- `modules/fundamental/src/advisory/model/mod.rs` — update module-level re-exports or shared types if they reference advisory_status

## Implementation Notes
- The `AdvisorySummary` struct likely has a `status: String` field populated by joining the `advisory_status` table — replace the join-based population with direct access to the advisory entity's `status` enum field, converting to string via `.to_string()` or serde serialization
- The `AdvisoryDetails` struct follows the same pattern — update its `From` impl or constructor to read `status` directly from the advisory entity model
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` for struct definition and `From` implementation style
- The API response shape must remain identical — status is still a string in the JSON response. Use serde's string serialization on the enum or explicit `.to_string()` conversion
- Error handling: maintain `Result<T, AppError>` with `.context()` wrapping per project convention

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs` — reference model struct pattern for `From` impl and field mapping
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3 that provides the status values

## Acceptance Criteria
- [ ] `AdvisorySummary` struct populates status from the advisory entity's enum column without any join
- [ ] `AdvisoryDetails` struct populates status from the advisory entity's enum column without any join
- [ ] Status values in API responses remain unchanged (still string representations: "New", "Analyzing", "Fixed", "Rejected")
- [ ] No references to `advisory_status` table or entity remain in the model layer

## Test Requirements
- [ ] Verify model structs compile with the updated entity dependency: `cargo check -p fundamental`
- [ ] Verify `AdvisorySummary::from()` correctly converts the enum status to a string matching the original format
- [ ] Verify `AdvisoryDetails::from()` correctly converts the enum status to a string matching the original format

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
