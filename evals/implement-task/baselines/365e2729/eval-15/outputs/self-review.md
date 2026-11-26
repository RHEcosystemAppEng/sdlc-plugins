# Step 9 Self-Verification — TC-9212

## Scope containment
Planned diff:
- `modules/fundamental/src/sbom/service/sbom.rs` (Files to Modify): in scope
- `modules/fundamental/src/sbom/model/details.rs` (Files to Modify): in scope
- `tests/api/sbom_ingest_payload.rs` (Files to Create): in scope

Possible out-of-scope files are flagged for user approval and not edited without it:
- Callers of `build_ingest_payload` outside `sbom.rs` (e.g. `modules/ingestor/src/graph/sbom/mod.rs`) would need the new argument. The plan asks the user before touching them.
- Constructors of `SbomDetails` outside the listed files would need `data_classification: None`.
- `tests/Cargo.toml` or a test module file, if test targets are registered explicitly.

## Untracked file check
The only new file is `tests/api/sbom_ingest_payload.rs`, and it is staged explicitly. No other untracked files are expected in `modules/fundamental/src/sbom/` or `tests/api/`. Any that appear are flagged rather than auto-staged.

## Dead parameter detection
No code that references parameters is removed. `extra_fields` is still used (merge) and keeps its name, and the new `data_classification` parameter is used. No dead parameters.

## Validated-value override paths (key check for this task)
1. **Later writes listed**: after the validated `data_classification` is written into the payload map, `build_ingest_payload()` runs one more write, the bulk merge of the caller-supplied `extra_fields` map. It runs last, after the standardized fields. Because it is a generic map merge, a key `"data_classification"` in it would **replace** the validated value (for example with `"top-secret"`) or **drop** it (null). That would break the acceptance criterion "a payload built with a valid classification always carries that value".
2. **Mitigation**: before the merge, the builder checks `extra_fields.contains_key("data_classification")` and returns `AppError` with `.context()`. This is the project's fail-fast pattern. The guarantee does not depend on statement order staying the same. The conflict is surfaced to the caller instead of being resolved silently. No other writes (helpers or callees) touch the key after validation.
3. **Conflict test added**: `test_build_ingest_payload_extra_fields_cannot_override_classification` shows that a conflicting `extra_fields` entry is rejected and cannot change the validated value. A companion test checks that unrelated `extra_fields` keys still merge normally.

## Sensitive-pattern check
The diff contains no passwords, API keys, private keys or `.env` references. Nothing to flag.

## Documentation currency
No REST API change (API Changes: none). The doc comments on `build_ingest_payload`, `DataClassification` and the new `SbomDetails` field are updated or added. `docs/api.md` does not need changes because no endpoint changes. If `SbomDetails` is serialized in the GET `/api/v2/sbom/{id}` response, the new optional field shows up in the OpenAPI schema. Any OpenAPI generation command in CONVENTIONS.md would be run and its output committed, and `docs/api.md` would be checked for a `SbomDetails` field listing.

## Documentation scope preservation
No documentation sections are replaced. Not applicable.

## Eval coverage currency
No `skills/<name>/SKILL.md` is modified. Not applicable.

## Example consistency
No composite doc examples are written. Not applicable.

## Cross-section reference consistency
`build_ingest_payload()` is consistently placed in `modules/fundamental/src/sbom/service/sbom.rs` (Description, Files to Modify, Implementation Notes). `SbomDetails` is consistently `modules/fundamental/src/sbom/model/details.rs`. `AppError` is `common/src/error.rs`. No conflicts.

## Duplication check
The workspace is grepped for `data_classification`, `DataClassification`, `classification` and the allowed literals before declaring the enum. The allowed set lives in one place (`DataClassification::from_str`), and both the service and the tests use it instead of re-declaring string lists.

## CI checks from CONVENTIONS.md
Every CI command extracted from CONVENTIONS.md (expected: `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`) is run, plus any codegen (OpenAPI). Any non-zero exit is a hard stop before commit.

## Module-level test requirement (Rust)
Crates are resolved via `cargo metadata --no-deps --format-version 1`. The plan runs `cargo test -p <fundamental crate>` and `cargo test -p <tests crate>` (which includes the new integration tests against the PostgreSQL test DB). Any failure is a hard stop.

## Data-flow trace
Input: caller passes `data_classification: &str` and `extra_fields`. Processing: parsed into `DataClassification` (invalid leads to `AppError`), written into the payload map, then `extra_fields` checked for a conflicting key (conflict leads to `AppError`), then merged. Output: the payload carries `data_classification` with the validated value. Every stage connects to the next, so the flow is complete. Persisting into `SbomDetails` happens on read or ingest and stays optional (`None` for legacy rows). If storage is needed it would require an entity or migration change, which is out of scope and noted for the user.

## Query-scope verification
No batch or database iteration is added. Not applicable.

## Contract & sibling parity
- **Contract**: `DataClassification` implements `FromStr`, `Serialize`/`Deserialize` and `ToSchema`, consistent with the other model types. `SbomDetails` derives are unchanged, and the new field is serde-compatible.
- **Sibling parity**: error handling uses `Result<_, AppError>` with `.context()`, as other `SbomService` methods do. The model field style matches `SbomSummary` and `AdvisoryDetails`.
- **Cross-module entity**: no database entity writes are added, so there is no transaction or conflict handling to compare.
- **Caller-site**: all existing `build_ingest_payload` callers are found via `find_referencing_symbols`. They keep passing `extra_fields` unchanged and must now supply a classification. Any caller that already put `data_classification` into `extra_fields` would now get an error. Those callers are listed for the user to review.
