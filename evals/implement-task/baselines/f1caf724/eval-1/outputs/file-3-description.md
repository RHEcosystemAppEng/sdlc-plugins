# File 3: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Pre-Implementation Inspection

Read this file to see how existing model submodules (summary, details) are registered.

## Changes

### Register the new severity_summary model submodule

Add the following line alongside existing `pub mod` statements:

```rust
pub mod severity_summary;
```

This follows the pattern of existing registrations like `pub mod summary;` and `pub mod details;`.
