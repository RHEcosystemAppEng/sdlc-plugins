# define-feature Sandbox

Sandbox for the define-feature skill. Interactively defines Jira features by walking through description template sections. Read-only filesystem, Jira-only network access.

## Allowed Endpoints

| Endpoint | Access |
|---|---|
| LLM API (Anthropic, Vertex AI, Bedrock) | full |
| Jira (`*.atlassian.net`) | full |
| Filesystem workspace | read-only |

## Usage

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/define-feature:latest
```

## Extending

```dockerfile
FROM ghcr.io/mrizzi/sdlc-plugins/define-feature:latest
# Add tools if needed
```

## Custom Policy

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest \
  --policy plugins/sdlc-workflow/sandboxes/define-feature/policy.yaml
```
