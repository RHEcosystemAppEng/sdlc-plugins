# Implementation Plan — TC-9210: Add severity-sorted remediation list to SBOM risk report

## Step 0 — Validate Project Configuration

CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: project key TC, Cloud ID, field IDs present
- Code Intelligence: serena_backend configured with rust-analyzer

Configuration is valid. Proceeding.

## Step 1 — Parse Task Description

- **Repository:** trustify-backend
- **Target Branch:** main
- **Jira ID:** TC-9210
- **Files to Modify:**
  1. `modules/fundamental/src/sbom/service/sbom.rs` — add severity-sorted remediation list builder
  2. `modules/fundamental/src/sbom/endpoints/get.rs` — include remediation list in response
- **Files to Create:**
  1. `tests/api/sbom_remediation.rs` — integration tests for remediation list
- **No Target PR** — standard flow
- **No Bookend Type** — standard implementation
- **Dependencies:** None

## Step 1.5 — Verify Description Integrity

Fetch comments on TC-9210. Search for the `[sdlc-workflow] Description digest:` marker. If no digest comment is found, log a warning and proceed (backward compatibility). If found, compute the current digest with `python3 scripts/sha256-digest.py`, compare format tags and hex hashes. On match, proceed silently. On mismatch, alert the user and pause.

## Step 4 — Understand the Code

### Code inspection targets

Before modifying any files, inspect the following to understand existing patterns:

1. **`modules/fundamental/src/sbom/service/sbom.rs`** — understand SbomService structure, existing methods for fetching related data, import patterns
2. **`modules/fundamental/src/sbom/endpoints/get.rs`** — understand how SbomDetails is constructed and returned, how additional data is included in responses
3. **`modules/fundamental/src/advisory/service/advisory.rs`** — locate the existing `SEVERITY_ORDER` constant, understand its type and usage pattern (see symbol-search.md for full deduplication analysis)
4. **`modules/fundamental/src/sbom/model/details.rs`** — understand the SbomDetails struct to plan where `remediations` field will be added
5. **`tests/api/sbom.rs`** — inspect sibling test patterns for assertion style, setup/teardown, naming conventions

### Symbol deduplication — SEVERITY_ORDER

**Critical finding:** The task requires sorting by severity using a `SEVERITY_ORDER` constant. Before declaring a new one, search the entire `modules/fundamental/src/` package:

- **Search:** Grep/find_symbol for `SEVERITY_ORDER` across `modules/fundamental/src/**/*.rs`
- **Result:** Found existing definition at `modules/fundamental/src/advisory/service/advisory.rs`:
  ```rust
  const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
  ```
- **Decision:** Make it `pub const` and import it in the sbom service. No new constant declared. See `symbol-search.md` for full analysis.

### Convention conformance analysis

From sibling inspection:
- **Error handling:** All service methods return `Result<T, AppError>` with `.context()` for error wrapping
- **Service structure:** Methods are async, take `&self` and relevant IDs, use SeaORM queries
- **Endpoint pattern:** Handler functions extract path parameters, call service methods, return JSON
- **Model pattern:** Response structs use `#[derive(Serialize, Deserialize, Debug)]`
- **Test patterns:** Integration tests use real PostgreSQL, assert on `resp.status()` and response body values
- **Import organization:** Grouped by crate (std, external, internal)

## Step 5 — Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9210
```

## Step 6 — Implement Changes

### 6.1 — Make SEVERITY_ORDER public in advisory module

**File:** `modules/fundamental/src/advisory/service/advisory.rs`

Change:
```rust
const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```
to:
```rust
pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

Re-export through `modules/fundamental/src/advisory/service/mod.rs` if needed for clean import paths.

### 6.2 — Add RemediationItem model

**File:** `modules/fundamental/src/sbom/model/details.rs` (within existing file, no new file needed)

Add a new struct within the existing details module:

```rust
/// A single remediation entry linking an SBOM to an advisory with severity.
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct RemediationItem {
    pub advisory_id: String,
    pub severity: String,
    pub title: String,
    pub fix_version: Option<String>,
}
```

Add `remediations: Vec<RemediationItem>` field to the existing `SbomDetails` struct.

### 6.3 — Add remediation list builder to SbomService

**File:** `modules/fundamental/src/sbom/service/sbom.rs`

