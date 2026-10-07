# Parameter Cleanup: Dead Parameter Detection and Removal

## Dead Parameter Detection Reasoning

When code that references a function parameter is removed, the parameter may become "dead" -- present in the signature but never used in the body. This is exactly what happens in TC-9207:

1. `SbomService::list` accepts `version_filter: &str`.
2. The only code in the method body that references `version_filter` is the `VersionMatches` filtering logic.
3. The task asks us to remove that filtering logic.
4. After removal, `version_filter` has zero references in the function body -- it is a dead parameter.

### Detection method

After removing the filter logic from the function body, scan the remaining body for any reference to `version_filter`. Since the `VersionMatches` filter was the sole consumer of that parameter, no references remain. The parameter is confirmed dead.

In Rust, the compiler would emit a warning for unused parameters unless the name is prefixed with an underscore (`_version_filter`). This warning is itself a signal that the parameter should be evaluated for removal.

## Why Remove, Not Rename

The temptation when encountering an unused parameter is to prefix it with an underscore (e.g., `_version_filter`) to suppress the compiler warning. This is the wrong approach for a public API method. Here is why:

### Underscore prefixing suppresses warnings but preserves problems

- **Unnecessary API surface**: The parameter remains part of the function's public signature. Every caller must still pass a value for it, even though that value is ignored. This is confusing for developers reading the code -- they see a parameter being passed and naturally assume it has an effect.
- **Maintenance burden**: All 3 call sites must continue constructing and passing a value that serves no purpose. If the type of the parameter changes or is removed in a future refactor, all callers break for no functional reason.
- **Misleading contracts**: A function's signature is its contract. A parameter in the signature promises "I use this value." A dead parameter violates that promise silently.
- **Code review noise**: Future contributors will wonder why a parameter exists, investigate whether it is used, and potentially try to "fix" the apparent oversight -- wasting review cycles.

### Removal is the correct fix

Removing the parameter:

- Eliminates the unnecessary API surface.
- Simplifies all call sites -- callers no longer need to construct or pass a meaningless argument.
- Makes the function's contract honest -- the signature accurately reflects what the function uses.
- Lets the compiler enforce completeness -- if a call site is missed during cleanup, the build fails immediately, unlike underscore prefixing which silently compiles.

## Removal Procedure

1. **Remove the parameter from the function signature**: Delete `version_filter: &str` from `SbomService::list`.

2. **Find all call sites**: Use `find_referencing_symbols` on `SbomService::list` (or Grep for `\.list(`) to locate every caller. For this task, there are exactly 3:
   - `modules/fundamental/src/sbom/endpoints/list.rs` -- the REST endpoint handler
   - `modules/search/src/service/mod.rs` -- the search service
   - `tests/api/sbom.rs` -- integration tests

3. **Update each call site**: Remove the `version_filter` argument from every call. Since parameter positions shift, ensure the remaining arguments (`search`, `paginated`, `tx`) are still in the correct order.

4. **Remove upstream extraction**: In the endpoint handler, also remove the code that extracts the `version` query parameter from the HTTP request -- there is no longer a downstream consumer for it.

5. **Remove dead tests**: Delete `test_list_sboms_version_filtered` since it tests behavior that no longer exists. Update any remaining test calls that passed version filter values.

6. **Re-run tests**: Run `cargo test` for all affected crates to confirm that:
   - The code compiles without the parameter (no missed call sites).
   - Existing tests that do not depend on version filtering still pass.
   - No regressions were introduced by the parameter removal.

## General Principle

Dead parameters should be removed at the point they become dead, not deferred. The implement-task skill's self-verification step (Step 9, "Dead parameter detection") codifies this:

> When the implementation removes code that references function parameters, scan the modified functions for parameters that are no longer used in the function body. [...] The correct fix is removal, not renaming.

This principle applies broadly: after any refactoring that removes the last reference to a parameter, the parameter itself should be removed and all call sites updated in the same change. Deferring removal leads to accumulated dead parameters that obscure the codebase's actual contracts.
