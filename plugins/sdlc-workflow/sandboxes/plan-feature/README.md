# plan-feature Sandbox

Sandbox for the plan-feature skill. Reads Jira features and Figma designs to generate implementation tasks. Read-only filesystem access.

## Allowed Endpoints

| Endpoint | Access |
|---|---|
| LLM API (Anthropic, Vertex AI, Bedrock) | full |
| Jira (`*.atlassian.net`) | full |
| Figma (`api.figma.com`, `*.figma.com`) | read-only |
| Filesystem workspace | read-only |

## Usage

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/plan-feature:latest
```

## Extending

```dockerfile
FROM ghcr.io/mrizzi/sdlc-plugins/plan-feature:latest
# Add tools needed for code analysis
```

## Custom Policy

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest \
  --policy plugins/sdlc-workflow/sandboxes/plan-feature/policy.yaml
```
