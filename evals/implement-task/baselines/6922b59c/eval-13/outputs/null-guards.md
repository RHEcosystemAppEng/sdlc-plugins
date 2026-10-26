# Defensive Property Access Analysis -- TC-9211

## Context

The `AdvisoryIngestResult` struct is defined in `modules/ingestor/src/service/mod.rs` and consumed by the new `extract_vulnerability_summary()` method in `modules/fundamental/src/advisory/service/advisory.rs`. This crosses a module boundary (ingestor -> fundamental), so defensive property access is mandatory per the SKILL.md quality practices.

The three nullable fields use `Option<T>`, which means accessing the inner value without a guard will cause a compile error (Rust enforces Option handling at compile time). However, using `.unwrap()` would compile but panic at runtime if the value is `None`. The goal is to use safe, idiomatic combinators that never panic.

---

## Fields Requiring Guards

### 1. `cves: Option<Vec<String>>`

**Why it needs a guard**: This field is `None` when the advisory has no CVE references. The extractor needs both the list itself (for `cve_list`) and its length (for `cve_count`). Accessing `.len()` or iterating on a `None` value without unwrapping would not compile, and using `.unwrap()` would panic at runtime.

**Guard pattern used**: `as_ref().cloned().unwrap_or_default()`

```rust
let cve_list: Vec<String> = ingest_result
    .cves
    .as_ref()
    .cloned()
    .unwrap_or_default();
let cve_count: u32 = cve_list.len() as u32;
```

**Why this pattern**:
- `as_ref()` borrows the Option contents without moving them out of the struct (needed since we take `&AdvisoryIngestResult`).
- `.cloned()` converts `Option<&Vec<String>>` to `Option<Vec<String>>` by cloning, which is necessary since we need an owned `Vec<String>` for the output struct.
- `.unwrap_or_default()` returns an empty `Vec<String>` when `None`, which is the `Default` implementation for `Vec<T>`.
- `cve_count` is derived from the already-guarded `cve_list`, ensuring consistency between the two fields.

**Alternative considered**: `.map_or_else(Vec::new, |v| v.clone())` -- equivalent but less idiomatic than `unwrap_or_default` when `Default` provides the right fallback.

---

### 2. `affected_packages: Option<Vec<AffectedPackage>>`

**Why it needs a guard**: This field is `None` for advisories without package-level detail. The extractor only needs the count (not the full list), so we avoid cloning the entire vector.

**Guard pattern used**: `as_ref().map(|pkgs| pkgs.len() as u32).unwrap_or(0)`

```rust
let affected_package_count: u32 = ingest_result
    .affected_packages
    .as_ref()
    .map(|pkgs| pkgs.len() as u32)
    .unwrap_or(0);
```

**Why this pattern**:
- `as_ref()` borrows without moving, consistent with the `&self` receiver pattern.
- `.map()` transforms the `Some` variant by computing the length, avoiding a full clone of the `Vec<AffectedPackage>` (which may contain complex structs).
- `.unwrap_or(0)` provides the explicit default of 0 for the `None` case.
- This is more efficient than `unwrap_or_default` + `.len()` because it avoids allocating an empty vector just to measure it.

**Alternative considered**: `.as_ref().map_or(0, |pkgs| pkgs.len() as u32)` -- equivalent and slightly more concise. Either form is acceptable; the `map().unwrap_or()` chain reads more clearly in a step-by-step fashion.

---

### 3. `severity_counts: Option<HashMap<String, u32>>`

**Why it needs a guard**: This field is `None` when severity metadata is absent from the advisory. The extractor needs the full map for the `severity_breakdown` output field. Accessing keys or iterating on a `None` value without guarding would not compile, and `.unwrap()` would panic.

**Guard pattern used**: `as_ref().cloned().unwrap_or_default()`

```rust
let severity_breakdown: HashMap<String, u32> = ingest_result
    .severity_counts
    .as_ref()
    .cloned()
    .unwrap_or_default();
```

**Why this pattern**:
- `as_ref()` borrows without moving.
- `.cloned()` converts `Option<&HashMap<String, u32>>` to `Option<HashMap<String, u32>>` by cloning, needed for ownership transfer to the output struct.
- `.unwrap_or_default()` returns an empty `HashMap` when `None`, which is the `Default` implementation for `HashMap<K, V>`.
- The pattern is identical to the `cves` field because the requirement is the same: transfer the full collection or provide an empty default.

**Alternative considered**: Using `into_iter().flatten().collect()` -- this would work if we consumed the `AdvisoryIngestResult` (took ownership), but since we borrow it via `&`, the `as_ref().cloned().unwrap_or_default()` pattern is the correct choice.

---

## Patterns NOT Used (and Why)

### `.unwrap()`

Never used. `.unwrap()` panics on `None`, which directly violates the task requirement that the extractor "handle all nullable fields gracefully without panicking." Even though Rust's type system makes `None` handling explicit, `.unwrap()` is an escape hatch that converts a compile-time safety guarantee into a runtime crash.

### `.expect("message")`

Not used. While `.expect()` provides a better panic message than `.unwrap()`, it still panics on `None`. The extractor has well-defined default behavior for every `None` case, so there is no reason to panic.

### `if let Some(x) = field` (match/if-let)

Not used in the primary implementation because the combinator chains (`unwrap_or_default`, `map().unwrap_or()`) are more concise for this use case where every `None` maps to a simple default. However, `if let` / `match` would be equally correct and would be preferred if the `None` case required complex logic or side effects (e.g., logging a warning).

### Direct field access without Option handling

Not possible in Rust -- the compiler enforces `Option` unwrapping. This is noted for completeness since in other languages (JavaScript, Python) direct access on nullable fields is a common source of runtime errors.

---

## Summary Table

| Field | Type | Guard | Output Type | None Default |
|-------|------|-------|-------------|-------------|
| `cves` | `Option<Vec<String>>` | `as_ref().cloned().unwrap_or_default()` | `Vec<String>` | `vec![]` (empty) |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | `as_ref().map(\|p\| p.len() as u32).unwrap_or(0)` | `u32` | `0` |
| `severity_counts` | `Option<HashMap<String, u32>>` | `as_ref().cloned().unwrap_or_default()` | `HashMap<String, u32>` | `HashMap::new()` (empty) |

All guards are applied at the point of extraction in `extract_vulnerability_summary()`. The output `VulnerabilitySummary` struct uses non-optional types exclusively, so downstream consumers never need to handle `None` -- the defensive boundary is fully encapsulated in the extractor method.

---

## Test Coverage for Null Guards

| Test | What it verifies about null guards |
|------|-----------------------------------|
| `test_extract_summary_all_none_fields` | All three guards produce correct defaults simultaneously when every field is `None` |
| `test_extract_summary_mixed_some_none_cves_only` | `cves` guard passes through `Some` value while `affected_packages` and `severity_counts` guards produce defaults |
| `test_extract_summary_mixed_some_none_packages_only` | `affected_packages` guard passes through `Some` value while `cves` and `severity_counts` guards produce defaults |
| `test_extract_summary_mixed_some_none_severity_only` | `severity_counts` guard passes through `Some` value while `cves` and `affected_packages` guards produce defaults |
| `test_extract_summary_all_fields_populated` | All three guards pass through `Some` values correctly (no false defaults) |
| `test_cve_count_matches_cve_list_length` | The `cves` guard maintains the invariant that `cve_count == cve_list.len()` across `None`, empty `Some`, and populated `Some` inputs |

Each nullable field is tested in isolation (the "mixed" tests) and in combination (all-None, all-Some), ensuring that guards default independently and do not interfere with each other.
