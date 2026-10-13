# Dead Parameter Cleanup Approach

## Principle: Remove Dead Parameters, Do Not Suppress Warnings

When a code change removes the logic that used a function parameter, that parameter becomes
dead -- it exists in the signature but has zero references in the function body. The correct
response is to **remove the parameter from the signature and update all call sites**, not to
rename it with an underscore prefix.

## Why Not Underscore-Prefix?

In Rust (and many other languages), prefixing a parameter with an underscore (`_version_filter`)
tells the compiler "I know this is unused; don't warn me." This suppresses the warning but
does not address the underlying problem:

1. **Unnecessary API surface**: callers are still required to construct and pass a value for
   a parameter the function ignores. This is confusing to readers and maintainers -- the
   signature promises the function will use the value, but it does not.

2. **Maintenance burden**: every existing and future call site must provide an argument that
   serves no purpose. If the function has many callers, each one carries dead code in the
   form of an unused argument expression.

3. **Misleading contract**: the function signature is part of its public contract. A parameter
   in the signature communicates "this value affects the function's behavior." A dead parameter
   violates that contract silently.

4. **Cargo-cult propagation**: future code written by analogy ("the other function takes a
   version filter, so mine should too") will propagate the dead parameter into new code.

Underscore prefixes are appropriate for parameters that are intentionally unused *by design* --
for example, a trait method that some implementations need but others do not, or a callback
parameter that a specific handler ignores. They are not appropriate for parameters that became
unused due to a code change.

## Detection Process

When an implementation removes code that references a function parameter, apply the following
checks:

1. **Identify candidates from the diff**: look at `git diff` output for functions where
   removed lines contained the only reference to a parameter. If the removed code was the
   sole consumer of a parameter, that parameter is now dead.

2. **Verify with body scan**: confirm the parameter has zero remaining references in the
   function body. Check for both direct uses (`version_filter`) and indirect uses (e.g.,
   passed to a helper function, used in a macro, captured in a closure).

3. **Check for compiler/linter warnings**: build the project and look for unused-variable
   or unused-parameter warnings. In Rust, `cargo check` will emit `warning: unused variable:
   version_filter` (unless the parameter is underscore-prefixed).

## Removal Process

1. **Remove the parameter from the function signature.** In this case, remove
   `version_filter: &str` from `SbomService::list`.

2. **Find all call sites.** Use `find_referencing_symbols` (Serena) or Grep to locate every
   place the function is called. For TC-9207, the three call sites are:

   - `modules/fundamental/src/sbom/endpoints/list.rs` -- the REST endpoint handler
   - `modules/search/src/service/mod.rs` -- the search service
   - `tests/api/sbom.rs` -- integration tests

3. **Update every caller** to remove the corresponding argument. In Rust, the compiler will
   enforce this -- any caller still passing the extra argument will produce a type error
   because the argument count no longer matches the signature.

4. **Remove upstream extraction**: if the parameter's value was extracted from an external
   source (e.g., a query parameter, config value, or user input), remove that extraction
   logic too. For TC-9207, the endpoint handler extracts `version` from the HTTP query
   string solely to pass it to `SbomService::list` -- that extraction should also be removed.

5. **Re-run tests** to confirm nothing broke. The compiler catches call-site mismatches, but
   tests verify that the remaining behavior is correct and that no test depended on the
   removed parameter's side effects.

## Trait/Interface Consideration

For trait or interface methods, exercise caution: only remove the parameter if **no
implementation** references it. If one implementation uses the parameter and another does not,
the parameter must remain in the trait signature, and non-using implementations should
underscore-prefix it. In TC-9207, `list` is a concrete method on `SbomService` (not a trait
method), so this consideration does not apply.

## Summary

| Approach | Compiler warning | API surface | Caller burden | Correctness |
|---|---|---|---|---|
| `_version_filter` (suppress) | Silenced | Unchanged (bloated) | All callers still pass unused arg | Misleading contract |
| Remove parameter | N/A (parameter gone) | Reduced (clean) | Callers simplified | Honest contract |

The right choice is removal. Underscore suppression hides the symptom; parameter removal fixes
the cause.