Import the existing `SEVERITY_ORDER` constant:
```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

Add a new method to `SbomService`:

```rust
/// Builds a severity-sorted list of remediations for the given SBOM.
pub async fn get_remediation_list(
    &self,
    sbom_id: &str,
    connection: &impl ConnectionTrait,
) -> Result<Vec<RemediationItem>, AppError> {
    // Fetch advisories related to this SBOM via sbom_advisory join table
    // Map each advisory to RemediationItem { advisory_id, severity, title, fix_version }
    // Sort using SEVERITY_ORDER: position in array determines priority
    let mut items = /* ... fetch and map ... */;
    items.sort_by_key(|item| {
        SEVERITY_ORDER
            .iter()
            .position(|&s| s == item.severity.to_lowercase())
            .unwrap_or(SEVERITY_ORDER.len())
    });
    Ok(items)
}
```

Key: imports `SEVERITY_ORDER` from advisory module — no duplication.

### 6.4 — Include remediation list in SBOM details response

**File:** `modules/fundamental/src/sbom/endpoints/get.rs`

In the handler for `GET /api/v2/sbom/{id}`, call `sbom_service.get_remediation_list()` and include the result in the `SbomDetails` response under the `remediations` field.

## Step 7 — Write Tests

**File:** `tests/api/sbom_remediation.rs`

Following sibling test conventions from `tests/api/sbom.rs`:

```rust
/// Verifies that the remediation list is sorted by severity (Critical first, None last).
#[test]
async fn test_remediation_list_sorted_by_severity() {
    // Given an SBOM with advisories of varying severity
    // ...setup...

    // When fetching SBOM details
    // ...GET /api/v2/sbom/{id}...

    // Then remediations are ordered Critical > High > Medium > Low > None
    assert_eq!(remediations[0].severity, "critical");
    assert_eq!(remediations[1].severity, "high");
    assert_eq!(remediations[2].severity, "medium");
    assert_eq!(remediations[3].severity, "low");
    assert_eq!(remediations[4].severity, "none");
}

/// Verifies that an SBOM with no advisories returns an empty remediation list.
#[test]
async fn test_empty_sbom_returns_empty_remediation_list() {
    // Given an SBOM with no linked advisories
    // ...setup...

    // When fetching SBOM details
    // ...GET /api/v2/sbom/{id}...

    // Then the remediations list is empty
    assert!(remediations.is_empty());
}

/// Verifies that multiple advisories of the same severity maintain stable ordering.
#[test]
async fn test_same_severity_stable_ordering() {
    // Given an SBOM with multiple high-severity advisories
    // ...setup with known advisory IDs...

    // When fetching SBOM details
    // ...GET /api/v2/sbom/{id}...

    // Then all are "high" severity and appear in stable order
    assert_eq!(remediations[0].severity, "high");
    assert_eq!(remediations[1].severity, "high");
    // Value-based assertions on specific advisory IDs
    assert_eq!(remediations[0].advisory_id, expected_first_id);
    assert_eq!(remediations[1].advisory_id, expected_second_id);
}
```

Tests use value-based assertions (per skill guidance), not just `.count() > 0` or `.any()`.

Run tests:
```bash
cargo metadata --no-deps --format-version 1  # resolve crate name for modules/fundamental
cargo test -p trustify-module-fundamental
```

## Step 8 — Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id} response includes `remediations` field — added via endpoint handler
- [x] Advisories sorted Critical > High > Medium > Low > None — uses `SEVERITY_ORDER` for sort key
- [x] Uses existing `SEVERITY_ORDER` from advisory module — imported via `use crate::advisory::service::advisory::SEVERITY_ORDER`, no duplicate definition
- [x] RemediationItem includes advisory_id, severity, title, fix_version — struct defined with all four fields

## Step 9 — Self-Verification

### Scope containment
Files modified/created:
1. `modules/fundamental/src/advisory/service/advisory.rs` — visibility change only (`const` → `pub const`)
2. `modules/fundamental/src/sbom/service/sbom.rs` — listed in Files to Modify
3. `modules/fundamental/src/sbom/endpoints/get.rs` — listed in Files to Modify
4. `tests/api/sbom_remediation.rs` — listed in Files to Create

Note: `advisory.rs` is not listed in Files to Modify but requires a minimal visibility change (`const` → `pub const`) to enable reuse. This would be flagged as out-of-scope in Step 9's scope containment check and presented to the user for approval. The alternative (duplicating the constant) is worse per the skill's symbol deduplication guidance.

### Symbol deduplication check
No new `SEVERITY_ORDER` constant declared anywhere. The existing one is reused. Verified by searching for `SEVERITY_ORDER` across the diff.

### Dead parameter detection
No parameters removed — not applicable.

### Module-level test
```bash
cargo metadata --no-deps --format-version 1
cargo test -p trustify-module-fundamental
```

Crate name resolved via `cargo metadata`, not from the nearest `Cargo.toml` (which may be a virtual workspace manifest).

## Step 10 — Commit and Push

```bash
git add modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/sbom/service/sbom.rs \
       modules/fundamental/src/sbom/endpoints/get.rs \
       tests/api/sbom_remediation.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(sbom): add severity-sorted remediation list to risk report

Add RemediationItem struct and SbomService::get_remediation_list() method
that sorts advisories by severity using the existing SEVERITY_ORDER constant
from the advisory module. Include remediation list in GET /api/v2/sbom/{id}
response.

Implements TC-9210"

git push -u origin TC-9210
gh pr create --base main --title "feat(sbom): add severity-sorted remediation list" --body "..."
```

## Step 11 — Update Jira

- Set `customfield_10875` (Git Pull Request) to PR URL in ADF format
- Add comment with PR link and change summary
- Transition TC-9210 to In Review
