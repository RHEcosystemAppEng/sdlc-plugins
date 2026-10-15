# File 2: Modify `migration/src/lib.rs`

## Action: MODIFY

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner discovers and executes it.

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

### Change 2: Register migration in `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function, after the existing `m0001_initial` entry. Migrations must be listed in sequential order.

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

## Key Design Decisions

1. **Sequential ordering**: The new migration is appended after `m0001_initial`, maintaining the chronological ordering convention.

2. **Minimal change**: Only two lines are added -- the module declaration and the registration entry. No other modifications to `lib.rs` are needed.

3. **Pattern conformance**: Both additions follow the exact pattern established by `m0001_initial` -- same `mod` declaration style, same `Box::new(<module>::Migration)` registration pattern.
