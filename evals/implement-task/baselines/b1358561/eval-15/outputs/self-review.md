# Step 9 Self-Verification — TC-9212

The procedures come from `shared/self-verification.md`. Each check is marked as firing or not. Firing checks are reported as PASS or FLAGGED. This change is a plan for an eval, so commands are described as they would be run.

| # | Check | Fires? | Result |
|---|---|---|---|
| 1 | Scope containment | yes (always) | FLAGGED, conditional (see below) |
| 2 | Untracked files | yes | PASS |
| 3 | Sensitive patterns | yes (always) | PASS |
| 4 | Dead parameters | no | — |
| 5 | Duplication | yes | PASS |
| 6 | Documentation currency | yes | PASS, with an advisory |
| 7 | Documentation scope preservation | no | — |
| 8 | Eval coverage | no | — |
| 9 | Example consistency | no | — |
| 10 | Cross-section references | yes | PASS |
| 11 | Data-flow trace | yes | PASS |
| 12 | Query scope | no | — |
| 13 | Contract & sibling parity | yes | PASS |
| 14 | CI checks from CONVENTIONS.md | yes (always) | PASS (required before commit) |
| 15 | Module tests (Rust) | yes | PASS (required before commit) |
| 16 | Validated-value override paths | yes | FLAGGED, then resolved in the plan |

## 1. Scope containment — FLAGGED (conditional, needs user approval)
`git diff --name-only` is compared with Files to Modify and Files to Create.
- In scope: `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/model/details.rs`, `tests/api/sbom_ingest_payload.rs`.
- Out-of-scope files that might be needed. Each one is listed for the user to approve or revert before commit:
  - `tests/Cargo.toml` (or the `tests/api` module list), if the new test file must be registered as a test target.
  - Any file outside the two listed files that builds `SbomDetails { .. }` as a struct literal. Adding a non-`Option` field breaks those constructions. `find_referencing_symbols("SbomDetails")` lists them. To keep this set small, the field becomes `Option<DataClassification>` if such sites exist.
- Nothing is committed outside scope without explicit approval.

## 2. Untracked files — PASS
`git status --short` shows only `tests/api/sbom_ingest_payload.rs` as `??`. It is in Files to Create. No other untracked files are near the modified directories.

## 3. Sensitive patterns — PASS
`git diff HEAD | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` runs now. `git diff --cached | grep ...` runs after staging, including the new test file. The added content is enum variants, a reserved-key constant and test fixtures (`"public"`, `"scanner-x"`). Nothing matches. Note: test values such as `"secret"` as a disallowed classification don't match the pattern, and they are not credentials.

## 4. Dead parameters — does not fire
No removed lines refer to a function parameter. `extra_fields` is still used (it is checked, then merged) and keeps its name.

## 5. Duplication — PASS
I searched `common/` and `modules/` for `classification`, `Classification`, `ALLOWED_`, `RESERVED_` and for string-set validators (`matches!(.., "public" | ..)`). No existing classification enum or allowed-value validator was found, so `DataClassification` is declared in the model file that uses it (Reuse rule 3). Error construction reuses `AppError` and `.context()` from `common/src/error.rs` and adds no new error type.

## 6. Documentation currency — PASS (advisory)
No HTTP API changed, but the ingest payload shape did: there is a new `data_classification` key, and `extra_fields` now rejects a reserved key. Check `README.md`, `docs/api.md` and `docs/architecture.md`. If any of them lists ingest payload fields or describes how `extra_fields` passes through, flag it to the user as an out-of-scope doc update (check 1). It is not edited without approval.

## 7 / 8 / 9 — do not fire
No doc section was replaced, no `skills/*/SKILL.md` was changed, and no composite-example docs were modified.

## 10. Cross-section references — PASS
`sbom.rs` (`SbomService::build_ingest_payload`) uses the same path in Files to Modify and Implementation Notes. `details.rs` (`SbomDetails`) matches the "struct patterns in `modules/fundamental/src/sbom/model/`" note. `common/src/error.rs` matches the repo tree. The new test path `tests/api/` matches the existing integration-test directory. No discrepancies.

