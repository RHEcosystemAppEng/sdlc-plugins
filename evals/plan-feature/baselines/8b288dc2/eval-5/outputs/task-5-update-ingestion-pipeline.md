# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. This simplifies the ingestion path by removing the lookup table write and the FK reference step.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert + FK assignment with direct enum value assignment on advisory insert; remove any references to `advisory_status` entity or table

## Implementation Notes
- The current ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` likely: (1) checks if the status exists in `advisory_status` table, (2) inserts it if not, (3) uses the returned ID as `status_id` on the advisory row. Replace this with: (1) map the status string from the feed to the `AdvisoryStatusEnum` variant, (2) set `status` directly on the advisory `ActiveModel`
- Use the `AdvisoryStatusEnum` type defined in `entity/src/advisory.rs` (from Task 3) for the enum mapping
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` as a reference for the `ActiveModel` insert pattern without lookup tables
- Error handling: if the status string from the feed does not match a known enum variant, return an `AppError` with context rather than silently defaulting — per the error handling pattern in `common/src/error.rs`
- The `IngestorService` in `modules/ingestor/src/service/mod.rs` may also reference advisory status — check and update if needed

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference implementation for ingestion without lookup table indirection
- `entity/src/advisory.rs` — `AdvisoryStatusEnum` type for enum value mapping
- `common/src/error.rs` — `AppError` for error handling when status string is invalid

## Acceptance Criteria
- [ ] Advisory ingestion writes enum value directly to `advisory.status` column
- [ ] No writes to `advisory_status` lookup table occur during ingestion
- [ ] All four status values (New, Analyzing, Fixed, Rejected) are correctly mapped from feed input to enum variants
- [ ] Invalid status strings from feed input produce a clear error instead of silent failure

## Test Requirements
- [ ] Ingestion of an advisory with status "New" correctly sets the enum value
- [ ] Ingestion of an advisory with status "Fixed" correctly sets the enum value
- [ ] Ingestion of an advisory with an invalid status string returns an appropriate error

## Verification Commands
- `cargo check -p trustify-module-ingestor` — ingestor module compiles
- `cargo test -p trustify-module-ingestor -- advisory` — advisory ingestion tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

---
Description Digest: sha256-md:ae5015c08bf8ff926117f88d62afdac1037285a3a2d54db7c98226cf6bb34930
Priority: High
Fix Versions: RHTPA 2.0.0
