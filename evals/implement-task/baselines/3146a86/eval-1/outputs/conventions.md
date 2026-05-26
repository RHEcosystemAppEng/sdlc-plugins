# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### 1. Error Handling: `Result<T, AppError>` with `.context()` Wrapping
All endpoint handlers in `modules/fundamental/src/advisory/endpoints/` return `Result<T, AppError>`. Service method errors are wrapped using `.context("descriptive message")` from anyhow. The `AppError` enum in `common/src/error.rs` implements `IntoResponse` for automatic HTTP error mapping.

### 2. Module Structure: `model/` + `service/` + `endpoints/` Pattern
Every domain module (sbom, advisory, package) follows the same three-subdirectory structure:
- `model/` — data structs (Summary, Details)
- `service/` — business logic methods
- `endpoints/` — HTTP handlers and route registration

### 3. Naming Conventions: `verb_noun` Service Methods
Service methods follow `verb_noun` naming: `fetch`, `list`, `search`, `ingest`. New methods should follow the same pattern (e.g., `severity_summary`).

### 4. Endpoint Handler Pattern
Handlers extract path parameters via `Path<Id>`, receive service via dependency injection, call a single service method, and return `Json<T>`. No business logic in handlers.

### 5. Route Registration Pattern
Each module's `endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` to register routes. The server's `main.rs` mounts all module routers — individual modules do not modify `main.rs`.

### 6. Service Method Signatures
All service methods take `&self`, a typed ID parameter, and `&Transactional<'_>` as the last parameter for database transaction access.

### 7. Model Struct Patterns
Model structs derive `Clone, Debug, Serialize, Deserialize, ToSchema`. Summary structs are lightweight (used in lists), Details structs are comprehensive (used in single-item fetches).

### 8. Module Registration
New submodules are registered via `pub mod <name>;` in the parent `mod.rs`, following alphabetical ordering.

### 9. Test Patterns
Integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization. Tests follow `test_<endpoint>_<scenario>` naming. All endpoint test suites include a 404 test case.
