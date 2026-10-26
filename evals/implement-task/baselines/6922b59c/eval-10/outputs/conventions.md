# Convention Conformance Analysis for TC-9208

## Discovered Conventions (from sibling analysis)

### Production Code Conventions

**Module structure:**
- Each domain module follows `model/ + service/ + endpoints/` directory layout
- Models, services, and endpoints are each in their own submodule with a `mod.rs` barrel file

**Endpoint patterns (from `list.rs`, `get.rs` siblings):**
- Handlers return `Result<T, AppError>` with `.context()` wrapping on all fallible operations
- Path parameters extracted via Axum's `Path<T>` extractor
- Route registration in `endpoints/mod.rs` using Axum router methods
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

**Error handling:**
- All errors use `AppError` from `common/src/error.rs`
- Error wrapping uses `.context("descriptive message")` pattern
- 404 responses use `AppError::NotFound` (or equivalent variant)

**Naming conventions:**
- Structs: PascalCase (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`)
- Files: snake_case matching the primary struct (e.g., `summary.rs`, `details.rs`)
- Endpoint files named by action (e.g., `list.rs`, `get.rs`)

**Response types:**
- Response structs derive `Debug, Clone, Serialize, Deserialize, utoipa::ToSchema`
- Structs include doc comments on each field

**Database access:**
- SeaORM entities for queries
- Shared query helpers from `common/src/db/query.rs` for filtering, pagination, sorting

### Test Code Conventions

**File structure (from `tests/api/sbom.rs`, `tests/api/advisory.rs` siblings):**
- Integration tests live in `tests/api/` directory
- Test files named after the domain entity being tested
- Tests use a real PostgreSQL test database
- Status code checks use `assert_eq!(resp.status(), StatusCode::OK)` pattern

**Setup/teardown:**
- Tests bootstrap a test database with known fixture data
- Each test function is independent (no shared mutable state between tests)

**Assertion patterns (from siblings):**

Pattern 1 -- `.filter().any()` existence check (from `tests/api/advisory.rs`):
```rust
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");
```

Pattern 2 -- `.filter().count() > 0` existence check (from `tests/api/sbom.rs`):
```rust
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

Both patterns check only for the existence of items matching a predicate. They do not
verify specific counts, specific values, or the completeness of the result set.

**Naming:**
- Test function names use `test_` prefix with descriptive snake_case names

---

## Convention Conflicts

### CONFLICT: Sibling assertion patterns vs. skill quality guidance

**Sibling pattern:** Existing tests in `tests/api/advisory.rs` and `tests/api/sbom.rs`
use `.filter().any()` and `.filter().count() > 0` to check for existence of items in
list responses. These are existence-only checks that do not verify specific values.

**Skill guidance (Step 7):** "Prefer value-based assertions over length-only checks:
When verifying collections or response data, assert on the actual values -- not just the
count. Assert on specific items or key fields so that test failures reveal *what* changed,
not just *how many*. Length checks alone hide regressions behind a passing count and
prevent subsequent assertions from running."

**Resolution:** Per the skill's explicit rule -- "Skill guidance takes precedence over
sibling patterns" (Step 4 and Step 7) -- the new tests for `package_license.rs` will
NOT adopt the sibling `.filter().any()` / `.filter().count() > 0` assertion patterns.
Instead, they will use value-based assertions that verify specific counts, specific
license identifiers, and the structure of the response.

The sibling patterns will still be followed for all non-conflicting aspects: test file
location (`tests/api/`), naming conventions (`test_` prefix), setup/teardown approach
(real PostgreSQL test database), status code assertion style
(`assert_eq!(resp.status(), StatusCode::OK)`), and overall test structure.

### No other conflicts detected

The task's implementation notes are consistent with the discovered production code
conventions (error handling, module structure, naming).
