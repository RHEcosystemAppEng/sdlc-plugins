# Symbol Deduplication Analysis -- TC-9210

## Symbol Under Investigation

**Symbol:** `SEVERITY_ORDER`
**Context:** The task requires sorting advisories by severity (Critical > High > Medium > Low > None). This requires a constant that maps severity strings to sort weights or defines their ordering.

## Search Process

### Step 1: Search the target package broadly for SEVERITY_ORDER

Before declaring a new `SEVERITY_ORDER` constant in the sbom service, search the entire `modules/fundamental/` package (not just the file being edited) for any existing definition.

**Tool used:** `mcp__serena_backend__search_for_pattern` (or equivalent Grep)

**Search query:** `SEVERITY_ORDER` across `modules/fundamental/src/`

**Search scope:** The entire `modules/fundamental` crate -- this is the target package that contains both the `sbom` and `advisory` modules. Searching broadly ensures we find definitions in sibling modules, not just the file being edited (`sbom/service/sbom.rs`).

### Step 2: Search with variations

Also searched for common naming variations to ensure full coverage:

- `SEVERITY_ORDER` (SCREAMING_SNAKE_CASE -- Rust constant convention)
- `severity_order` (snake_case -- Rust function/variable convention)
- `SeverityOrder` (PascalCase -- Rust type convention)

**Search scope:** `modules/fundamental/src/**/*.rs`

### Step 3: Results

**Match found:**

- **File:** `modules/fundamental/src/advisory/service/advisory.rs`
- **Definition:** `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`
- **Visibility:** Defined within the advisory service module

This is an array constant that lists severity levels in descending priority order. The position of each severity string in the array determines its sort weight -- index 0 ("critical") is highest priority, index 4 ("none") is lowest.

No other definitions of `SEVERITY_ORDER` or equivalent severity ordering constants were found elsewhere in the package.

### Step 4: Reuse feasibility check

**Dependency relationship:** Both `sbom` and `advisory` are sibling modules within the same crate (`modules/fundamental`). There is no cross-crate dependency to introduce -- they share the same `Cargo.toml` and compilation unit. The sbom module can import from the advisory module directly via a crate-internal path (e.g., `use crate::advisory::service::advisory::SEVERITY_ORDER`).

**Visibility check:** If `SEVERITY_ORDER` is not currently `pub`, it needs to be made `pub` (or `pub(crate)`) so the sbom service can import it. Since both modules are in the same crate, `pub(crate)` is sufficient and maintains encapsulation.

## Decision

**Reuse the existing `SEVERITY_ORDER` constant** from `modules/fundamental/src/advisory/service/advisory.rs`.

**Rationale:**
1. The constant defines exactly the same ordering the task requires (Critical > High > Medium > Low > None).
2. Both modules are in the same crate, so no new dependency is needed.
3. Reusing ensures a single source of truth -- if the severity ordering ever changes, it only needs to be updated in one place.
4. Declaring a duplicate constant in the sbom service would violate DRY and create a maintenance risk where the two definitions could drift out of sync.

**Action required:** If `SEVERITY_ORDER` is not already `pub` or `pub(crate)`, change its visibility to `pub(crate)` in `advisory.rs`, then import it in `sbom.rs` via `use crate::advisory::service::advisory::SEVERITY_ORDER`.
