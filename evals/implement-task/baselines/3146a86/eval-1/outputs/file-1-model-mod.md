# File 1 — Modify: `modules/fundamental/src/advisory/model/mod.rs`

## Current State (inferred from sibling analysis)

```rust
pub mod summary;
pub mod details;
```

## Change Required

Add a `pub mod severity_summary;` declaration to register the new model sub-module.

## After Change

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

Declarations are kept in alphabetical order, following the pattern observed across other `mod.rs` files in the codebase.

## Why

Without this declaration, Rust's module system will not compile `severity_summary.rs` and the struct will be invisible to the rest of the crate.

## Inspection Steps

1. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` — confirm current module declarations.
2. Verify alphabetical ordering used by sibling `mod.rs` files in `sbom/model/mod.rs` and `package/model/mod.rs` via `mcp__serena_backend__get_symbols_overview`.
3. Use `mcp__serena_backend__insert_after_symbol` to add `pub mod severity_summary;` after the `pub mod details;` line, or use Edit tool if Serena is not available.
