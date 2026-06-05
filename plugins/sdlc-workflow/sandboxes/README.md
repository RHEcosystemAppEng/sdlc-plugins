# OpenShell Sandboxes for sdlc-workflow

Pre-built sandbox images for running sdlc-workflow skills inside [OpenShell](https://github.com/NVIDIA/OpenShell) with least-privilege network and filesystem policies.

## Quick Start

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/sdlc-workflow:latest
```

## Available Sandboxes

| Sandbox | Image | Jira | GitHub | Figma | Filesystem |
|---|---|---|---|---|---|
| [sdlc-workflow](sdlc-workflow/) | `ghcr.io/mrizzi/sdlc-plugins/sdlc-workflow` | full | full | read-only | read-write |
| [plan-feature](plan-feature/) | `ghcr.io/mrizzi/sdlc-plugins/plan-feature` | full | — | read-only | read-only |
| [implement-task](implement-task/) | `ghcr.io/mrizzi/sdlc-plugins/implement-task` | full | full | — | read-write |
| [verify-pr](verify-pr/) | `ghcr.io/mrizzi/sdlc-plugins/verify-pr` | full | read-only | — | read-only |
| [define-feature](define-feature/) | `ghcr.io/mrizzi/sdlc-plugins/define-feature` | full | — | — | read-only |
| [setup](setup/) | `ghcr.io/mrizzi/sdlc-plugins/setup` | read-only | — | — | read-write |

All sandboxes include LLM API access (Anthropic, Google Vertex AI, Amazon Bedrock).

## Custom Registry Shorthand

```bash
export OPENSHELL_COMMUNITY_REGISTRY=ghcr.io/mrizzi/sdlc-plugins
openshell sandbox create --from implement-task
```

## Extending the Base Image

Add project-specific build tools by extending the base image:

```dockerfile
FROM ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest
RUN dnf install -y rust cargo && dnf clean all
```

```bash
openshell sandbox create --from ./my-custom-sandbox/
```

## Building Locally

```bash
podman build -f plugins/sdlc-workflow/sandboxes/base/Dockerfile -t sdlc-base .
podman build -t implement-task plugins/sdlc-workflow/sandboxes/implement-task/
```

## Overriding Policies

```bash
openshell sandbox create \
  --from ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest \
  --policy plugins/sdlc-workflow/sandboxes/implement-task/policy.yaml
```
