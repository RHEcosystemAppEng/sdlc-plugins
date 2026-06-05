# verify-pr Sandbox

Sandbox for the verify-pr skill. Verifies PRs against Jira task acceptance criteria and creates sub-tasks for review feedback. Read-only filesystem, read-only GitHub access.

## Allowed Endpoints

| Endpoint | Access |
|---|---|
| LLM API (Anthropic, Vertex AI, Bedrock) | full |
| Jira (`*.atlassian.net`) | full |
| GitHub API (`api.github.com`) | read-only |
| Filesystem workspace | read-only |

## Usage

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/verify-pr:latest
```

## Extending

```dockerfile
FROM ghcr.io/mrizzi/sdlc-plugins/verify-pr:latest
# Add tools needed for code analysis
```

## Custom Policy

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest \
  --policy plugins/sdlc-workflow/sandboxes/verify-pr/policy.yaml
```
