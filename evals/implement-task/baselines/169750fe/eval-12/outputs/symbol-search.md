# Symbol Deduplication Analysis — TC-9210

## Search Objective

Before declaring any new constant for severity ordering in the SBOM service module, search the entire `modules/fundamental` package (not just `modules/fundamental/src/sbom/service/sbom.rs`) for an existing definition of `SEVERITY_ORDER` or equivalent severity-ordering symbols.

## Search Process

### Step 1 — Search the target package broadly

Using `find_symbol` / `search_for_pattern` (Serena) or Grep as fallback, search the entire `modules/fundamental/src/` directory tree for:

- `SEVERITY_ORDER` (exact name referenced in the task description)
- `severity_order` (snake_case variant)
- `SeverityOrder` (PascalCase variant)

Search scope: `modules/fundamental/src/**/*.rs` — this covers all submodules (advisory, sbom, package) within the fundamental crate, not just the file being edited.

### Step 2 — Result

**Match found:** `modules/fundamental/src/advisory/service/advisory.rs`

The file defines:

```rust
const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

This constant maps severity strings to sort weights by position in the array, which is exactly what the SBOM remediation sorting needs (Critical > High > Medium > Low > None, determined by array index).

### Step 3 — Visibility check

The constant is currently declared as a private `const` within `advisory.rs`. It is not `pub` and therefore cannot be imported directly from outside the advisory service module.

### Step 4 — Dependency relationship check

Check whether the sbom module already depends on the advisory module. Both `sbom` and `advisory` are submodules within the same crate (`modules/fundamental`), so there is no cross-crate dependency to add — they share the same `Cargo.toml` and can reference each other's public symbols via `crate::advisory::...`.

## Decision: Reuse (make public) — do NOT redeclare

**Decision:** Make `SEVERITY_ORDER` public (`pub const`) in `modules/fundamental/src/advisory/service/advisory.rs` and import it in the sbom service module.

**Rationale:**

1. **No new dependency required.** Both modules live in the same crate (`modules/fundamental`). Making the constant `pub` and importing it via `crate::advisory::service::advisory::SEVERITY_ORDER` (or re-exporting through `mod.rs`) requires zero `Cargo.toml` changes.

2. **DRY principle.** A single source of truth for severity ordering ensures that any future updates (e.g., adding a new severity level) apply consistently across both the advisory and sbom modules. Duplicating the constant would create a maintenance risk — the two copies could diverge silently.

3. **Symbol deduplication guidance.** Per the implement-task skill's symbol deduplication protocol: when a symbol exists in the same package and the dependency already exists, import and reuse rather than redeclare.

**Rejected alternative:** Declaring a new `SEVERITY_ORDER` constant in `modules/fundamental/src/sbom/service/sbom.rs`. This would duplicate the existing definition and violate the acceptance criterion "no duplicate definition." It would also mean future severity changes must update two files — a maintenance burden with no upside.
