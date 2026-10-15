# File 4: modules/fundamental/src/advisory/model/mod.rs

## Action: MODIFY

## Purpose

Register the new `severity_summary` model module so it is accessible from other parts
of the crate.

## Detailed Changes

### Add module declaration

Add the following line alongside the existing module declarations:

```rust
pub mod severity_summary;
```

This should be added after the existing `pub mod summary;` and `pub mod details;`
declarations, maintaining alphabetical ordering if the existing declarations follow
that convention, or appended at the end otherwise.

### Before (expected current state)

```rust
pub mod summary;
pub mod details;
```

### After

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

(Alphabetical ordering: details, severity_summary, summary.)

### Convention Conformance

- Follows the same `pub mod <name>;` pattern as existing module registrations.
- Maintains the module registration pattern observed in sibling `model/mod.rs` files
  (e.g., `sbom/model/mod.rs` exports `summary` and `details`).
