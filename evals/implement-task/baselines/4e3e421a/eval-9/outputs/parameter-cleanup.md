# Dead Parameter Cleanup: TC-9207

## 1. Identify the candidate

Removing the `VersionMatches` filter block from `SbomService::list` removes the only lines that
referenced `version_filter`. After that edit the parameter has zero references in the function
body, so it is a dead parameter (skill Step 9, "Dead parameter detection").

Before I treat it as dead, I would check that it really is unused:
- `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)`: read the body after
  the edit and confirm nothing still reads `version_filter`, including logging, tracing spans,
  or forwarding to a helper.
- `cargo check` / `cargo clippy`: an `unused_variables` warning on `version_filter` confirms it.

## 2. Decision: remove it, do not rename it

| Option | Verdict |
|---|---|
| Rename to `_version_filter` | Rejected. It hides the warning but keeps a meaningless argument in the public API. The skill says "The correct fix is removal, not renaming." |
| `#[allow(unused_variables)]` | Rejected for the same reason. |
| Keep it "for future use" | Rejected. Version filtering has moved to the client, and the acceptance criteria require callers to work without the argument. |
| **Remove it from the signature** | **Chosen.** |

`SbomService::list` is an inherent method, not a trait method, so there are no other
implementations to check. If Step 4 shows it actually implements a trait (for example a shared
`ListService` trait), I would remove the parameter from the trait only if no other implementation
uses it. Otherwise I would stop and ask the user.

New signature (same shape as `AdvisoryService::list` and `PackageService::list`):

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

## 3. Find all call sites

- `mcp__serena_backend__find_referencing_symbols("SbomService/list", relative_path="modules/fundamental/src/sbom/service/sbom.rs")`
- Grep cross-check, in case the language server misses something such as macro-generated calls:
  `search_for_pattern("\\.list\\(")` limited to files that import `SbomService`, and
  `search_for_pattern("version_filter|VersionMatches")` across the workspace.

Expected result (from the task's Implementation Notes). The check confirms there are no others:

| # | Call site | In Files to Modify? | Current call (expected) | Updated call |
|---|---|---|---|---|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | Yes | `service.list(search, paginated, &version, &tx)` | `service.list(search, paginated, &tx)` |
| 2 | `modules/search/src/service/mod.rs` | **No** | `sbom_service.list(q, p, "", tx)` | `sbom_service.list(q, p, tx)` |
| 3 | `tests/api/sbom.rs` | Yes | `service.list(q, p, "<ver>", &tx)` (several) | `service.list(q, p, &tx)`; the version-specific test is deleted |

## 4. Update each call site

### Call site 1: endpoint handler (`endpoints/list.rs`)
- Drop the argument from the call.
- Removing the parameter leaves the extracted `version` value with nothing to receive it, which
  is a second dead value in the chain. Remove the `version` field from the query-params struct
  (or the separate `Query<...>` extractor) and its utoipa `IntoParams`/`#[param]` annotation.
  That way the API no longer accepts or documents `version`, as the acceptance criteria require.
- Remove any imports that are now unused.

### Call site 2: search service (`modules/search/src/service/mod.rs`), out of scope
- This file is not listed in Files to Modify. Without the change, though, the workspace does not
  compile, and the acceptance criteria require "All call sites compile".
- The change is minimal: delete the `""` argument and nothing else in the file.
- In Step 9's scope containment check, I would list it as an out-of-scope file with the reason
  above and **wait for explicit user approval before committing**. I would not quietly keep the
  dead parameter to avoid touching this file.
- After the edit, I would check whether the search service has its own wrapper that took a
  version argument only to pass it through. If so, that wrapper parameter is dead as well. I
  would flag it to the user rather than widening scope further on my own.

### Call site 3: integration tests (`tests/api/sbom.rs`)
- Delete `test_list_sboms_version_filtered`. The behaviour it checked no longer exists.
- In the other tests, mechanically remove the version argument (usually `""`) from
  `SbomService::list` calls. Leave assertions and setup alone.
- Remove fixtures or helpers used only by the deleted test, such as SBOMs seeded with specific
  versions just for that test, if nothing else references them.

## 5. Cascading dead-code check

After removing the parameter, I would look for code that only existed to support it:
- **`VersionMatches` filter type.** If it is defined in `sbom.rs` and unused, delete it. If it
  lives in `common/src/db/query.rs` (out of scope) and now has no users, flag it in the PR
  description as a follow-up instead of deleting it.
- **Helper functions** such as `apply_version_filter(...)` that are now unreferenced: remove them
  if they are in in-scope files.
- **Imports** that become unused in all touched files: remove them so clippy passes with
  `-D warnings`.
- **Documentation:** `docs/api.md` (and the generated OpenAPI spec, if CONVENTIONS.md has a
  generation command) probably mention `version`. Flag these for approval and regenerate the spec.

## 6. Verify

1. `cargo check --workspace --all-targets`: every caller compiles.
2. Run each CI command from CONVENTIONS.md (fmt, clippy with `-D warnings`, and so on). Any
   failure is a hard stop.
3. Run `cargo test -p <crate>` for every crate with a modified file. Resolve crate names with
   `cargo metadata --no-deps --format-version 1`; expect the fundamental module, the search
   module, and the tests crate.
4. Run `git diff` and grep for `version_filter` and `VersionMatches`. There should be no
   remaining references, except a `VersionMatches` definition in `common` if one exists and was
   flagged.
5. Confirm there are no new compiler warnings compared with the baseline taken before the change.
