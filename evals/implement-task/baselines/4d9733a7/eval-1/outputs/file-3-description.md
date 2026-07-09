# File 3: modules/fundamental/src/advisory/model/mod.rs

**Action**: Modify (existing file)

## Current State

This file registers the model sub-modules for the advisory domain. It currently contains:

```rust
pub mod summary;
pub mod details;
```

## Changes

### Register new model module

Add a new module declaration for the severity summary model:

```rust
pub mod severity_summary;
```

This makes the `SeveritySummary` struct available to the rest of the codebase via `crate::advisory::model::severity_summary::SeveritySummary`. The addition follows the existing pattern of one `pub mod` declaration per model file, in alphabetical order with existing declarations.
