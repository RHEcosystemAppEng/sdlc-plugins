# File 2: Modify `migration/src/lib.rs`

## Action: MODIFY

## Purpose

Register the new `m0002_drop_advisory_status` migration module so the migration runner discovers and executes it.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module, following the existing pattern for `m0001_initial`:

```rust
// Before (existing):
mod m0001_initial;

// After (added line):
mod m0001_initial;
mod m0002_drop_advisory_status;
```

The module declaration is added immediately after the existing `m0001_initial` declaration, maintaining alphabetical/numerical ordering.

### Change 2: Register migration in the `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the pattern used for `m0001_initial`:

```rust
// Before (existing):
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}

// After (added entry):
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

The new migration is appended after `m0001_initial` to maintain execution order. Migrations run sequentially in the order listed.

## Conventions Applied

- Module naming follows the `m<NNNN>_<snake_case_description>` pattern established by `m0001_initial`
- Registration follows the `Box::new(<module>::Migration)` pattern in the `migrations()` vec
- Ordering is sequential by migration number (m0001 before m0002)
- No other changes to this file -- keeping modifications minimal and in scope
