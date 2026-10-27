# Defensive Property Access Analysis — TC-9211

## Why Defensive Access Is Needed

The `AdvisoryIngestResult` struct is defined in the **ingestor module** (`modules/ingestor/src/service/mod.rs`) and consumed in the **fundamental module** (`modules/fundamental/src/advisory/service/advisory.rs`). The data crosses a module boundary — the producer's schema uses `Option<T>` for all three aggregate fields, meaning any or all of them may be `None` at runtime.

Because the producer (`IngestorService::ingest_advisory()`) is an independent module:
- Its schema may evolve independently of the consumer
- The `Option` types are an explicit contract that `None` is a valid state
- Advisory documents in the wild may lack CVE references, package-level detail, or severity metadata
- Accessing these fields without guards would cause a panic on `.unwrap()` — unacceptable in a service that processes external data

## Fields Requiring Guards

### 1. `cves: Option<Vec<String>>`

**What it represents**: List of CVE identifiers (e.g., `["CVE-2024-1234"]`).

**When it is None**: The advisory has no CVE references — for example, vendor-specific advisories that use proprietary identifiers instead of CVE IDs.

**Guard pattern used**:
```rust
let cve_list = result.cves.as_ref()
    .map(|v| v.clone())
    .unwrap_or_default();
let cve_count = cve_list.len() as u32;
```

- `as_ref()` borrows the `Option<Vec<String>>` as `Option<&Vec<String>>` to avoid consuming the original
- `map(|v| v.clone())` clones the inner Vec when present
- `unwrap_or_default()` returns an empty `Vec<String>` when `None`
- `cve_count` is derived from `cve_list.len()`, ensuring consistency

**NOT used**: `.unwrap()` — would panic on None. `.expect()` — same issue with a custom message.

### 2. `affected_packages: Option<Vec<AffectedPackage>>`

**What it represents**: Packages impacted by the advisory.

**When it is None**: The advisory does not include package-level impact detail — for example, high-level advisories that describe a vulnerability class without enumerating specific affected packages.

**Guard pattern used**:
```rust
let affected_package_count = result.affected_packages.as_ref()
    .map(|pkgs| pkgs.len() as u32)
    .unwrap_or(0);
```

- `as_ref()` borrows without consuming
- `map(|pkgs| pkgs.len() as u32)` extracts the count when present
- `unwrap_or(0)` defaults to 0 when `None`

Since only the count is needed (not the package list itself), we avoid cloning the entire Vec and use `map()` to extract the scalar value.

**NOT used**: Direct `.len()` on the `Option` — `Option<Vec<T>>` does not have a `.len()` method; calling it would be a compile error. `.unwrap().len()` — would panic on None.

### 3. `severity_counts: Option<HashMap<String, u32>>`

**What it represents**: Counts of vulnerabilities per severity level (e.g., `{"critical": 2, "high": 5}`).

**When it is None**: The advisory lacks severity metadata — for example, advisories from sources that do not assign CVSS scores or severity ratings.

**Guard pattern used**:
```rust
let severity_breakdown = result.severity_counts.as_ref()
    .cloned()
    .unwrap_or_default();
```

- `as_ref()` borrows without consuming
- `.cloned()` clones the `HashMap` when present (equivalent to `map(|m| m.clone())`)
- `unwrap_or_default()` returns an empty `HashMap<String, u32>` when `None` (HashMap implements Default)

**NOT used**: `.unwrap()` — would panic on None. Direct iteration (`.iter()`, `.keys()`) on the `Option` — not available without unwrapping first.

## Guard Pattern Summary

| Field | Type | Guard | Default on None |
|-------|------|-------|-----------------|
| `cves` | `Option<Vec<String>>` | `as_ref().map(\|v\| v.clone()).unwrap_or_default()` | `vec![]` (empty Vec) |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | `as_ref().map(\|pkgs\| pkgs.len() as u32).unwrap_or(0)` | `0` |
| `severity_counts` | `Option<HashMap<String, u32>>` | `as_ref().cloned().unwrap_or_default()` | `HashMap::new()` (empty map) |

All patterns are idiomatic Rust for handling `Option<T>`:
- **`unwrap_or_default()`** — used when T implements `Default` and the default is the correct fallback
- **`as_ref()`** — used to borrow the inner value without consuming the `Option`
- **`map()`** — used to transform the inner value (e.g., extract `.len()`) while preserving the `Option` wrapper
- **`cloned()`** — used to clone a borrowed inner value when ownership is needed

No `.unwrap()` or `.expect()` calls are used anywhere in the implementation. Every access path handles `None` explicitly.

## Test Coverage for Null Guards

The test suite includes explicit all-None coverage:

1. **`test_extract_vulnerability_summary_all_none`**: Constructs an `AdvisoryIngestResult` with `cves: None`, `affected_packages: None`, `severity_counts: None`. Verifies the resulting `VulnerabilitySummary` has `cve_count: 0`, `cve_list: []`, `affected_package_count: 0`, `severity_breakdown: {}`.

2. **`test_extract_vulnerability_summary_mixed_some_none`**: Constructs an `AdvisoryIngestResult` with `cves: Some(...)` but `affected_packages: None` and `severity_counts: None`. Verifies each `None` field defaults independently without affecting the `Some` field.

3. **`test_cve_count_matches_cve_list_length`**: Tests with `cves: None` as one of the parameterized cases, confirming the `None` → 0 count path.

These tests ensure the guards work correctly across all nullable field combinations — including the worst-case scenario where every field is `None`.
