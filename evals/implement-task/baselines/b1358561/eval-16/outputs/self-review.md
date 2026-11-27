# Step 9 Self-Verification — TC-9213

Checks were applied to the planned change following `shared/self-verification.md`. Nothing was
executed (eval mode), so commands are described, not run.

| # | Check | Fires? | Result |
|---|---|---|---|
| 1 | Scope containment | Always | PASS (conditional). Planned diff: `advisory/service/advisory.rs`, `advisory/model/summary.rs` (Files to Modify) and `tests/api/advisory_summary.rs` (Files to Create). Possible out-of-scope edits: (a) callers of `build_summary()` that need the new argument, (b) a test registration entry in `tests/Cargo.toml`. Each would be listed with its reason and needs explicit user approval before commit. |
| 2 | Untracked files | Yes (new test file in `tests/api/`) | PASS. The only untracked file is `tests/api/advisory_summary.rs`, which is in Files to Create. No other untracked files are expected near the modified files. |
| 3 | Sensitive patterns | Always | PASS. The planned change has no passwords, API keys, private keys or `.env` references. Both `git diff HEAD` and `git diff --cached` (after staging) would be scanned with the grep pattern. |
| 4 | Dead parameters | No | Not fired. No lines that use a parameter are removed; one parameter is added and it is used. |
| 5 | Duplication | Yes (new validation logic and constant) | PASS (conditional). Step 4 searches for an existing `RiskClassification` enum or allowed-value constant (e.g. near the `severity` handling). If one exists, it is imported per the Step 6 Reuse rules. If not, `ALLOWED_RISK_CLASSIFICATIONS` is the single definition, used by both the service and the tests. |
| 6 | Documentation currency | Borderline (a public model struct gains a field; API Changes is "none") | PASS. No endpoint or config changes. If `docs/api.md` documents the `AdvisorySummary` schema, that is flagged to the user as an out-of-scope doc and not edited without approval. |
| 7 | Documentation scope preservation | No | Not fired. No documentation section is replaced. |
| 8 | Eval coverage | No | Not fired. No `skills/*/SKILL.md` is modified. |
| 9 | Example consistency | No | Not fired. No docs with composite examples are modified. |
| 10 | Cross-section references | Yes (task lists file paths) | PASS. `AdvisoryService::build_summary()` is at `modules/fundamental/src/advisory/service/advisory.rs` in both Files to Modify and Implementation Notes. `AdvisorySummary` is at `.../advisory/model/summary.rs`, which matches the repo tree and the model directory named in the Implementation Notes. `tests/api/advisory_summary.rs` sits next to the existing `tests/api/advisory.rs`. `AppError` is at `common/src/error.rs`, which matches the repo tree. |
| 11 | Data-flow trace | Yes (new feature) | PASS. Input: the `risk_classification` argument to `build_summary()`. Processing: membership check against the allowed set; an invalid value returns `Err(AppError)` with context. Output: the value is written to `AdvisorySummary.risk_classification`, the struct is returned, and serde serializes it with the rest of the summary. Every stage connects. Persistence is out of scope: the task adds no entity or migration change, and the summary is a built response model. |
| 12 | Query scope | No | Not fired. No batch database operations. |
| 13 | Contract & sibling parity | Yes (struct has siblings; calls shared `AppError`) | PASS. Contract: no trait is implemented or changed; the `Result<AdvisorySummary, AppError>` return type is kept. Sibling parity: the new field copies the derives, serde and doc style of the `severity` field and of `SbomSummary`/`PackageSummary`; errors use `.context()` like sibling services. Cross-module entity: none, since no shared DB entity is written. Caller-site: `AppError` is built and wrapped the way other validation sites in `fundamental` do it (variant confirmed from `common/src/error.rs`). |
| 14 | CI checks from CONVENTIONS.md | Always | Pending execution. Every CI command recorded from `CONVENTIONS.md` would run in order, then any codegen commands (e.g. an OpenAPI spec, if `AdvisorySummary` derives `ToSchema`) with their changed files staged. If `CONVENTIONS.md` lists no CI section, the fallback is `cargo fmt --check`, `cargo clippy` and `cargo check`. Any non-zero exit is a hard stop and goes to the user. |
| 15 | Module tests (Rust) | Yes (Rust crates modified) | Pending execution. Use `cargo metadata --no-deps --format-version 1` to resolve the package that owns `modules/fundamental/src/...` and the package that owns `tests/api/advisory_summary.rs`, not the nearest `Cargo.toml`. Then run `cargo test -p <crate>` for each. Needs the PostgreSQL test DB; if it is unavailable, that is reported clearly. A failure is a hard stop. |
| 16 | Validated-value override paths | Yes (a validated, fail-closed value is added) | PASS. (1) Later writes: after `risk_classification` is validated and assigned in the struct literal, `build_summary()` only returns the struct. Per the Implementation Notes (to be confirmed with `find_symbol include_body=true`), it does no merge, bulk update, defaults merge, extra-field map or patch helper afterwards, and no callee writes to the struct. (2) No path can replace the validated value; validation happens before construction, so an invalid value never reaches the struct. (3) No later write path exists, so no override/conflict test is added and no test seam is introduced. The happy-path value test and the rejection test cover the acceptance criteria. |

## Flags to resolve before commit

- Possible out-of-scope edits (callers of `build_summary()`, test registration, `docs/api.md`)
  need user approval if Step 4 finds they are required.
- Checks 14 and 15 were not run in this eval, so their results are pending.
