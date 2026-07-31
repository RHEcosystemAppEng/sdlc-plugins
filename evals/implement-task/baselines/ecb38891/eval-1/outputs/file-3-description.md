# File 3: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Purpose
Register the new `severity_summary` model submodule in the advisory model module.

## Pre-Implementation Inspection
Before modifying, read this file to confirm the pattern of existing module registrations (e.g., `pub mod summary;`, `pub mod details;`).

## Changes

### Add module registration

Add the following line alongside the existing module declarations:

```rust
pub mod severity_summary;
```

This follows the same pattern as the existing `pub mod summary;` and `pub mod details;` declarations in this file.
