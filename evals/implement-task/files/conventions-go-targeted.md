<!-- SYNTHETIC TEST DATA — Go commands are target-project policy, not plugin defaults. -->

# CONVENTIONS.md

## Dependency Updates

```json
{
  "policies": [
    {
      "ecosystem": "*",
      "strategy": "batch",
      "update_command": "./scripts/update-all-dependencies",
      "targeted_fallback_command": "./scripts/update-dependency {package} {fixed_version}",
      "graph_command": "./scripts/dependency-paths {package}",
      "constraint_changes": true,
      "verification": ["./scripts/test-all"]
    },
    {
      "ecosystem": "Go modules",
      "strategy": "targeted",
      "update_command": "go get {package}@{fixed_version}",
      "targeted_fallback_command": "",
      "graph_command": "go mod graph",
      "constraint_changes": false,
      "verification": ["go test ./..."]
    }
  ]
}
```
