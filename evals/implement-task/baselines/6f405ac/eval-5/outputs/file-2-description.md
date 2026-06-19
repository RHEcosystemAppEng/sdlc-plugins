# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration registry so it is executed by the migration runner.

## Detailed Changes

### 1. Add module declaration

Add a new `mod` statement for the migration module, following the existing pattern:

```rust
// Existing:
mod m0001_initial;

// Add:
mod m0002_drop_advisory_status;
```

### 2. Register in migrations() function

Add the new migration to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`:

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

### Key Implementation Details

1. **Module declaration:** The `mod m0002_drop_advisory_status;` line is added alongside the existing `mod m0001_initial;` declaration
2. **Registration order:** The new migration is added AFTER `m0001_initial` in the `vec![]` to maintain sequential execution order -- migrations must run in the order they are listed
3. **Pattern conformance:** Uses the exact same `Box::new(module::Migration)` pattern as the existing `m0001_initial` registration
4. **Minimal change:** Only two lines are added to this file -- the module declaration and the vec entry. No other modifications are needed.