## 11. Data-flow trace — PASS
- **Input**: a raw classification string, from `SbomDetails.data_classification` or the caller, plus the caller's `extra_fields`.
- **Processing**: `DataClassification::from_str` either returns an enum value or `AppError` with context (fail-closed). Then the reserved-key check on `extra_fields` either rejects a conflicting key or passes.
- **Output**: the standardized fields are written, `data_classification` is written as the canonical lowercase string, and the unrelated `extra_fields` are merged. The payload is returned to the existing send path. On error, `?` passes `AppError` up and nothing is sent.
Every stage connects to the next. Persistence is not in scope: the task doesn't touch `entity/sbom.rs` or migrations, which the description intends.

## 12. Query scope — does not fire
There are no batch database operations.

## 13. Contract & sibling parity — PASS
- **Contract**: `FromStr::Err = AppError` matches how the trait is used. `DataClassification` derives the same set as sibling model types (`Serialize`, `Deserialize`, `ToSchema`, `Clone`, `Debug`). `build_ingest_payload` keeps its return type `Result<_, AppError>`.
- **Sibling parity**: error handling uses `.context()`, as in `advisory/service/advisory.rs` and `sbom.rs`. The model doc comments follow `summary.rs`.
- **Cross-module entity**: no DB writes, so this doesn't apply. The ingestor module, which consumes the payload, receives one more key. Its `graph/sbom/mod.rs` is checked to confirm unknown keys are tolerated or the key is expected.
- **Caller-site**: existing callers of `build_ingest_payload` already handle `Result` with `?`. The new error cases (invalid classification, reserved key) come through the same path, so callers don't change. The `extra_fields` name and type are kept, as the Implementation Notes require.

## 14. CI checks from CONVENTIONS.md — PASS (hard stop if any fail)
Run every CI command taken from `CONVENTIONS.md` in Step 4, in order (typically `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`). Run any recorded codegen command, such as OpenAPI generation, because `ToSchema` on a new enum may change the spec, and stage what it produces. Any non-zero exit stops execution and is reported to the user.

## 15. Module tests (Rust) — PASS (hard stop if any fail)
`cargo metadata --no-deps --format-version 1` maps the modified files to their packages. `modules/fundamental/src/...` maps to the fundamental crate (for example `trustify-module-fundamental`), and `tests/api/sbom_ingest_payload.rs` maps to the `tests` package. The package names come from the metadata, not from the nearest `Cargo.toml`. Run `cargo test -p <fundamental-crate>` and `cargo test -p <tests-crate>`. These need the PostgreSQL test DB, so try the run first and report clearly if the environment is unavailable.

## 16. Validated-value override paths — FLAGGED, then resolved
1. **Later writes after the validated assignment** in `build_ingest_payload()`:
   - the merge of caller-supplied `extra_fields` into the same map, which runs **last** as the Implementation Notes describe.
   - There are no other writes after it in the function. Immediate callees (the payload send/serialize step) only read the map.
2. **Can a path replace the value?** Yes. An `extra_fields` entry `"data_classification": <anything>` would overwrite the validated value. That breaks AC2 and could let an unvalidated value such as `"top-secret"` through, bypassing AC1.
   **Resolution**: reject any reserved key (`RESERVED_PAYLOAD_KEYS = ["data_classification"]`) in `extra_fields` with `AppError` plus `.context()`, before the merge. This is fail-fast and doesn't depend on write order. A post-merge `debug_assert_eq!` is added as defense in depth. Re-applying the value after the merge was rejected because it would silently ignore what the caller asked for.
3. **Conflict test**: `build_ingest_payload_rejects_extra_fields_override_of_classification` passes a valid `internal` together with `extra_fields = {"data_classification": "public"}` and asserts an error. `build_ingest_payload_preserves_unrelated_extra_fields` shows that non-reserved keys still merge and the validated value stays.

**Overall**: no hard-stop failures. Check 16's flag is resolved in the planned code and tests. Check 1's possible out-of-scope files (test registration, extra `SbomDetails` construction sites) must get user approval before Step 10.
