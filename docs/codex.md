# Codex support

The `sdlc-workflow` plugin supports Codex in addition to Claude Code. The
Claude Code manifest and marketplace remain unchanged; Codex uses the
compatibility manifest at `plugins/sdlc-workflow/.codex-plugin/plugin.json`.

## Install from Codex CLI

From any trusted project, run:

```bash
codex plugin marketplace add RHEcosystemAppEng/sdlc-plugins --ref main
codex plugin add sdlc-workflow@sdlc-plugins
```

Verify the installation with:

```bash
codex plugin list
```

Start a new Codex conversation after installation so the skills are loaded.

## Project configuration

The `setup` skill accepts either project configuration file:

- `AGENTS.md` is preferred when running in Codex.
- `CLAUDE.md` remains supported for Claude Code and existing projects.

The file must contain the `# Project Configuration` sections described in
[`project-config-contract.md`](project-config-contract.md). The configuration
format is shared between both clients, so teams can keep one file when both
clients are used.

Run the setup skill after installing the plugin and choose the configuration
file appropriate for the client:

```text
$setup
```

The Jira, Serena, and other MCP integrations are supplied by the host. The
plugin does not bundle credentials or replace those MCP server configurations.

## Current compatibility boundary

The skills are shared instruction files and retain Claude-compatible variables
such as `${CLAUDE_PLUGIN_ROOT}`. Codex provides this compatibility variable for
installed plugins. Fullsend-specific scripts and Claude Code marketplace
commands remain supported for Claude users and are not required for ordinary
Codex skill execution.
