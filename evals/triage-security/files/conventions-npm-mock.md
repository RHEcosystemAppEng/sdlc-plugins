<!-- SYNTHETIC TEST DATA — npm commands are declared by this target project, not the plugin. -->

# CONVENTIONS.md

## Dependency Updates

```json
{
  "policies": [
    {
      "ecosystem": "npm",
      "strategy": "targeted",
      "update_command": "npm update {package}",
      "targeted_fallback_command": "",
      "graph_command": "npm ls {package} --all",
      "constraint_changes": false,
      "verification": ["npm test"]
    }
  ]
}
```
