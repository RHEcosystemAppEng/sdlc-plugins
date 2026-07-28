# File 2: migration/src/lib.rs

**Action**: Modify existing file
**Purpose**: Register the new `m0002_drop_advisory_status` migration module in the migration list

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` statement for the new migration module, placed after the existing `m0001_initial` module declaration.

**Before:**
```rust
mod m0001_initial;
```

**After:**
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations list

Add the new migration to the `vec![]` returned by the `migrations()` function, after the existing `m0001_initial` entry. The ordering is significant — migrations execute in the order they appear in this list.

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

### Design Decisions

1. **Module ordering**: The `mod` declaration and the `vec![]` entry both follow the existing `m0001_initial` entry, maintaining chronological ordering of migrations. This is critical for correctness — the `m0002` migration must run after `m0001` because the `advisory` table (and its `status` column) is created by the initial migration.

2. **Pattern compliance**: The registration follows exactly the same pattern as `m0001_initial`: a `Box::new()` wrapping the module's `Migration` struct. This is the standard SeaORM migration registration pattern.

3. **No other changes**: Only the module declaration and the vec entry are modified. No imports, no structural changes, no other edits to `lib.rs`.
