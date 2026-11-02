# Defensive Property Access Analysis — TC-9211

## Why Guards Are Needed

The `AdvisoryIngestResult` struct is produced by `IngestorService::ingest_advisory()` in the
**ingestor** module (`modules/ingestor/src/service/mod.rs`). The consumer is
`AdvisoryService::extract_vulnerability_summary()` in the **fundamental** module
(`modules/fundamental/src/advisory/service/advisory.rs`).

**The data crosses a module boundary.** The ingestor module's schema uses `Option<T>` types
for all three aggregate fields, meaning the producer explicitly allows `None` values. The
producer may return `None` when:
- The advisory document lacks CVE references
- The advisory has no package-level detail
- Severity metadata is absent from the source document

Because the consumer operates in a different module from the producer, it cannot assume the
producer's internal state or rely on informal guarantees. The `Option<T>` type signature is
the contract — guards must handle `None` at every access point. Additionally, the producer's
schema may evolve independently (e.g., adding new optional fields or changing when `None` is
returned), so defensive access future-proofs the consumer against upstream changes.

## Nullable Fields Requiring Guards

### 1. `cves: Option<Vec<String>>`

**What it contains**: List of CVE identifiers (e.g., `["CVE-2024-1234", "CVE-2024-5678"]`).

**When it is None**: The advisory has no CVE references — some advisory formats report
affected products without linking to specific CVE IDs.

**Guard pattern**: `unwrap_or_default()` via `as_ref().map().unwrap_or_default()`

```rust
let cve_list = result.cves.as_ref()
    .map(|v| v.clone())
    .unwrap_or_default();  // Vec::default() = empty Vec
let cve_count = cve_list.len() as u32;
```

**Why this pattern**: `Vec<String>` implements `Default` (empty vec), making
`unwrap_or_default()` idiomatic. Using `as_ref()` avoids consuming the Option, and
`map(|v| v.clone())` produces an owned `Vec<String>` for the output struct. Direct access
like `result.cves.len()` or `result.cves.join(",")` would fail to compile on `Option<Vec<String>>`
and `.unwrap()` would panic at runtime when None.

### 2. `affected_packages: Option<Vec<AffectedPackage>>`

**What it contains**: List of packages impacted by the advisory, with version ranges and
remediation status.

**When it is None**: Advisories without package-level detail — some sources provide
vulnerability descriptions without enumerating affected packages.

**Guard pattern**: `map()` + `unwrap_or(0)` for the derived count

```rust
let affected_package_count = result.affected_packages.as_ref()
    .map(|pkgs| pkgs.len() as u32)
    .unwrap_or(0);
```

**Why this pattern**: We only need the count, not the full list. `map()` transforms the
`Option<&Vec<AffectedPackage>>` into `Option<u32>`, and `unwrap_or(0)` provides the
default. This avoids cloning the entire `Vec<AffectedPackage>` when only the length is
needed. Directly calling `result.affected_packages.len()` would fail to compile on
`Option<Vec<AffectedPackage>>`, and iterating the Option without unwrapping would skip
the computation silently.

### 3. `severity_counts: Option<HashMap<String, u32>>`

**What it contains**: Counts per severity level, e.g., `{"critical": 3, "high": 5, "medium": 12}`.

**When it is None**: Severity metadata is absent from the source advisory document —
not all advisory formats include CVSS scores or severity classifications.

**Guard pattern**: `unwrap_or_default()` via `as_ref().map().unwrap_or_default()`

```rust
let severity_breakdown = result.severity_counts.as_ref()
    .map(|m| m.clone())
    .unwrap_or_default();  // HashMap::default() = empty HashMap
```

**Why this pattern**: `HashMap<String, u32>` implements `Default` (empty map), making
`unwrap_or_default()` idiomatic. The output struct needs an owned `HashMap`, so `clone()`
via `map()` produces the owned value. Directly accessing keys like
`result.severity_counts["critical"]` would fail on `Option<HashMap>`, and `.unwrap()`
would panic when None.

## Patterns NOT Used (and Why)

| Pattern | Why Avoided |
|---------|-------------|
| `.unwrap()` | Panics on `None` — violates the "handle without panicking" acceptance criterion |
| Direct field access (`.len()`, `.join()`, `.iter()`) | Does not compile on `Option<T>` — requires unwrapping first |
| `if let Some(v) = field { ... } else { default }` | Valid but verbose for simple default cases; `unwrap_or_default()` is more idiomatic in Rust |
| `match field { Some(v) => ..., None => ... }` | Equivalent to `if let` — appropriate for complex branching but overkill for default value extraction |
| `_` prefix to suppress warnings | Does not solve the problem — the fields are actively used, not ignored |

## Test Coverage for Guards

The test suite includes a dedicated all-None test case:

- **Input**: `AdvisoryIngestResult { cves: None, affected_packages: None, severity_counts: None }`
- **Expected output**: `VulnerabilitySummary { cve_count: 0, cve_list: [], affected_package_count: 0, severity_breakdown: {} }`

This test verifies that all three guards produce sensible defaults simultaneously,
catching any guard that was missed or incorrectly implemented. The mixed Some/None test
further verifies that each field's guard operates independently.
