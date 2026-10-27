# File 2: migration/src/lib.rs (MODIFY)

## Purpose
Register the new migration module in the migration list.

## Changes

### 1. Add module declaration
Add at the top of the file, after existing module declarations:
```rust
mod m0002_drop_advisory_status;
```

### 2. Register in migrations() function
Add the new migration to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry:

```rust
pub fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // NEW
    ]
}
```

## Patterns followed
- Module declaration follows existing `mod m0001_initial;` pattern
- Registration follows existing `Box::new(m0001_initial::Migration)` pattern in the `vec![]`
- Chronological ordering maintained (m0002 after m0001)

## Pre-modification inspection
Before modifying, would inspect `migration/src/lib.rs` using `mcp__serena_backend__get_symbols_overview` to confirm:
- The `migrations()` function exists and returns `Vec<Box<dyn MigrationTrait>>`
- The current registration pattern uses `Box::new(...)` in a `vec![]`
- `m0001_initial` is the last registered migration
