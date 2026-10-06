# File 2: MODIFY `migration/src/lib.rs`

## Action: Modify existing file

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it runs as part of the migration sequence.

## Detailed Changes

### Pre-implementation inspection

Use `mcp__serena_backend__get_symbols_overview` on `migration/src/lib.rs` to understand its current structure, then `mcp__serena_backend__find_symbol` to read the `migrations()` function and the module declarations.

### Change 1: Add module declaration

Add a new `mod` declaration for the migration module, alongside the existing one for `m0001_initial`.

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

Add the new migration to the `vec![]` returned by the `migrations()` function, following the pattern of how `m0001_initial` is registered.

**Before (approximate):**
```rust
fn migrations(&self) -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

**After:**
```rust
fn migrations(&self) -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

### Conventions followed

- Module declaration order matches chronological migration order (m0001 before m0002)
- Registration in the `vec![]` follows the same `Box::new(<module>::Migration)` pattern
- New migration is appended at the end of the vec (migrations run in order)
- No other changes to the file

### Verification

After modification, verify:
1. `cargo check -p migration` (or the correct crate name) compiles successfully
2. The migration module is correctly referenced and the Migration struct is accessible
