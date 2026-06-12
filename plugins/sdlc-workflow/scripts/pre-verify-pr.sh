#!/usr/bin/env bash
# pre-verify-pr.sh — Validate inputs before sandbox creation.
#
# Runs on the fullsend runner BEFORE the sandbox is created.
# Fails fast on invalid inputs to avoid wasting sandbox compute time.
#
# Required env vars:
#   JIRA_ISSUE_ID     — Jira issue key (e.g., TC-4741)
#   JIRA_SERVER_URL   — Jira instance URL
#   JIRA_EMAIL        — Jira user email
#   JIRA_API_TOKEN    — Jira API token
#   GH_TOKEN          — GitHub token

set -euo pipefail

# 1. Validate required env vars are set
: "${JIRA_ISSUE_ID:?JIRA_ISSUE_ID is required}"
: "${JIRA_SERVER_URL:?JIRA_SERVER_URL is required}"
: "${JIRA_EMAIL:?JIRA_EMAIL is required}"
: "${JIRA_API_TOKEN:?JIRA_API_TOKEN is required}"
: "${GH_TOKEN:?GH_TOKEN is required}"

# 2. Validate JIRA_ISSUE_ID format
if [[ ! "${JIRA_ISSUE_ID}" =~ ^[A-Z]+-[0-9]+$ ]]; then
  echo "ERROR: JIRA_ISSUE_ID '${JIRA_ISSUE_ID}' does not match expected format (e.g., TC-4741)"
  exit 1
fi

echo "Issue: ${JIRA_ISSUE_ID}"

# 3. Verify the Jira issue exists
AUTH=$(echo -n "${JIRA_EMAIL}:${JIRA_API_TOKEN}" | base64)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Basic ${AUTH}" \
  -H "Accept: application/json" \
  "${JIRA_SERVER_URL}/rest/api/3/issue/${JIRA_ISSUE_ID}?fields=summary")

if [[ "${HTTP_CODE}" == "404" ]]; then
  echo "ERROR: Jira issue ${JIRA_ISSUE_ID} not found"
  exit 1
elif [[ "${HTTP_CODE}" != "200" ]]; then
  echo "ERROR: Jira API returned HTTP ${HTTP_CODE} for ${JIRA_ISSUE_ID}"
  exit 1
fi

echo "Jira issue verified: ${JIRA_ISSUE_ID}"

# 4. Check if the issue has a linked PR (best-effort — don't fail if field is missing)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PR_FIELD=$(python3 "${SCRIPT_DIR}/jira-client.py" get_issue "${JIRA_ISSUE_ID}" \
  --fields "customfield_10875" 2>/dev/null | \
  python3 -c "import json,sys; d=json.load(sys.stdin); f=d.get('fields',{}).get('customfield_10875',''); print(f if f else '')" 2>/dev/null || echo "")

if [[ -n "${PR_FIELD}" ]]; then
  echo "PR linked: ${PR_FIELD}"
else
  echo "WARNING: No PR linked in Jira custom field — the skill will ask for the PR URL"
fi

echo "Input validation passed"
