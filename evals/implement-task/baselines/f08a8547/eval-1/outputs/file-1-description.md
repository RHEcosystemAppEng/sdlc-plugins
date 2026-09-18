# File 1: Model Module Registration

**File**: `modules/fundamental/src/advisory/model/mod.rs`
**Action**: MODIFY

## Current State

This file re-exports the model submodules for the advisory domain. Based on the
repository structure, it currently contains:

```rust
pub mod summary;
pub mod details;
```

These correspond to `summary.rs` (AdvisorySummary) and `details.rs` (AdvisoryDetails).

## Changes

Add a single line to register the new `severity_summary` submodule:

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;
```

## Rationale

This follows the established pattern where each model struct lives in its own file
and is re-exported from `mod.rs`. The `severity_summary` module will contain the
`SeveritySummary` response struct defined in File 4.

## Convention Adherence

- Follows the existing `pub mod <name>;` pattern in sibling `mod.rs` files.
- Alphabetical ordering is not strictly required (siblings `summary` and `details`
  are not alphabetical), but the new entry is placed after existing entries for
  minimal diff.
