# Dead Parameter Cleanup — TC-9207

## Why this is needed

The task Description only says "Remove the filter logic from the service method body."
Doing literally just that leaves `SbomService::list` with a `version_filter: &str`
parameter that is never read. That is a dead parameter, and Step 9 check 4 (Dead
parameters, `shared/self-verification.md`) fires because the removed lines referenced a
function parameter. The Acceptance Criterion "All call sites compile and pass without the
version_filter argument" also requires the argument to be gone.

## Decision: remove, do not rename or suppress

| Option | Verdict |
|---|---|
| Keep `version_filter: &str` unused | Rejected — rustc/clippy `unused_variables` warning; misleading API; fails `-D warnings` CI |
| Rename to `_version_filter` | Rejected — check 4 says underscore-prefixing is a symptom of a dead parameter; the fix is removal, not renaming |
| `#[allow(unused_variables)]` | Rejected — same reason |
| **Remove from signature and update all callers** | **Chosen** |

`SbomService::list` is an inherent method (not a trait method), so there are no other
implementations to check before removing it.

## Procedure

1. **Remove the filter logic** in `modules/fundamental/src/sbom/service/sbom.rs` — the
   `VersionMatches` filter application. Keep search, sort, pagination, and result mapping as they are.
2. **Confirm the parameter is dead:** `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)`
   and check that `version_filter` has zero remaining references in the body.
3. **Remove the parameter** from the signature:
   ```rust
   // before
   pub async fn list(&self, search: Query, paginated: Paginated, version_filter: &str, tx: &Transactional<'_>)
       -> Result<PaginatedResults<SbomSummary>, AppError>
   // after
   pub async fn list(&self, search: Query, paginated: Paginated, tx: &Transactional<'_>)
       -> Result<PaginatedResults<SbomSummary>, AppError>
   ```
4. **Find every caller:** `mcp__serena_backend__find_referencing_symbols("SbomService/list",
   relative_path="modules/fundamental/src/sbom/service/sbom.rs")`, cross-checked with
   `search_for_pattern("\\.list\\(")` scoped to `modules/` and `tests/`. Expected (from
   Implementation Notes), plus any others found:

   | # | Call site | In Files to Modify? | Change |
   |---|---|---|---|
   | 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | Yes | Stop extracting `version` query param (remove field/extractor and OpenAPI `params` entry); call `service.list(search, paginated, &tx)` |
   | 2 | `modules/search/src/service/mod.rs` | **No** | `list(query, paginated, "", &tx)` → `list(query, paginated, &tx)`. Required to compile; flagged under Scope containment (check 1) for explicit user approval before commit |
   | 3 | `tests/api/sbom.rs` | Yes | Delete `test_list_sboms_version_filtered`; in remaining tests drop the version argument (`""` → removed). No assertion changes for unrelated tests |

5. **Cascade the cleanup (dead code introduced by the removal):**
   - Endpoint: the `version` field on the query struct becomes dead once not passed — remove it (and the whole struct/extractor if it only held `version`).
   - Imports: remove `VersionMatches` and any other now-unused `use` items in `sbom.rs` and `list.rs`.
   - `VersionMatches` type itself: `search_for_pattern("VersionMatches")`. If it has no remaining users, report it as dead code; its definition file (likely `common/src/db/query.rs`) is not in Files to Modify, so propose removal and ask the user rather than editing silently.
   - Tests helpers: if `tests/api/sbom.rs` has fixtures/helpers used only by the removed test (e.g. multi-version SBOM seeding), remove them too.
6. **Re-run checks:** `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`
   (catches leftover unused vars/imports), and `cargo test` per modified crate
   (resolved with `cargo metadata`: fundamental, search, tests) plus any CONVENTIONS.md CI commands.
   If an OpenAPI generation command is documented, run it and stage the regenerated spec.

## Verification checklist

- [ ] `grep -rn "version_filter" modules/ tests/` → no matches
- [ ] `grep -rn "VersionMatches" modules/` → no matches (or flagged definition only)
- [ ] No `_version`/`_version_filter` underscore names introduced
- [ ] clippy clean with `-D warnings`
- [ ] All 3 call sites updated; out-of-scope `modules/search/src/service/mod.rs` approved by user
- [ ] `docs/api.md` `version` param mention flagged for approval (documentation currency)

Step 9 check 4 report: `PASS — version_filter removed from SbomService::list; 3 callers updated`.
