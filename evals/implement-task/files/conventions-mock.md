<!-- SYNTHETIC TEST DATA — mock CONVENTIONS.md for implement-task eval testing -->

# Coding Conventions

## Language and Framework

- Rust (edition and MSRV are defined in the workspace `Cargo.toml`)
- Web framework: Axum
- ORM: SeaORM with `DeriveEntityModel`
- Database: PostgreSQL

## Code Style

- Follow `rustfmt` defaults — run `cargo fmt --check` before committing
- Clippy is enforced with strict flags (see the exact invocation in Pre-commit checks)
- `unwrap()` and `expect()` are forbidden in production code; they are allowed in tests

## Pre-commit checks

Before committing any changes, run:

```sh
cargo xtask precommit
```

This command performs the following steps in order:

1. **Runs clippy** (`cargo clippy --all-targets --all-features -- -D warnings`)
2. **Runs `cargo fmt`** — applies standard Rust formatting
3. **Runs `cargo check`** (`--all-targets --all-features`) — verifies the project compiles cleanly

Any files modified by these steps must be included in the commit.

## Testing Conventions

- Integration tests use `#[test_context(TrustifyContext)]` from the `trustify_test_context` crate
- Test functions are `async fn` annotated with `#[test(actix_web::test)]`
- Tests return `anyhow::Result<()>` for ergonomic error handling
