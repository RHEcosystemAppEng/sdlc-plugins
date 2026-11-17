<!-- SYNTHETIC TEST DATA — DO NOT USE IN PRODUCTION -->

# Project Conventions

## General

- Language: Rust (edition 2021)
- Framework: actix-web 4.x with SeaORM 1.x
- Database: PostgreSQL 15

## Database Migrations

- Tool: SeaORM Migration
- Naming: `migration/src/m{YYYYMMDD}_{HHMMSS}_{name}.rs`
- Index naming: `idx_{table}_{columns}`
- FK index policy: All foreign keys must have indexes
- Rollback: Every `up()` must have a matching `down()`
- Concurrency: Use `IF NOT EXISTS` and `CONCURRENTLY` for production
- Transaction safety: Wrap multi-statement migrations in explicit transactions
- Testing: All migrations must pass `cargo test` in the migration crate

## Code Style

- Use `clippy` with default lints
- Format with `rustfmt`
- Error handling: Use `anyhow` for application errors, `thiserror` for library errors

## CI Checks

- `cargo fmt --check`
- `cargo clippy -- -D warnings`
- `cargo test`
- `cargo sqlx prepare --check` (for offline query verification)

## Performance Testing

- Backend benchmarks: `cargo bench`
- Load testing: `wrk -t4 -c100 -d30s`
