# implement-task Sandbox

Sandbox for the implement-task skill. Implements Jira tasks by modifying code, running tests, and creating PRs. Read-write filesystem and full GitHub access.

## Allowed Endpoints

| Endpoint | Access |
|---|---|
| LLM API (Anthropic, Vertex AI, Bedrock) | full |
| Jira (`*.atlassian.net`) | full |
| GitHub API (`api.github.com`) | full |
| GitHub (`github.com`, SSH) | full |
| npm registry (`registry.npmjs.org`) | read-only |
| crates.io | read-only |
| PyPI (`pypi.org`) | read-only |
| Filesystem workspace | read-write |

## Usage

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/implement-task:latest
```

## Extending

```dockerfile
FROM ghcr.io/mrizzi/sdlc-plugins/implement-task:latest
RUN dnf install -y rust cargo && dnf clean all
```

## Custom Policy

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest \
  --policy plugins/sdlc-workflow/sandboxes/implement-task/policy.yaml
```
