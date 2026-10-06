# Task 5 — Update advisory ingestion pipeline for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline must map incoming status strings from advisory feeds to the corresponding `AdvisoryStatusEnum` variant and set the enum value on the advisory row during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert + FK assignment with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants; remove any references to `advisory_status` entity
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references `advisory_status` in the ingestion flow

## Implementation Notes
- In the advisory ingestion handler, replace the pattern of:
  1. Insert status into `advisory_status` table
  2. Get the inserted `status_id`
  3. Set `advisory.status_id = status_id`
  
  With the simpler pattern of:
  1. Map the status string to `AdvisoryStatusEnum` variant
  2. Set `advisory.status = AdvisoryStatusEnum::from_str(status_string)`
- Implement a mapping function from raw status strings to `AdvisoryStatusEnum`:
  ```rust
  fn map_status(raw: &str) -> Result<AdvisoryStatusEnum, AppError> {
      match raw {
          "New" | "new" => Ok(AdvisoryStatusEnum::New),
          "Analyzing" | "analyzing" => Ok(AdvisoryStatusEnum::Analyzing),
          "Fixed" | "fixed" => Ok(AdvisoryStatusEnum::Fixed),
          "Rejected" | "rejected" => Ok(AdvisoryStatusEnum::Rejected),
          _ => Err(AppError::BadRequest(format!("Unknown advisory status: {}", raw))),
      }
  }
  ```
- Handle unknown status values gracefully — log a warning and return an error rather than panicking
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping for error propagation in the ingestion pipeline.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's handler file scope.

### Constraints (from docs/constraints.md)
- §2.1: Every commit MUST reference Jira issue ID in the footer
- §2.2: Commit messages MUST follow Conventional Commits (`refactor(ingestor): ...`)
- §2.3: Every commit MUST include `--trailer="Assisted-by: Claude Code"`
- §5.1: Changes MUST be scoped to the files listed in Files to Modify
- §5.3: Implementation MUST follow the patterns referenced in Implementation Notes
- §5.6: Each new feature MUST be traced through its complete data-flow lifecycle

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — existing SBOM ingestion module showing the project's ingestion pattern (parse, store, link)
- `common/src/error.rs` — `AppError` enum for error handling in ingestion failures
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3 that this task will use for status mapping

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to `advisory.status` column
- [ ] No references to `advisory_status` lookup table remain in the ingestion pipeline
- [ ] Status string mapping handles all four valid values: `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] Unknown status strings produce a descriptive error (not a panic)
- [ ] Ingestion of advisory feeds with various status values succeeds end-to-end

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" sets `advisory.status` to `AdvisoryStatusEnum::New`
- [ ] Verify ingestion of an advisory with status "Fixed" sets `advisory.status` to `AdvisoryStatusEnum::Fixed`
- [ ] Verify ingestion with an unknown status value returns an appropriate error
- [ ] Verify the complete ingestion data-flow: parse advisory feed -> map status -> insert advisory row with enum status

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status
