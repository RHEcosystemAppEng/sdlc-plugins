# Symbol Deduplication Analysis for TC-9210

## Search Objective

Before implementing the severity-sorted remediation list, determine whether
`SEVERITY_ORDER` already exists in the `modules/fundamental` crate so we can
reuse it rather than redeclaring it.

## Searches Performed

### 1. Exact symbol name search: `SEVERITY_ORDER`

**Tool used:** `mcp__serena_backend__find_symbol` (or Grep as fallback)

**Search scope:** entire `modules/fundamental/src/` directory tree

**Query variants searched:**
- `SEVERITY_ORDER` (Rust constant, SCREAMING_SNAKE_CASE)
- `severity_order` (snake_case variant)
- `SeverityOrder` (PascalCase variant)

**Result:** Found in `modules/fundamental/src/advisory/service/advisory.rs`

**Definition found:**
```rust
pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

This is a public constant (`pub`) defined in the advisory service module.

### 2. Value-based search for the severity list pattern

**Tool used:** Grep / `mcp__serena_backend__search_for_pattern`

**Pattern:** `"critical".*"high".*"medium"` (to catch any inline duplication of the
severity ordering that might not use the constant name)

**Search scope:** entire `modules/fundamental/src/` directory

**Result:** Only one match -- the `SEVERITY_ORDER` definition in
`modules/fundamental/src/advisory/service/advisory.rs`. No other file in the
crate defines or inlines this ordering.

### 3. Dependency relationship check

**Tool used:** Read on `modules/fundamental/Cargo.toml`

**Finding:** Both `sbom` and `advisory` are submodules within the same crate
(`modules/fundamental`). They share the same `Cargo.toml` and are compiled as
part of the same Rust library crate. There is no cross-crate dependency issue --
they are sibling modules within one crate.

### 4. Visibility check

**Tool used:** `mcp__serena_backend__find_symbol` on the constant

**Finding:** The constant is declared `pub`, meaning it is already exported from
its module. We need to verify the re-export chain:
- `advisory/service/mod.rs` must re-export from `advisory.rs` (or the constant
  must be reachable via the module path)
- The constant is accessible as
  `crate::advisory::service::advisory::SEVERITY_ORDER` (or a shorter path if
  re-exported through `mod.rs`)

## Decision

**Reuse the existing `SEVERITY_ORDER` constant.**

Rationale:
1. The constant already exists in a sibling module within the same crate.
2. It is declared `pub`, so it is already exported.
3. Since both `sbom` and `advisory` live in the same crate (`modules/fundamental`),
   no new dependency needs to be added -- a simple `use crate::advisory::...` import
   suffices.
4. The task description explicitly states: "reuse this constant for sorting instead
   of redefining it."
5. Reusing avoids the maintenance risk of two definitions drifting apart.

**Import path to use in `sbom/service/sbom.rs`:**
```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

No changes to the advisory module are required -- the constant is already `pub`.
