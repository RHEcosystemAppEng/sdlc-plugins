# File 1: migration/src/lib.rs (Modify)

## Pre-change Inspection

Before modifying this file, read it using `mcp__serena_backend__get_symbols_overview` (or `Read` as fallback) to understand:
- The current module declarations (e.g., `mod m0001_initial;`)
- The `migrations()` function structure and how it populates the `vec![]`
- The return type and any wrapper patterns

## Changes

### 1. Add module declaration

Add a new module declaration for the migration:

```rust
mod m0002_drop_advisory_status;
```

This should be placed after the existing `mod m0001_initial;` declaration, maintaining alphabetical/numerical ordering.

### 2. Register migration in `migrations()` function

Inside the `migrations()` function, add the new migration to the `vec![]` following the pattern of `m0001_initial`:

```rust
Box::new(m0002_drop_advisory_status::Migration),
```

This entry must appear after `m0001_initial` in the vec to ensure migrations execute in the correct order.

## Expected Result

The file should look approximately like:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;

// ... existing code ...

fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Verification

- The new module must compile (no unresolved imports)
- The migrations() function must return both migrations in order
- `cargo check -p migration` should pass
