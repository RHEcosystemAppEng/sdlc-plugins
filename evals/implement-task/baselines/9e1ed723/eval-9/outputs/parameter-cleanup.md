# Dead Parameter Cleanup — TC-9207

## 1. Identifying the candidate

Once the `VersionMatches` filter block is deleted from `SbomService::list`
(`modules/fundamental/src/sbom/service/sbom.rs`), `version_filter: &str` has
**zero references** in the method body. The removed lines were its only use. rustc
would report `unused variable: version_filter`, and clippy with `-D warnings` would fail.

## 2. Decision: remove the parameter, don't silence it

Options I considered:

| Option | Verdict |
|---|---|
| Rename to `_version_filter` | Rejected. It hides the warning but leaves a dead parameter in a public API, and callers keep passing meaningless values. The skill says: "The correct fix is removal, not renaming." |
| `#[allow(unused_variables)]` / `let _ = version_filter;` | Rejected for the same reason. |
| Keep it "for future use" / backward compat | Rejected. Version filtering has moved to the client. `list` is an inherent method on `SbomService`, not a trait method, so no other implementation could depend on the parameter. |
| **Remove from signature and update every caller** | **Chosen** |

New signature (it now matches the sibling `AdvisoryService::list` / `PackageService::list` shape):

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

## 3. Finding all call sites

- Primary: `mcp__serena_backend__find_referencing_symbols(name_path="SbomService/list",
  relative_path="modules/fundamental/src/sbom/service/sbom.rs")`.
- Cross-check: `search_for_pattern` / Grep for `\.list\(` near `SbomService`/`sbom_service`,
  plus `version_filter`, across the workspace (including `tests/`). This catches calls that
  rust-analyzer might miss, for example in macros or in test crates it hasn't indexed yet.
- Expected result: the three callers from the Implementation Notes. If any extra caller turns
  up, it gets the same update and is flagged in scope containment.

## 4. Call-site updates

| # | File | Before | After | In scope? |
|---|---|---|---|---|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | extracts `version` query param; `service.list(search, paginated, &version, &tx)` | `version` field/extractor and its OpenAPI param removed; `service.list(search, paginated, &tx)` | Yes |
| 2 | `modules/search/src/service/mod.rs` | `SbomService::list(..., search, paginated, "", &tx)` | `SbomService::list(..., search, paginated, &tx)` | **No. Flag for user approval** |
| 3 | `tests/api/sbom.rs` | tests pass `""`, `"1.0"`, etc. | `test_list_sboms_version_filtered` deleted; other calls drop the version argument | Yes |

### Endpoint handler: cascading dead code

Removing the argument from the service call makes the handler's own `version` binding
dead. That includes the `Option<String>` field on the query-params struct and any
`unwrap_or_default()` local. Each of these gets removed too (the dead-parameter scan
also applies to the modified handler), and so does the `utoipa` `IntoParams`/`params(...)`
documentation for `version`. Result: the endpoint no longer extracts or advertises the
parameter, which satisfies the API change for `GET /api/v2/sbom`. If CONVENTIONS.md
defines an OpenAPI generation command, the regenerated spec is committed alongside.

### Search service: scope conflict

`modules/search/src/service/mod.rs` is a required call-site update, because without it the
workspace won't compile and AC "All call sites compile" fails. However, the file is not
listed in Files to Modify. Following the skill's scope rules:
1. Make the minimal one-line change (drop the `""` argument). No other edits to that file.
2. In Step 9 scope containment, list it as out of scope, explain why (a direct consequence
   of the signature change, named as call site #2 in Implementation Notes), and get explicit
   user approval before committing.
3. Record it as a deviation in the PR description and the Jira comment.

### Tests

- `test_list_sboms_version_filtered` is **deleted** because it exercises only the removed feature.
- All other tests: mechanical removal of the version argument. Assertions are not changed,
  which shows that the non-version behaviour is preserved.

## 5. Related cleanup (flag only)

- Unused imports in `sbom.rs` (e.g. `VersionMatches`) are removed because they are in an
  in-scope file and would otherwise trigger warnings.
- If `VersionMatches` (wherever it is defined, probably `common/src/db/query.rs` or the sbom
  module) has no remaining users, it is now dead code. That file is out of scope, so I would
  **report it for follow-up rather than delete it**.

## 6. Verification

1. `cargo check --workspace --all-targets`: confirms every call site compiles.
2. CONVENTIONS.md CI commands (e.g. `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`):
   confirms no unused-variable/import warnings remain. Non-zero exit is a hard stop.
3. `cargo test -p <fundamental crate>`, `cargo test -p <search crate>`, `cargo test -p <tests package>`
   (package names resolved via `cargo metadata`).
4. Re-grep for `version_filter` and `VersionMatches` in the modified files, which should return no matches.
