# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration list so that SeaORM's migration runner discovers and executes it.

## Pre-implementation inspection

Before modifying this file, inspect it using `mcp__serena_backend__get_symbols_overview` to understand its structure, then use `mcp__serena_backend__find_symbol` with `include_body=true` on the `migrations()` function to see:

- How `m0001_initial` is declared as a module (`mod m0001_initial;`)
- How it is referenced in the `migrations()` function's `vec![]`
- The exact syntax for `Box::new(m0001_initial::Migration)` or equivalent
- The return type of the `migrations()` function

## Detailed Changes

### Change 1: Add module declaration

Add a new `mod` declaration for the migration module, following the pattern of the existing `m0001_initial` declaration:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the pattern used for `m0001_initial`:

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

## Key implementation decisions

- The new migration is appended after `m0001_initial` to maintain chronological ordering
- The exact syntax (`Box::new(...)` vs other patterns) follows whatever is discovered in the existing code during inspection
- No other changes to `lib.rs` are needed

## Acceptance Criteria Coverage

- Migration is registered in `migration/src/lib.rs`
