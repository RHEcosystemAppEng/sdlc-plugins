# Defensive Property Access Analysis: TC-9211

## Context

The `AdvisoryIngestResult` struct (defined in `modules/ingestor/src/service/mod.rs`)
crosses a module boundary from the `ingestor` crate into the `fundamental` crate.
Its aggregate data fields use `Option<T>`, meaning they may be `None` at runtime
even when the upstream type signature declares them. The producer's schema may evolve
independently, so all nullable fields must be guarded defensively.

## Fields Requiring Guards

### 1. `cves: Option<Vec<String>>`

**Why it needs a guard:** This field may be `None` when the advisory has no CVE
references. Accessing `.len()`, iterating, or calling `.join()` on a `None` value
would cause a panic (unwrap on None) or a compile error if not handled.

**Guard pattern:** `unwrap_or_default()`

```rust
let cve_list = ingest_result.cves
    .as_ref()
    .cloned()
    .unwrap_or_default();  // None -> empty Vec<String>
let cve_count = cve_list.len() as u32;
```

**Why this pattern:** `unwrap_or_default()` is idiomatic Rust for `Option<Vec<T>>`.
`Vec::default()` produces an empty vector, which is the correct semantic default --
zero CVEs. Using `.as_ref().cloned()` avoids consuming the original value (in case
the `AdvisoryIngestResult` is borrowed). The `cve_count` is derived from the
already-unwrapped `cve_list.len()`, ensuring consistency between the count and the
list (acceptance criterion: "cve_count matches the length of cve_list").

**Alternative considered:** `.map_or_else(Vec::new, |v| v.clone())` -- functionally
equivalent but less idiomatic than `unwrap_or_default()` for types implementing
`Default`.

---

### 2. `affected_packages: Option<Vec<AffectedPackage>>`

**Why it needs a guard:** This field may be `None` for advisories without
package-level detail. The extractor only needs the count (not the full list), so
accessing `.len()` on `None` would panic.

**Guard pattern:** `map` + `unwrap_or`

```rust
let affected_package_count = ingest_result.affected_packages
    .as_ref()
    .map(|pkgs| pkgs.len() as u32)
    .unwrap_or(0);
```

**Why this pattern:** Since we only need the count (not the full vector), using
`.map(|pkgs| pkgs.len())` followed by `.unwrap_or(0)` is more efficient than
cloning the entire vector just to call `.len()`. The default of `0` matches the
task requirement: "When `affected_packages` is `None`, set
`affected_package_count` to 0".

**Alternative considered:** `.unwrap_or_default()` after mapping -- equivalent
since `u32::default()` is `0`, but `.unwrap_or(0)` is more explicit about the
intent.

---

### 3. `severity_counts: Option<HashMap<String, u32>>`

**Why it needs a guard:** This field may be `None` when severity metadata is absent
from the advisory. Accessing keys, iterating, or merging into downstream data
structures on `None` would panic.

**Guard pattern:** `unwrap_or_default()`

```rust
let severity_breakdown = ingest_result.severity_counts
    .as_ref()
    .cloned()
    .unwrap_or_default();  // None -> empty HashMap<String, u32>
```

**Why this pattern:** `HashMap::default()` produces an empty map, which is the
correct semantic default -- no severity data available. This matches the task
requirement: "When `severity_counts` is `None`, use an empty `HashMap`". The
pattern mirrors the `cves` field handling for consistency.

**Alternative considered:** Using `HashMap::new()` via `unwrap_or_else(HashMap::new)`
-- functionally identical to `unwrap_or_default()` since `HashMap::default()` calls
`HashMap::new()` internally.

---

## Summary Table

| Field | Type | Guard Pattern | Default Value | Rationale |
|---|---|---|---|---|
| `cves` | `Option<Vec<String>>` | `.unwrap_or_default()` | `vec![]` (empty) | Advisory may lack CVE references |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | `.map(\|v\| v.len()).unwrap_or(0)` | `0` | Only count needed; avoids clone |
| `severity_counts` | `Option<HashMap<String, u32>>` | `.unwrap_or_default()` | `HashMap::new()` (empty) | Severity metadata may be absent |

## Design Principles Applied

1. **No panics on None:** Every `Option<T>` field is unwrapped with a fallback, never
   with `.unwrap()` or `.expect()`. This ensures the extractor never panics regardless
   of upstream data completeness.

2. **Non-optional output fields:** The `VulnerabilitySummary` struct uses non-optional
   types (`u32`, `Vec<String>`, `HashMap<String, u32>`) so downstream consumers (email
   digest rendering) do not need to add their own null checks. The guard boundary is
   at the extractor, not pushed downstream.

3. **Consistent count-list relationship:** `cve_count` is derived from
   `cve_list.len()` after unwrapping, not independently from the `Option`. This makes
   it impossible for `cve_count` to diverge from the list length.

4. **Efficiency:** For `affected_packages`, only the count is extracted (via `.map`
   and `.len()`) without cloning the full vector, since the `VulnerabilitySummary`
   does not need the package details.

5. **Idiomatic Rust:** Uses `unwrap_or_default()` for types implementing `Default`
   (`Vec`, `HashMap`), and `map` + `unwrap_or` for derived values. These are
   standard Rust patterns for defensive Option handling, preferred over `match`
   blocks or `if let` for simple default cases.

## Cross-Module Boundary Considerations

The `AdvisoryIngestResult` struct is owned by the `ingestor` crate. If the struct
evolves to add new `Option<T>` fields in the future, the extractor should be updated
to handle them. The current design makes this straightforward: each new nullable field
gets the same guard pattern (unwrap with a sensible default) and a corresponding
non-optional field in `VulnerabilitySummary`.

If `AdvisoryIngestResult` later changes a field from `Option<T>` to `T` (non-optional),
the guard code will still compile -- `unwrap_or_default()` on a non-Option value would
cause a compile error, catching the contract change at build time rather than runtime.
This is a benefit of using the Rust type system rather than runtime null checks.
