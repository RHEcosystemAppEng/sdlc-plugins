# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner discovers and executes it.

## Sibling Reference

The existing registration of `m0001_initial` in this file serves as the pattern for how to add the new migration.

## Detailed Changes

### Change 1: Add module declaration

Add a new `mod` statement for the migration module. Place it after the existing `m0001_initial` module declaration, maintaining numerical ordering:

```rust
// Existing:
mod m0001_initial;

// Add:
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function. Place it after `m0001_initial`, maintaining execution order (migrations run in the order they appear in the vector):

```rust
// Existing pattern:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        // Add the following line:
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Conventions Applied

- Follows the exact registration pattern used by `m0001_initial` (wrapping in `Box::new()`)
- Maintains sequential ordering in the migration list (m0001 before m0002)
- Module declaration placed in numerical order alongside existing migration module declarations
- No other changes to `lib.rs` -- the modification is scoped to registration only

## Verification

- The migration runner will pick up `m0002_drop_advisory_status` when `migrations()` is called
- The ordering ensures `m0001_initial` (which created the `advisory` table with the `status` column) runs before `m0002_drop_advisory_status` (which drops the column)
- This ordering is critical for correctness: dropping a column that does not yet exist would fail
