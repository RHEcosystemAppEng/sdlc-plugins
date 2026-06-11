# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner discovers and executes it.

## Changes

### 1. Add module declaration

Add a new module declaration for the migration, following the existing pattern of `m0001_initial`:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // NEW
```

### 2. Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function. The new entry follows the same `Box::new(...)` pattern used for `m0001_initial`:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // NEW
    ]
}
```

## Conventions followed

- Module naming follows the `m<NNNN>_<description>` pattern established by `m0001_initial`
- Registration uses `Box::new(<module>::Migration)` pattern consistent with existing entries
- Migration ordering is sequential -- `m0002` comes after `m0001` in the vec

## Verification

- After modification, confirm that `cargo check` succeeds (the new module must exist for compilation)
- The migration runner will execute migrations in the order listed in the vec
