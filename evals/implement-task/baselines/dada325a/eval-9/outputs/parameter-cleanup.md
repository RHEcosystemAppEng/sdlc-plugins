# Parameter Cleanup — TC-9207

## 1. Identify the dead parameter

The diff for `SbomService::list` removes the only lines that read `version_filter`, which apply `VersionMatches` to the query. After that change:

- `version_filter: &str` has zero references in the function body.
- rustc would warn `unused variable: version_filter`.

That makes it a **dead parameter**.

## 2. Remove it, don't rename it

These options are rejected:

- Renaming it to `_version_filter`. That only silences the warning while the API still asks for a meaningless argument. The skill says "The correct fix is removal, not renaming."
- Keeping it and ignoring it. Callers would keep passing values that do nothing, which misleads readers, and it violates AC3 ("All call sites compile and pass without the version_filter argument").

The chosen fix is to remove it from the signature:

```rust
// Before
pub async fn list(&self, search: Query, paginated: Paginated, version_filter: &str, tx: &Transactional<'_>)
    -> Result<PaginatedResults<SbomSummary>, AppError>

// After
pub async fn list(&self, search: Query, paginated: Paginated, tx: &Transactional<'_>)
    -> Result<PaginatedResults<SbomSummary>, AppError>
```

`SbomService::list` is an inherent method on a concrete struct, not a trait method, so no other implementations have to agree on the signature. If Step 4 turned up a trait (e.g. a `SbomLister` used for mocking), I would remove the parameter from the trait only after confirming that no implementation reads it.

## 3. Find every call site

- Primary: `mcp__serena_backend__find_referencing_symbols(name_path="SbomService/list", relative_path="modules/fundamental/src/sbom/service/sbom.rs")`
- Cross-check, in case of macro-generated or dynamic calls the LSP misses: `search_for_pattern("\.list\(")` scoped to `modules/` and `tests/`, filtered to receivers of type `SbomService`, plus a search for `version_filter`.

Expected result (it matches the task's Implementation Notes):

| # | File | Current call (illustrative) | Updated call | In scope? |
|---|---|---|---|---|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | `service.list(search, paginated, &params.version.unwrap_or_default(), &tx)` | `service.list(search, paginated, &tx)` | Yes |
| 2 | `modules/search/src/service/mod.rs` | `self.sbom.list(query, paginated, "", &tx)` | `self.sbom.list(query, paginated, &tx)` | **No: flag for approval** |
| 3 | `tests/api/sbom.rs` (several calls) | `service.list(q, p, "1.0", &tx)` / `list(q, p, "", &tx)` | `service.list(q, p, &tx)` | Yes |

If the search finds any call site beyond these three, it gets the same treatment, and it gets flagged too if it falls outside Files to Modify.

## 4. Update each call site

### 4.1 Endpoint handler (`list.rs`)

The dead parameter cascades upward. After the service stops accepting a version, the handler's `version` value becomes dead as well, so I would remove the whole chain:
1. The `version: Option<String>` field in the query-params struct, or the whole struct and its `Query<...>` extractor argument if `version` was its only field.
2. The `("version" = Option<String>, Query, ...)` entry in `#[utoipa::path(params(...))]`.
3. The argument in the `list(...)` call.
4. Any imports used only by those pieces.

After the edit I would re-scan the handler for unused bindings so that no new dead variable is left behind.

### 4.2 Search service (`modules/search/src/service/mod.rs`): out of scope

The edit is a one-line, mechanical change: drop the `""` argument. The empty string shows this caller never used version filtering, so the change has no effect on behavior. The file is not in Files to Modify, though, so:

- I would **not** edit it silently.
- In Step 9's scope-containment check I would tell the user it is required for compilation (task call site #2) and ask for explicit approval.
- If the user refuses, the build breaks. The only workaround is to keep a dead `_version_filter` parameter, which the skill forbids and which fails AC3. I would present that tradeoff and stop until the user decides.

### 4.3 Integration tests (`tests/api/sbom.rs`)

- Delete `test_list_sboms_version_filtered` entirely. Its whole purpose was to test the removed behavior.
- In the remaining tests, drop the version argument from every `list(...)` call. Any test that passed a non-empty version string while asserting on non-version behavior is updated to the 3-argument call. Its assertions still hold because the filter no longer narrows results. If an assertion relied on version narrowing (e.g. an expected count), I would check it against the fixture data rather than adjust the number blindly.
- HTTP-level tests that hit `GET /api/v2/sbom?version=...` only to test filtering are removed along with the filtered test.

## 5. Related dead code (flag only)

- `VersionMatches`, probably in `common/src/db/query.rs`: if `search_for_pattern("VersionMatches")` shows no remaining users, it is dead code. That file is out of scope, so I would mention it in the PR and Jira comment as a follow-up instead of deleting it.
- The `use ...::VersionMatches;` import in `sbom.rs` **is** removed, because it is in scope and would otherwise cause an `unused_imports` warning.

## 6. Verify

1. `cargo check` and `cargo clippy --all-targets -- -D warnings` (or the CI commands in `CONVENTIONS.md`): no unused-variable or unused-import warnings, and all call sites compile.
2. `cargo test -p <fundamental-crate>`, `cargo test -p <search-crate>`, and `cargo test -p <tests-crate>`. Crate names come from `cargo metadata --no-deps --format-version 1`.
3. Run the OpenAPI generation command if `CONVENTIONS.md` defines one, and commit the regenerated spec without the `version` param.
4. Final `grep -rn "version_filter"` across the repo should return nothing.

Any non-zero exit is a hard stop and gets reported to the user before committing.
