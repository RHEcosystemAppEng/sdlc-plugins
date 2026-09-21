#!/usr/bin/env bash
# pre-triage-security.sh — collect one poller-dispatched security issue's
# credentialed evidence before Fullsend creates the token-free sandbox.

set -euo pipefail

# The Fullsend poller dispatches one Jira work item per run. The pre-script does
# not discover issues: it validates this URL, derives its Jira key, and gathers
# the complete evidence bundle for that one issue.
: "${FULLSEND_WORK_ITEM_URL:?FULLSEND_WORK_ITEM_URL (Jira work-item URL) is required}"
: "${JIRA_SERVER_URL:?JIRA_SERVER_URL is required}"
: "${JIRA_EMAIL:?JIRA_EMAIL is required}"
: "${JIRA_API_TOKEN:?JIRA_API_TOKEN is required}"

if [[ ! "${FULLSEND_WORK_ITEM_URL}" =~ ^https?://[^/]+/browse/([A-Z][A-Z0-9]+-[0-9]+)/?$ ]]; then
  echo "ERROR: FULLSEND_WORK_ITEM_URL must be a Jira issue URL" >&2
  exit 1
fi
ISSUE_KEY="${BASH_REMATCH[1]}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${FULLSEND_PROJECT_ROOT:-$(pwd)}"
if [[ ! -f "${PROJECT_ROOT}/CLAUDE.md" ]]; then
  echo "ERROR: target project CLAUDE.md is required at ${PROJECT_ROOT}/CLAUDE.md" >&2
  exit 1
fi

PRE_OUTPUT_DIR="${PRE_DIR:-/tmp/fullsend-triage-security}"
mkdir -p "${PRE_OUTPUT_DIR}"
OUTPUT_FILE="${PRE_OUTPUT_DIR}/triage-security-input.json"
TEMP_FILE="${OUTPUT_FILE}.tmp"

python3 "${SCRIPT_DIR}/pre_triage_security.py" collect "${ISSUE_KEY}" "${PROJECT_ROOT}" > "${TEMP_FILE}"
mv "${TEMP_FILE}" "${OUTPUT_FILE}"

echo "Pre-fetched triage-security evidence for ${ISSUE_KEY} to ${OUTPUT_FILE}"
