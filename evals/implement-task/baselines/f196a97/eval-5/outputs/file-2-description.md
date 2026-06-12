# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it is discovered and executed by the migration runner.

## Detailed Changes

### Change 1: Add module declaration

**Location**: Near the top of the file, after the existing `mod m0001_initial;` declaration.

**Add**:
```rust
mod m0002_drop_advisory_status;
```

**Before** (existing):
```rust
mod m0001_initial;
```

**After** (with addition):
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

**Location**: Inside the `migrations()` function, in the `vec![]` that lists all migration instances.

**Add**: A new entry after the existing `m0001_initial` entry, following the same `Box::new(...)` pattern.

**Before** (existing):
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

**After** (with addition):
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

### Design Decisions

1. **Module declaration placement**: Added immediately after `m0001_initial` to maintain alphabetical/sequential ordering of migration modules.

2. **Registration order**: Added at the end of the `vec![]` to ensure migrations run in chronological order (m0001 before m0002). SeaORM executes migrations in the order they appear in this vector.

3. **Pattern conformance**: Both the `mod` declaration and `Box::new(...)` registration exactly follow the pattern established by `m0001_initial`, as required by the Implementation Notes.
