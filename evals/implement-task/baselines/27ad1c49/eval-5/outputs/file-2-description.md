# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration list so
it is discovered and executed by SeaORM's migration runner.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module, following the existing `m0001_initial`
declaration:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations vector

Add the new migration to the `vec![]` inside the `migrations()` function, after the
existing `m0001_initial` entry:

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

### Pre-implementation verification

Before modifying this file, verify:
- Use `mcp__serena_backend__get_symbols_overview` on `migration/src/lib.rs` to see the current structure
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `migrations()` function to see the exact current vec contents and registration pattern
- Confirm the module declaration ordering convention (alphabetical or chronological)

### Editing approach

Use `mcp__serena_backend__replace_symbol_body` to update the `migrations()` function body,
or fall back to Edit tool if Serena symbolic editing is unavailable for this change.
For the mod declaration, use `mcp__serena_backend__insert_after_symbol` to add after the
`m0001_initial` mod declaration, or fall back to Edit tool.
