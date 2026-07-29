# Parameter Cleanup: Dead Parameter Removal Strategy

## Principle: Remove Dead Parameters, Do Not Underscore-Prefix Them

When a code change removes the only logic that references a function parameter, that
parameter becomes dead. The correct remediation is to **remove the parameter from the
function signature** and update all call sites, not to prefix the parameter name with an
underscore (e.g., renaming `version_filter` to `_version_filter`).

### Why underscore-prefixing is wrong

In Rust (and many other languages), prefixing a parameter with `_` suppresses the
compiler's "unused variable" warning. This is a useful convention during active
development -- for example, when a parameter will be used in a future commit, or when
a trait requires a parameter that a particular implementation does not need. However,
using it as a permanent fix for a parameter that is genuinely dead introduces several
problems:

1. **Unnecessary API surface**: The parameter remains part of the function's public
   contract. Every caller must still construct and pass the argument, even though the
   function ignores it. This increases cognitive load for maintainers who must wonder
   "why is this parameter here if it is not used?"

2. **Misleading caller burden**: Call sites continue to compute, extract, or hardcode a
   value for the dead parameter. In this task's case, the endpoint handler extracts a
   `version` query parameter from the HTTP request solely to pass it to the service
   method. If the parameter is kept but underscore-prefixed, the handler continues
   doing unnecessary work and the `version` query param continues to appear in the API
   surface, misleading API consumers into thinking it has an effect.

3. **Suppressed warnings hide real problems**: The underscore prefix tells the compiler
   "I know this is unused and that is intentional." This is a lie when the parameter is
   genuinely dead -- it is not intentional, it is a leftover from removed functionality.
   Suppressing the warning removes the signal that would help a future developer notice
   the cleanup opportunity.

4. **Accumulated debt**: Dead parameters left in signatures accumulate over time. Each
   one adds a small amount of confusion. Across a codebase, they erode trust in the
   API surface -- developers stop trusting that every parameter matters, which makes
   the codebase harder to reason about.

### When underscore-prefixing IS appropriate

- **Trait/interface implementations**: When a trait or interface method requires a
  parameter but a specific implementation does not use it, underscore-prefixing is
  correct because the parameter cannot be removed from the signature without changing
  the trait contract.
- **Callback signatures**: When a function is passed as a callback and the caller
  expects a specific arity, unused parameters may need to stay in the signature.
- **Temporary development state**: When a parameter will be used in an upcoming commit
  or is part of a partially implemented feature, underscore-prefixing is a reasonable
  temporary measure.

None of these exceptions apply to TC-9207. The `version_filter` parameter in
`SbomService::list` is not required by a trait, not part of a callback signature, and
the version filtering feature is being permanently removed (moved to the client side).
The parameter must be removed.

## Cleanup Procedure for TC-9207

### Step 1: Remove the parameter from the function signature

In `modules/fundamental/src/sbom/service/sbom.rs`, change the `list` method signature
from:

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

to:

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

### Step 2: Update all call sites

There are 3 call sites that pass a `version_filter` argument to `SbomService::list`.
Each must be updated to remove the corresponding argument.

**Call site 1: `modules/fundamental/src/sbom/endpoints/list.rs`** (endpoint handler)

This is the REST endpoint handler for `GET /api/v2/sbom`. It extracts the `version`
query parameter from the HTTP request and passes it to `SbomService::list`. Changes:

- Remove the `version_filter` argument from the `list` call.
- Remove the `version` field from the query parameter struct (if one exists).
- Remove any extraction logic for the `version` query parameter.

**Call site 2: `modules/search/src/service/mod.rs`** (search service)

The search service calls `SbomService::list` with an empty string (`""`) as the version
filter. Change:

- Remove the empty-string argument from the `list` call.

**Call site 3: `tests/api/sbom.rs`** (integration tests)

Integration tests call `SbomService::list` with various version filter values. Changes:

- Remove the `test_list_sboms_version_filtered` test entirely (the feature no longer
  exists).
- Update any other test calls to `SbomService::list` to remove the version filter
  argument.

### Step 3: Re-run tests

After removing the parameter and updating all call sites, run the full test suite:

```bash
cargo test
```

This verifies:

- All call sites compile correctly with the updated signature.
- No test depends on the removed `version_filter` parameter in a way that was missed.
- The remaining SBOM list tests continue to pass without the version filtering
  functionality.
- The search service tests (if any) pass with the updated call.

If any test fails, investigate whether it was relying on the version filtering behavior
(in which case it should be removed or updated) or whether the parameter removal
introduced an unintended regression.

### Step 4: Verify no additional references

Use `grep` or Serena's `search_for_pattern` to search the entire codebase for any
remaining references to `version_filter` in the context of `SbomService::list`:

```bash
grep -rn "version_filter" modules/ tests/
```

If any references remain, update or remove them. This catches indirect references such
as documentation comments, logging statements, or configuration that may reference the
parameter.

## Summary

Dead parameters are API debt. They confuse callers, waste compute at call sites, and
suppress compiler warnings that serve as useful maintenance signals. When code that uses
a parameter is removed, the parameter itself must be removed from the signature and all
call sites must be updated. Underscore-prefixing is a suppression mechanism, not a
cleanup strategy.
