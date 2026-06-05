# setup Sandbox

Sandbox for the setup skill. Configures CLAUDE.md Project Configuration for use with sdlc-workflow skills. Read-write filesystem for CLAUDE.md modifications, read-only Jira for configuration verification.

## Allowed Endpoints

| Endpoint | Access |
|---|---|
| LLM API (Anthropic, Vertex AI, Bedrock) | full |
| Jira (`*.atlassian.net`) | read-only |
| Filesystem workspace | read-write |

## Usage

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/setup:latest
```

## Extending

```dockerfile
FROM ghcr.io/mrizzi/sdlc-plugins/setup:latest
# Add tools if needed
```

## Custom Policy

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest \
  --policy plugins/sdlc-workflow/sandboxes/setup/policy.yaml
```
