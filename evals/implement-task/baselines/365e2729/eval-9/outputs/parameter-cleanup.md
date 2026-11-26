# Dead Parameter Cleanup — TC-9207

## Why `version_filter` becomes dead

The only thing `version_filter` does in `SbomService::list` is feed the `VersionMatches` filter. Once that filter block is gone (the core of the task), the parameter has zero references in the method body. rust-analyzer and `cargo check` would then report `unused variable: version_filter`. Under `clippy -D warnings`, that warning fails CI.

## The decision: remove it, don't silence it

Per the skill's Step 9 "Dead parameter detection", **the correct fix is removal, not renaming.**

Approaches I rejected:
- Renaming it to `_version_filter`. That silences the warning but keeps a meaningless argument that every caller still has to supply.
- Adding `#[allow(unused_variables)]`. This has the same problem.
- Keeping the parameter "for compatibility". `SbomService::list` is an inherent method used inside the workspace, not a published API, and every caller is in this repo.

The approach I chose is to delete the parameter from the signature and update every call site so it stops passing the argument.

## Procedure

1. **Identify the candidate.** In the `git diff` for `sbom.rs`, the removed lines (the `VersionMatches` filter) contain the only references to `version_filter`.
2. **Confirm it is dead.** Run `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)` after the edit and check that `version_filter` no longer appears in the body. Also confirm that `cargo check` reports it as unused.
3. **Check it is not a trait method.** `list` is an inherent `impl SbomService` method, so no trait signature or other implementors need the parameter. Removing it is safe. If it were a trait method, I would remove it only if no implementation used it.
4. **Remove it from the signature.**
   ```rust
   // Before
   pub async fn list(&self, search: Query, paginated: Paginated, version_filter: &str, tx: &Transactional<'_>)
       -> Result<PaginatedResults<SbomSummary>, AppError>
   // After
   pub async fn list(&self, search: Query, paginated: Paginated, tx: &Transactional<'_>)
       -> Result<PaginatedResults<SbomSummary>, AppError>
   ```
5. **Find every call site.** Use `mcp__serena_backend__find_referencing_symbols("SbomService/list", relative_path="modules/fundamental/src/sbom/service/sbom.rs")`, with a Grep fallback for `\.list\(` and `SbomService::list` across the workspace. That catches anything the task description missed, such as a call from a test helper.
6. **Update each caller.**

| # | Call site | Before | After | Scope |
|---|---|---|---|---|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` (REST handler) | `service.list(search, paginated, &params.version, &tx)` | `service.list(search, paginated, &tx)`. Also remove the `version` field/extractor and its `utoipa` param annotation | In scope |
| 2 | `modules/search/src/service/mod.rs` (SearchService) | `sbom_service.list(search, paginated, "", &tx)` | `sbom_service.list(search, paginated, &tx)` | **Out of scope.** Needed for compilation; flagged for user approval in Step 9 |
| 3 | `tests/api/sbom.rs` (integration tests) | `service.list(q, p, "1.0", &tx)` and similar | `service.list(q, p, &tx)`. Delete `test_list_sboms_version_filtered` entirely | In scope |

7. **Cascade: look for newly dead code upstream.** Removing the argument can leave other things unused, so check each of these:
   - **Endpoint:** the `version` field in the handler's query-params struct (or the separate extractor) has no consumer. Remove it, and delete the struct if `version` was its only field.
   - **Search service:** the `""` literal disappears. Check that no local variable or config value existed only to supply it.
   - **Imports:** `VersionMatches` and similar imports in `sbom.rs` are removed if they become unused.
   - **`common/src/db/query.rs`:** if `VersionMatches` has no other users, it is dead too. That file is out of scope, so I would report it as a follow-up suggestion and not edit it.
   - **Tests:** remove any fixture or helper used only by `test_list_sboms_version_filtered`, as long as it lives in `tests/api/sbom.rs`.
8. **Verify.**
   - Run `cargo check --workspace --all-targets`. It should report no unused-variable or unused-import warnings and no "this function takes 4 arguments but 3 were supplied" errors.
   - Run the CI commands from CONVENTIONS.md (fmt, clippy with `-D warnings`).
   - Run `cargo test -p` for the fundamental, search and tests crates, resolving crate names with `cargo metadata`.
   - Run a final Grep for `version_filter`, `_version_filter` and `VersionMatches` in the modified crates. It should return nothing, apart from the out-of-scope definition in `common` if that is kept.

## Reporting

- The commit/PR body says that `version_filter` was removed from `SbomService::list` and lists the updated callers.
- The Step 9 scope-containment report lists `modules/search/src/service/mod.rs`, with the reason "required signature update at a call site; one-argument change only", and asks the user for explicit approval before committing.
- The PR and the Jira comment note that `GET /api/v2/sbom` no longer accepts `?version=`. This is a client-visible API change, and the task says version filtering has moved to the client side.
