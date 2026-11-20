# Dead Parameter Cleanup — TC-9207

This follows the implement-task skill's **Step 9 → Dead parameter detection** procedure.

## 1. Identify candidates

After removing the `VersionMatches` filter block from `SbomService::list` (`modules/fundamental/src/sbom/service/sbom.rs`), the diff shows that the removed lines held the **only** reference to `version_filter`. This would be confirmed with `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)` on the edited body. rust-analyzer and `cargo build` would also report `unused variable: version_filter`.

Candidate: `version_filter: &str` in `SbomService::list`.

There are also secondary candidates in the endpoint handler (`modules/fundamental/src/sbom/endpoints/list.rs`):
- the `version: Option<String>` field (or a dedicated `VersionQuery` extractor) in the handler's query-params struct
- any local variable such as `let version = params.version.unwrap_or_default();`

Once the handler stops passing it to the service, all of these are dead.

## 2. Detect: why removal, not renaming

The parameter now has zero references in the function body. The fixes that only silence the warning are all **rejected**:

| Option | Decision | Reason |
|---|---|---|
| Rename to `_version_filter` | Rejected | Hides the warning but keeps a meaningless argument in the public API. The skill says "The correct fix is removal, not renaming." |
| `#[allow(unused_variables)]` | Rejected | Same problem, and it suppresses lint signal |
| Keep it "for backward compatibility" | Rejected | `SbomService::list` is internal Rust API, not a wire contract. The only callers are inside this workspace. Keeping it would make callers think filtering still happens. |
| **Remove from signature and update all callers** | **Chosen** | Clean API that matches the sibling `AdvisoryService::list` / `PackageService::list` signatures |

`SbomService::list` is an inherent method, not a trait method, so the trait/interface caveat (only remove if no implementation uses it) does not apply. I would confirm this with `find_symbol` to check there is no `impl SomeTrait for SbomService` that declares `list`.

## 3. Remove and update call sites

### Signature change
```rust
// Before
pub async fn list(&self, search: Query, paginated: Paginated, version_filter: &str, tx: &Transactional<'_>)
    -> Result<PaginatedResults<SbomSummary>, AppError>

// After
pub async fn list(&self, search: Query, paginated: Paginated, tx: &Transactional<'_>)
    -> Result<PaginatedResults<SbomSummary>, AppError>
```
Also remove any import that becomes unused (e.g. `use ...::VersionMatches`).

### Call-site discovery
`mcp__serena_backend__find_referencing_symbols("SbomService/list", relative_path="modules/fundamental/src/sbom/service/sbom.rs")`. As a fallback, Grep for `\.list\(` and `SbomService::list` across `modules/`, `server/`, `tests/`. This cross-checks the task's list of 3 call sites and catches any caller the task missed. Any extra caller would be updated the same way and flagged as out of scope.

### Call-site updates

| # | File | Before | After | In task scope? |
|---|---|---|---|---|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | Extracts `version` from the query string, then `service.list(search, paginated, &version, &tx)` | No `version` extraction (field and OpenAPI `params` entry removed), then `service.list(search, paginated, &tx)` | Yes |
| 2 | `modules/search/src/service/mod.rs` | `sbom_service.list(search, paginated, "", &tx)` | `sbom_service.list(search, paginated, &tx)` | **No.** Flag for approval. |
| 3 | `tests/api/sbom.rs` | Several calls with `""`, `"1.0"`, etc. | Drop the version argument. Delete `test_list_sboms_version_filtered`. | Yes |

### Out-of-scope call site handling (`modules/search/src/service/mod.rs`)
- Without this edit the `search` crate fails to compile, which breaks acceptance criterion "All call sites compile and pass without the version_filter argument".
- The change is a minimal one-argument deletion with no behavior change. The empty string was already a no-op filter.
- In the Step 9 scope containment check I would list it as out of scope, give the reason above, and **wait for explicit user approval before committing**. The PR description and the Jira comment would record it as a deviation from the Files to Modify list.

### Orphaned dependent symbols
- `VersionMatches` filter type: Grep the workspace. If `SbomService::list` was its only user, it is now dead code. It probably lives in `common/src/db/query.rs`, which is out of scope, so I would **report it as a follow-up cleanup** (or ask the user) and not delete it. If it is still used elsewhere, leave it alone.
- The handler params struct: if removing `version` leaves a wrapper struct that only re-wraps `Query`/`Paginated`, simplify it to match the extractor pattern in `advisory/endpoints/list.rs` (same file, so in scope).

## 4. Re-run verification
1. `cargo build` / `cargo check` across the workspace. No `unused variable`/`unused import` warnings, and no arity errors (E0061) at any call site.
2. `cargo clippy -- -D warnings` plus all other CI commands from `CONVENTIONS.md`. Hard stop on any non-zero exit.
3. `cargo test -p <fundamental-crate>`, `cargo test -p <search-crate>`, and `cargo test -p <tests-crate>`, with crate names resolved via `cargo metadata --no-deps --format-version 1`.
4. Confirm that the remaining SBOM list tests and `tests/api/search.rs` pass unchanged.
