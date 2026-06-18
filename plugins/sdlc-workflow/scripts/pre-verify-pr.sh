#!/usr/bin/env bash
# pre-verify-pr.sh — Validate inputs and pre-fetch Jira data.
#
# Runs on the fullsend runner BEFORE the sandbox is created.
# 1. Validates required env vars and JIRA_ISSUE_ID format
# 2. Verifies the Jira issue exists
# 3. Fetches the full issue and PR linkage, writes to a JSON file
#    that host_files mounts into the sandbox
#
# Required env vars:
#   JIRA_ISSUE_ID     — Jira issue key (e.g., TC-4741)
#   JIRA_SERVER_URL   — Jira instance URL
#   JIRA_EMAIL        — Jira user email
#   JIRA_API_TOKEN    — Jira API token

set -euo pipefail

# 1. Validate required env vars are set
: "${JIRA_ISSUE_ID:?JIRA_ISSUE_ID is required}"
: "${JIRA_SERVER_URL:?JIRA_SERVER_URL is required}"
: "${JIRA_EMAIL:?JIRA_EMAIL is required}"
: "${JIRA_API_TOKEN:?JIRA_API_TOKEN is required}"

# 2. Validate JIRA_ISSUE_ID format
# https://confluence.atlassian.com/adminjiraserver/changing-the-project-key-format-938847081.html
if [[ ! "${JIRA_ISSUE_ID}" =~ ^[A-Z][A-Z0-9_]+-[0-9]+$ ]]; then
  echo "ERROR: JIRA_ISSUE_ID '${JIRA_ISSUE_ID}' does not match expected format (e.g., TC-4741)"
  exit 1
fi

echo "Issue: ${JIRA_ISSUE_ID}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 3. Fetch full issue details (validates existence + pre-fetches for sandbox)
ISSUE_JSON=$(python3 "${SCRIPT_DIR}/jira-client.py" get_issue "${JIRA_ISSUE_ID}" --fields "*all" 2>"/tmp/fullsend-pre-jira-stderr.txt") || {
  JIRA_STDERR=$(cat /tmp/fullsend-pre-jira-stderr.txt 2>/dev/null || echo "")
  if echo "${JIRA_STDERR}" | grep -qi "401\|unauthorized"; then
    echo "ERROR: Jira authentication failed — check JIRA_EMAIL and JIRA_API_TOKEN"
  elif echo "${JIRA_STDERR}" | grep -qi "403\|forbidden"; then
    echo "ERROR: Jira permission denied — check that the API token has access to ${JIRA_ISSUE_ID}"
  elif echo "${JIRA_STDERR}" | grep -qi "404\|not found"; then
    echo "ERROR: Jira issue ${JIRA_ISSUE_ID} not found"
  else
    echo "ERROR: Failed to fetch Jira issue ${JIRA_ISSUE_ID}"
    echo "${JIRA_STDERR}"
  fi
  rm -f /tmp/fullsend-pre-jira-stderr.txt
  exit 1
}
rm -f /tmp/fullsend-pre-jira-stderr.txt

echo "Jira issue verified: ${JIRA_ISSUE_ID}"

# 4. Extract PR URL from custom field (best-effort)
PR_URL=$(printf '%s\n' "${ISSUE_JSON}" | python3 "${SCRIPT_DIR}/pre_verify_pr.py" extract-pr-url 2>/dev/null || echo "")

if [[ -n "${PR_URL}" ]]; then
  echo "PR linked: ${PR_URL}"
else
  echo "WARNING: No PR linked in Jira custom field — the skill will ask for the PR URL"
fi

# 5. Write pre-fetched data for sandbox consumption (tracker-agnostic format)
PRE_OUTPUT_DIR="/tmp/fullsend-pre-output"
mkdir -p "${PRE_OUTPUT_DIR}"

printf '%s\n' "${ISSUE_JSON}" | python3 "${SCRIPT_DIR}/pre_verify_pr.py" transform \
  "${JIRA_ISSUE_ID}" "${PR_URL}" > "${PRE_OUTPUT_DIR}/verify-pr-input.json"

echo "Pre-fetched data written to ${PRE_OUTPUT_DIR}/verify-pr-input.json"
echo "Input validation passed"
