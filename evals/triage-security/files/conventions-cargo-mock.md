<!-- SYNTHETIC TEST DATA — this project declares Cargo commands; they are fixture policy, not SDLC defaults. -->

# CONVENTIONS.md

## Dependency Updates

```json
{
  "policies": [
    {
      "ecosystem": "Cargo",
      "strategy": "batch",
      "update_command": "cargo update",
      "targeted_fallback_command": "cargo update -p {package} --precise {fixed_version}",
      "graph_command": "cargo tree --workspace --target all --all-features --invert {package} --locked",
      "constraint_changes": true,
      "verification": ["cargo test --workspace"]
    }
  ]
}
```
