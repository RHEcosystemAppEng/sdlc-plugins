# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration list so the SeaORM migration runner can discover and execute it.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module alongside the existing `m0001_initial` declaration.

**Before:**
```rust
mod m0001_initial;
```

**After:**
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` in the `migrations()` function, after `m0001_initial`, following the same `Box::new()` pattern.

**Before:**
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

**After:**
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Conventions Applied

- **Module declaration**: Added `mod m0002_drop_advisory_status;` following the same pattern as `mod m0001_initial;`
- **Registration pattern**: Added `Box::new(m0002_drop_advisory_status::Migration)` in the `migrations()` vec, matching the existing `Box::new(m0001_initial::Migration)` pattern
- **Ordering**: The new migration is placed after `m0001_initial` in sequential order, maintaining the numeric ordering convention
- **Minimal changes**: Only two additions to an existing file -- a module declaration and a vec entry. No other modifications to `lib.rs` are needed.

## Implementation Notes Adherence

- Registers the new migration in `migration/src/lib.rs` by adding it to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial` as specified in the task description
