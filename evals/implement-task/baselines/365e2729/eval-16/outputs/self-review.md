# Step 9 Self-Verification — TC-9213

These checks were applied to the planned change; nothing was actually executed.

## Scope containment
- Planned `git diff --name-only`:
  - `modules/fundamental/src/advisory/model/summary.rs` (Files to Modify)
  - `modules/fundamental/src/advisory/service/advisory.rs` (Files to Modify)
  - `tests/api/advisory_summary.rs` (Files to Create)
- All three files are in scope.
- Possible flags, if they turn up during implementation, each needing user approval before commit:
  - (a) a caller of `build_summary()` outside the listed files that needs the new argument;
  - (b) a registration entry for the new test file (in `tests/Cargo.toml` or a test `mod` file);
  - (c) a regenerated OpenAPI spec.
- None of these are planned as edits without approval.

## Untracked file check
- The only new file is `tests/api/advisory_summary.rs`. It is staged on purpose.
- No other untracked files are expected in `advisory/model/`, `advisory/service/` or `tests/api/`.
- Any that do appear and are referenced by the diff would be flagged, not staged automatically.

## Dead parameter detection
- No code is removed. `build_summary()` gains a parameter and loses none, so no dead parameters are introduced. Not applicable.

## Validated-value override paths
1. **Later writes listed.** After the validated `risk_classification` is assigned, `build_summary()` only finishes the field-by-field population of `AdvisorySummary` and returns it. The Implementation Notes say it performs no further merge, bulk update or generic write, and the plan confirms this with `find_symbol(..., include_body=true)`. No later write in the function or its immediate callees touches the struct after it is built. There are no extra-field maps, defaults merges, `..Default::default()` / struct-update spreads or patch helpers.
2. **Nothing can replace the value.** The only assignment to `risk_classification` is the validated one. No generic path exists that could overwrite or drop it.
3. **Conflict test.** None is required, because no override path exists. The plan adds no override-conflict test and no artificial test seam (such as an extra-fields parameter) just to show a conflict the function cannot express.
   - The happy-path test asserts each of the four allowed values lands in the summary.
   - The rejection test covers the invalid input.
   - Together these cover both acceptance criteria.
- Re-check: if the existing struct literal uses `..base` / `..Default::default()` struct-update syntax, the explicitly named field takes precedence in Rust, so the validated value still holds.

## Sensitive-pattern check
- The planned diff has no passwords, API keys, private keys or `.env` references. The `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` check would return nothing.

## Documentation currency
- No endpoint, configuration or setup changes.
- If `AdvisorySummary` is serialized in `/api/v2/advisory` responses, `docs/api.md` (and the generated OpenAPI spec) would need the new `risk_classification` field and its four allowed values. That would be flagged as a doc file outside the listed scope for user approval.
- Otherwise no doc update is needed.

## Documentation scope preservation
- No documentation sections are replaced. Not applicable.

## Eval coverage currency
- No `skills/<name>/SKILL.md` is modified. Not applicable.

## Example consistency
- No documentation with composite examples is written. Not applicable.

## Cross-section reference consistency
- `AdvisoryService::build_summary()` points to `modules/fundamental/src/advisory/service/advisory.rs` in both Files to Modify and Implementation Notes.
- `AdvisorySummary` points to `modules/fundamental/src/advisory/model/summary.rs` in Files to Modify, which is consistent with "model/" in Implementation Notes and with the repo tree.
- `AppError` is in `common/src/error.rs`, which matches the repo tree.
- No inconsistencies.

## Duplication check
- The plan searches the `fundamental` and `common` crates for an existing risk/severity enum, allowed-values constant or validation helper.
  - If one exists with the same value set, it is reused (made `pub` if needed, since `fundamental` already depends on `common`).
  - If not, the allowed set is defined once, as `RiskClassification` plus `FromStr`. The tests reuse that type instead of a duplicated string list.

## CI checks from CONVENTIONS.md
- Every CI command extracted from `CONVENTIONS.md` is run in order, for example `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings` and `cargo check`.
- Any code generation command (such as OpenAPI generation) is run, and its output is staged if it changed.
- Any non-zero exit is a hard stop before Step 10.

## Module-level test requirement (Rust)
- `cargo metadata --no-deps --format-version 1` resolves the packages:
  - `modules/fundamental/...` belongs to the `fundamental` crate (the package name comes from the metadata, for example `trustify-module-fundamental`);
  - `tests/api/advisory_summary.rs` belongs to the `tests` package.
- Then run `cargo test -p <fundamental-pkg>` and `cargo test -p <tests-pkg>` (or `cargo nextest run -p ...`). These need the PostgreSQL test DB.
- Any failure is a hard stop.

## Data-flow trace
- Flow: caller passes a `risk_classification` string → `build_summary()` validates it with `RiskClassification::from_str` → on success the typed value is assigned to `AdvisorySummary.risk_classification` → the struct is returned (and serialized through serde if an endpoint exposes it).
- On failure: `AppError` with `.context()` → `Err` returned → `IntoResponse` maps it to an error status.
- Every stage connects to the next. The path is complete.

## Query-scope verification
- No batch operation or database iteration is added. Not applicable.

## Contract & sibling parity
- **Contract**: `RiskClassification` implements `FromStr` with the standard `Err` associated type. `AdvisorySummary` keeps all its existing derives (`Serialize`, `Deserialize`, `ToSchema`, etc.), and the new enum derives the same ones so the struct still compiles and has a schema.
- **Sibling parity**: the model change matches `SbomSummary` and `PackageSummary` (a doc-commented pub field, snake_case naming, the same serde/utoipa derives). The service validation uses `Result<T, AppError>` and `.context()`, like the other service methods.
- **Cross-module entity**: no database entity is written. The new field is computed and not persisted. Not applicable.
- **Caller-site**: every caller of `build_summary()` (found with `find_referencing_symbols`) is updated to pass the classification and propagate the `Result` with `?`, the same way the other service-call sites do. Callers outside the listed scope are flagged.

## Result
All applicable checks pass for the planned change. The commit can go ahead once any out-of-scope flags above are approved, if they come up.
