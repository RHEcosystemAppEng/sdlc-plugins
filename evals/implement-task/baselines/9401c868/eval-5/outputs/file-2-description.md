# File 2: Modify `migration/src/lib.rs`

## Action: MODIFY

## Purpose

Register the new `m0002_drop_advisory_status` migration module so the migration runner discovers and executes it.

## Changes

### Change 1: Add module declaration

**Location**: Near the top of the file, after the existing `mod m0001_initial;` declaration.

**Add**:
```rust
mod m0002_drop_advisory_status;
```

This declares the new migration module so it can be referenced in the migrations list.

### Change 2: Register migration in the migrations() function

**Location**: Inside the `migrations()` function, in the `vec![]` that lists all migrations.

**Before**:
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

**After**:
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

The new migration is appended after `m0001_initial` to maintain sequential execution order. Migration order is critical -- the initial migration must create the table before this migration can drop a column from it.

## Design Decisions

1. **Append to end of vec**: Migrations execute in the order they appear in the vec. The new migration must come after m0001_initial since it depends on the `advisory` table already existing.

2. **Module naming**: Uses `m0002_drop_advisory_status` matching the directory name, following the established `m<NNNN>_<description>` convention from m0001_initial.

3. **No other changes to lib.rs**: Only the module declaration and vec entry are added. No changes to imports, the Migrator struct, or any other code in the file.
