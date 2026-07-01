# File 2: `migration/src/lib.rs` (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration list so that SeaORM discovers and executes it.

## Pre-Implementation Inspection

Before modifying this file, inspect it using Serena:

```
mcp__serena_backend__get_symbols_overview("migration/src/lib.rs")
```

This reveals the current module declarations and the `migrations()` function structure.

Also use `find_symbol` to read the `migrations()` function body:

```
mcp__serena_backend__find_symbol("migrations", include_body=true)
```

## Detailed Changes

### 1. Add Module Declaration

Add a new module declaration for `m0002_drop_advisory_status` after the existing `m0001_initial` declaration:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### 2. Register in migrations() Function

Add the new migration to the `vec![]` in the `migrations()` function, following the same pattern used for `m0001_initial`:

```rust
// Before:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}

// After:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Conventions Applied

- Module declaration follows alphabetical/sequential ordering after existing migrations
- Registration in `migrations()` follows the `Box::new(<module>::Migration)` pattern established by `m0001_initial`
- New entry is appended at the end of the vec (migrations run in order)

## Scope Verification

- Only two lines are added to this file: one module declaration and one vec entry
- No other functions or imports are modified
- The change is minimal and scoped to migration registration only
