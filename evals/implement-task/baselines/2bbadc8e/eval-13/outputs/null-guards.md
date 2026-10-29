# Defensive Property Access Analysis: TC-9211

## Context

`AdvisoryIngestResult` is produced by `IngestorService::ingest_advisory()` in `modules/ingestor/src/service/mod.rs`. It crosses a module boundary into `modules/fundamental/src/advisory/service/advisory.rs` where the new `extract_vulnerability_summary()` method consumes it. Per the implement-task skill (Step 6, "Defensive property access on external data"), all nullable fields must be guarded before access because the producer's schema may allow null, return partial results, or evolve independently.

## Nullable Fields Analysis

### Field 1: `cves: Option<Vec<String>>`

| Property | Value |
|---|---|
| **Type** | `Option<Vec<String>>` |
| **When None** | Advisory has no CVE references |
| **Downstream usage** | Read `.len()` for `cve_count`, clone contents for `cve_list` |
| **Risk if unguarded** | `.unwrap()` panics at runtime when advisory lacks CVE data |
| **Guard pattern** | `unwrap_or_default()` |
| **Rationale** | `Vec<String>` implements `Default` (returns empty vec). This is the idiomatic Rust pattern for "give me the value or an empty collection". A single call resolves both `cve_list` and `cve_count` consistently. |

**Implementation**:
```rust
let cve_list = result.cves.clone().unwrap_or_default();
let cve_count = cve_list.len() as u32;
```

**Why `clone().unwrap_or_default()` and not `as_ref()`**: We need an owned `Vec<String>` for the output struct. Cloning before unwrapping avoids a borrow that would complicate the return value. If the field is `None`, `unwrap_or_default()` creates a new empty `Vec` without cloning.

**Why not `match`/`if let`**: `unwrap_or_default()` is more concise for the common case of "Option of a Default-implementing type". `match` would be equivalent but more verbose with no added clarity:
```rust
// Equivalent but unnecessarily verbose:
let cve_list = match &result.cves {
    Some(cves) => cves.clone(),
    None => Vec::new(),
};
```

---

### Field 2: `affected_packages: Option<Vec<AffectedPackage>>`

| Property | Value |
|---|---|
| **Type** | `Option<Vec<AffectedPackage>>` |
| **When None** | Advisory has no package-level detail |
| **Downstream usage** | Read `.len()` for `affected_package_count`; individual package data not needed in summary |
| **Risk if unguarded** | `.unwrap()` panics when advisory lacks package detail |
| **Guard pattern** | `as_ref().map().unwrap_or()` |
| **Rationale** | Only the count is needed, not the full vector. Using `as_ref()` avoids cloning the entire `Vec<AffectedPackage>`. `map(|pkgs| pkgs.len() as u32)` extracts the count from the borrowed reference. `unwrap_or(0)` provides the default when `None`. |

**Implementation**:
```rust
let affected_package_count = result
    .affected_packages
    .as_ref()
    .map(|pkgs| pkgs.len() as u32)
    .unwrap_or(0);
```

**Why `as_ref().map().unwrap_or()` and not `unwrap_or_default()`**: We do not need the owned `Vec<AffectedPackage>` -- only its length. `unwrap_or_default()` would require either cloning the vec (wasteful) or moving it out of the borrowed `result` (not possible with `&AdvisoryIngestResult`). The `as_ref().map()` chain borrows without cloning, then extracts the scalar count.

**Why not `if let`**: `if let` is equivalent but slightly more verbose for a single-expression extraction:
```rust
// Equivalent:
let affected_package_count = if let Some(pkgs) = &result.affected_packages {
    pkgs.len() as u32
} else {
    0
};
```

Both are idiomatic; the `as_ref().map().unwrap_or()` chain is preferred in Rust for single-field extraction from `Option`.

---

### Field 3: `severity_counts: Option<HashMap<String, u32>>`

| Property | Value |
|---|---|
| **Type** | `Option<HashMap<String, u32>>` |
| **When None** | Severity metadata absent from advisory |
| **Downstream usage** | Entire map included in output as `severity_breakdown` |
| **Risk if unguarded** | `.unwrap()` panics when severity metadata is missing |
| **Guard pattern** | `unwrap_or_default()` |
| **Rationale** | `HashMap<String, u32>` implements `Default` (returns empty map). The full map is needed for the output struct, so `clone().unwrap_or_default()` gives us an owned empty `HashMap` when `None`. |

**Implementation**:
```rust
let severity_breakdown = result
    .severity_counts
    .clone()
    .unwrap_or_default();
```

**Why `clone().unwrap_or_default()`**: Same rationale as `cves` -- we need an owned `HashMap` for the output struct. `Default` for `HashMap` returns an empty map, which is the correct default for "no severity data".

---

## Guard Pattern Summary

| Field | Type | Guard Pattern | Default Value | Clones Data? |
|---|---|---|---|---|
| `cves` | `Option<Vec<String>>` | `clone().unwrap_or_default()` | `vec![]` | Yes (owned needed for output) |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | `as_ref().map(\|v\| v.len() as u32).unwrap_or(0)` | `0` | No (only count needed) |
| `severity_counts` | `Option<HashMap<String, u32>>` | `clone().unwrap_or_default()` | `HashMap::new()` | Yes (owned needed for output) |

## Patterns Used

### `unwrap_or_default()` (Fields 1, 3)

Used when:
- The inner type implements `Default`
- The `Default` value is the desired fallback (empty collection)
- An owned value is needed for the output struct

This is the most concise Rust idiom for "give me the value or its default." It avoids explicit `match`/`if let` blocks and communicates intent clearly.

### `as_ref().map().unwrap_or()` (Field 2)

Used when:
- Only a derived value (e.g., length) is needed, not the full inner data
- Cloning the inner value would be wasteful
- The input is a borrow (`&AdvisoryIngestResult`), so `.unwrap()` cannot move out

This pattern borrows the inner value via `as_ref()`, transforms it with `map()`, and provides a scalar default with `unwrap_or()`.

## Patterns Explicitly Avoided

### `.unwrap()` -- NEVER used

Direct `.unwrap()` on any of these fields would panic at runtime when the value is `None`. This is unacceptable for data crossing a module boundary where the producer may return partial results.

### `.expect("message")` -- NOT used

While `.expect()` provides a better panic message than `.unwrap()`, it still panics. The task requires graceful handling, not descriptive panics.

### Unchecked property access chains

Accessing `result.cves.len()` or `result.severity_counts.get("critical")` without first resolving the `Option` wrapper would be a compile error in Rust (the type system prevents this). However, the principle extends to any nested access pattern -- always resolve the outer `Option` before accessing inner properties.

## Test Coverage for Null Guards

| Test Case | `cves` | `affected_packages` | `severity_counts` | Purpose |
|---|---|---|---|---|
| All populated | `Some(vec![...])` | `Some(vec![...])` | `Some(map)` | Verifies extraction with real data |
| All None | `None` | `None` | `None` | Verifies all guards produce defaults without panic |
| Mixed (cves Some, rest None) | `Some(vec![...])` | `None` | `None` | Verifies independent defaulting per field |
| Count consistency | Various | N/A | N/A | Verifies `cve_count == cve_list.len()` across None/empty/populated |

The all-None test case is the critical guard validation -- it exercises every null guard simultaneously and confirms the function does not panic when all external data fields are absent.
