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
# Iterate iteration directories in ascending numeric order so the
# highest-numbered iteration that has a result file wins. Plain glob order is
# lexicographic (iteration-9 sorts after iteration-20), which would select a
# stale iteration once there are >= 10 iterations. `sort -V` orders the
# embedded iteration numbers numerically; the `[[ -d ]]` guard skips the
# literal glob pattern when no iteration directory exists.
while IFS= read -r dir; do
  [[ -d "${dir}" ]] || continue
  # Prefer agent-result.json; fall back to result.json when it is absent,
  # matching the precedence in validate-output-schema.sh (agents sometimes
  # write "result.json" instead of "agent-result.json").
  if [[ -f "${dir}/agent-result.json" ]]; then
    RESULT_FILE="${dir}/agent-result.json"
  elif [[ -f "${dir}/result.json" ]]; then
    RESULT_FILE="${dir}/result.json"
  fi
done < <(printf '%s\n' iteration-*/output | sort -V)

if [[ -z "${RESULT_FILE}" ]]; then
  echo "ERROR: no agent-result.json or result.json found in any iteration output directory"
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
