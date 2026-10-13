# Defensive Property Access Analysis for TC-9211

## Why defensive access is needed

The `AdvisoryIngestResult` struct is defined in `modules/ingestor/src/service/mod.rs`
and is produced by `IngestorService::ingest_advisory()`. The vulnerability summary
extractor in `modules/fundamental/src/advisory/service/advisory.rs` consumes this
struct across a module boundary. Per the SKILL.md Step 6 guidance on "Defensive
property access on external data":

> When consuming data produced by another module, service, or external API, add
> null/undefined guards before accessing nested properties -- especially arrays and
> objects that may be absent even when the upstream type signature suggests otherwise.

The producer's schema explicitly allows `None` for all three aggregate fields.
The ingestor may return `None` when:
- An advisory has no CVE references (`cves`)
- An advisory lacks package-level detail (`affected_packages`)
- Severity metadata is absent from the advisory (`severity_counts`)

Because the data crosses the ingestor-to-fundamental module boundary, the producer's
schema may also evolve independently. Accessing any `Option` field without a guard
would cause a panic at runtime.

## Nullable Fields and Guard Patterns

### Field 1: `cves: Option<Vec<String>>`

- **Why nullable**: May be `None` when the advisory has no CVE references.
- **Guard pattern**: `unwrap_or_default()`
- **Usage**:
  ```rust
  let cve_list = ingest_result.cves.unwrap_or_default();
  let cve_count = cve_list.len() as u32;
  ```
- **Rationale**: `unwrap_or_default()` is idiomatic Rust for `Option<Vec<T>>` --
  `Vec::default()` produces an empty `Vec`, which is exactly the fallback the task
  specifies ("use an empty Vec and set cve_count to 0"). This avoids both `.unwrap()`
  (which panics on `None`) and verbose `match` blocks. Since we need to consume the
  inner `Vec` (to store it in `VulnerabilitySummary.cve_list`), `unwrap_or_default()`
  is preferred over `as_ref()` because it takes ownership directly.

### Field 2: `affected_packages: Option<Vec<AffectedPackage>>`

- **Why nullable**: May be `None` for advisories without package-level detail.
- **Guard pattern**: `map()` combined with `unwrap_or(0)`
- **Usage**:
  ```rust
  let affected_package_count = ingest_result
      .affected_packages
      .as_ref()
      .map(|pkgs| pkgs.len() as u32)
      .unwrap_or(0);
  ```
- **Rationale**: We only need the count, not the full list. Using `as_ref()` avoids
  moving the `Option` contents, then `map()` transforms `Some(&Vec<AffectedPackage>)`
  into `Some(u32)`, and `unwrap_or(0)` provides the default. This is more efficient
  than `unwrap_or_default()` followed by `.len()` because it avoids allocating an
  empty `Vec` when the field is `None`. An alternative pattern that also works:
  ```rust
  let affected_package_count = ingest_result
      .affected_packages
      .unwrap_or_default()
      .len() as u32;
  ```
  Both are safe; the `as_ref().map().unwrap_or()` chain is slightly more idiomatic
  when only a derived value is needed.

### Field 3: `severity_counts: Option<HashMap<String, u32>>`

- **Why nullable**: May be `None` when severity metadata is absent from the advisory.
- **Guard pattern**: `unwrap_or_default()`
- **Usage**:
  ```rust
  let severity_breakdown = ingest_result.severity_counts.unwrap_or_default();
  ```
- **Rationale**: `unwrap_or_default()` is idiomatic for `Option<HashMap<K, V>>` --
  `HashMap::default()` produces an empty map. Since the task requires storing the
  full map in `VulnerabilitySummary.severity_breakdown`, we take ownership. This is
  the simplest and most readable pattern for this case.

## Summary Table

| Field | Type | Guard Pattern | Default Value |
|---|---|---|---|
| `cves` | `Option<Vec<String>>` | `unwrap_or_default()` | `vec![]` |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | `as_ref().map(\|p\| p.len() as u32).unwrap_or(0)` | `0` (count only) |
| `severity_counts` | `Option<HashMap<String, u32>>` | `unwrap_or_default()` | `HashMap::new()` |

## Anti-patterns avoided

- **`.unwrap()` directly**: Panics on `None`. Never used on any of the three fields.
- **`.expect("should exist")`**: Same panic risk. Not appropriate for cross-module data
  where `None` is a valid, documented state.
- **Unchecked field access without guard**: Any `Option` field accessed without
  `unwrap_or_default()`, `map()`, `if let`, or `match` could panic. All three fields
  are guarded.
