#!/bin/bash
# bootstrap-plugin-cache.sh — Generate Claude Code marketplace cache
# from a plugin directory so it's auto-discovered via CLAUDE_CONFIG_DIR.
#
# Usage: bootstrap-plugin-cache.sh <plugin-dir> <config-dir>
#   plugin-dir: path to the plugin (e.g. /tmp/claude-config/plugins/sdlc-workflow)
#   config-dir: CLAUDE_CONFIG_DIR root (e.g. /tmp/claude-config)

set -euo pipefail

PLUGIN_DIR="${1:?Usage: $0 <plugin-dir> <config-dir>}"
CONFIG_DIR="${2:?Usage: $0 <plugin-dir> <config-dir>}"

PLUGIN_NAME=$(basename "$PLUGIN_DIR")
MARKETPLACE="claude-plugins-official"
VERSION="1.0.0"
PLUGINS_BASE="${CONFIG_DIR}/plugins"
MKT_BASE="${PLUGINS_BASE}/marketplaces/${MARKETPLACE}"
CACHE_DIR="${PLUGINS_BASE}/cache/${MARKETPLACE}/${PLUGIN_NAME}/${VERSION}"
TIMESTAMP="2026-01-01T00:00:00.000Z"
QUALIFIED="${PLUGIN_NAME}@${MARKETPLACE}"

mkdir -p \
  "${MKT_BASE}/.claude-plugin" \
  "${MKT_BASE}/plugins/${PLUGIN_NAME}" \
  "${CACHE_DIR}"

echo "# ${PLUGIN_NAME}" > "${CACHE_DIR}/README.md"
echo "# ${PLUGIN_NAME}" > "${MKT_BASE}/plugins/${PLUGIN_NAME}/README.md"

cat > "${MKT_BASE}/.claude-plugin/marketplace.json" << MKEOF
{
  "\$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "${MARKETPLACE}",
  "owner": {"name": "Anthropic", "email": "support@anthropic.com"},
  "plugins": [{"name": "${PLUGIN_NAME}", "version": "${VERSION}", "source": "./plugins/${PLUGIN_NAME}", "category": "development"}]
}
MKEOF

cat > "${PLUGINS_BASE}/known_marketplaces.json" << KMEOF
{
  "${MARKETPLACE}": {
    "source": {"source": "github", "repo": "anthropics/claude-plugins-official"},
    "installLocation": "${MKT_BASE}",
    "lastUpdated": "${TIMESTAMP}"
  }
}
KMEOF

cat > "${PLUGINS_BASE}/installed_plugins.json" << IPEOF
{
  "version": 2,
  "plugins": {
    "${QUALIFIED}": [{"scope": "user", "installPath": "${CACHE_DIR}", "version": "${VERSION}", "installedAt": "${TIMESTAMP}", "lastUpdated": "${TIMESTAMP}"}]
  }
}
IPEOF

cat > "${CONFIG_DIR}/settings.json" << SEOF
{
  "enabledPlugins": {"${QUALIFIED}": true}
}
SEOF

echo "Plugin '${PLUGIN_NAME}' registered in marketplace cache at ${CONFIG_DIR}"
