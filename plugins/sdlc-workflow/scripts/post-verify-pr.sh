#!/usr/bin/env bash
# post-verify-pr.sh — Execute verify-pr structured output actions.
#
# Runs on the fullsend runner AFTER the sandbox is destroyed.
# Working directory is the fullsend run output directory.
#
# Required env vars:
#   JIRA_SERVER_URL   — Jira instance URL
#   JIRA_EMAIL        — Jira user email
#   JIRA_API_TOKEN    — Jira API token
#   JIRA_PROJECT_KEY  — Jira project key (for root-cause task creation)
#   GH_TOKEN          — GitHub token
#
# The agent writes its output to output/agent-result.json (relative to
# the iteration directory). This script finds the most recent iteration's
# output and delegates to execute-actions.py.

set -euo pipefail

RESULT_FILE=""
for dir in iteration-*/output; do
  if [[ -f "${dir}/agent-result.json" ]]; then
    RESULT_FILE="${dir}/agent-result.json"
  fi
done

if [[ -z "${RESULT_FILE}" ]]; then
  echo "ERROR: agent-result.json not found in any iteration output directory"
  exit 1
fi

echo "Reading verify-pr result from: ${RESULT_FILE}"

if ! jq empty "${RESULT_FILE}" 2>/dev/null; then
  echo "ERROR: ${RESULT_FILE} is not valid JSON"
  exit 1
fi

OVERALL=$(jq -r '.report.overall' "${RESULT_FILE}")
ACTION_COUNT=$(jq '.actions | length' "${RESULT_FILE}")
echo "Overall: ${OVERALL}"
echo "Actions: ${ACTION_COUNT}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/execute-actions.py" "${RESULT_FILE}"
