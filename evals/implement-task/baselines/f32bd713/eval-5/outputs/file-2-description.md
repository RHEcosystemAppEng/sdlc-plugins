# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration registry so the migration runner discovers and executes it.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module, following the existing pattern:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in `migrations()` function

Add the new migration to the `vec![]` inside the `migrations()` function, after the existing `m0001_initial` entry:

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

### Key Design Decisions

1. **Ordering**: The new migration is appended after `m0001_initial` to maintain chronological ordering. Migrations execute in the order they appear in the vec, so this ensures `m0002` runs after `m0001`.

2. **Minimal change**: Only two additions -- the module declaration and the vec entry. No other modifications to `lib.rs` are needed.

### Conventions Applied

- Migration modules are declared at the top of `lib.rs`
- Each migration is registered as `Box::new(<module>::Migration)` in the `migrations()` vec
- Migrations are listed in sequential order matching their numeric prefix
