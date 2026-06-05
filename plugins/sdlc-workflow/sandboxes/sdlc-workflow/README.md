# sdlc-workflow Sandbox (General Purpose)

Combined sandbox for running any sdlc-workflow skill. Use this when invoking multiple skills in a single session.

## Allowed Endpoints

| Endpoint | Access |
|---|---|
| LLM API (Anthropic, Vertex AI, Bedrock) | full |
| Jira (`*.atlassian.net`) | full |
| GitHub API (`api.github.com`) | full |
| GitHub (`github.com`, SSH) | full |
| Figma (`api.figma.com`, `*.figma.com`) | read-only |
| npm registry (`registry.npmjs.org`) | read-only |
| crates.io | read-only |
| PyPI (`pypi.org`) | read-only |
| Filesystem workspace | read-write |

## Usage

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/sdlc-workflow:latest
```

## Extending

```dockerfile
FROM ghcr.io/mrizzi/sdlc-plugins/sdlc-workflow:latest
RUN dnf install -y rust cargo && dnf clean all
```

## Custom Policy

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest \
  --policy path/to/custom-policy.yaml
```
