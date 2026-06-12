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
if [[ ! "${JIRA_ISSUE_ID}" =~ ^[A-Z]+-[0-9]+$ ]]; then
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
PR_URL=$(echo "${ISSUE_JSON}" | python3 -c "
import json, sys
issue = json.load(sys.stdin)
field = issue.get('fields', {}).get('customfield_10875')
if not field:
    print('')
    sys.exit(0)
if isinstance(field, str):
    print(field)
elif isinstance(field, dict):
    # ADF format — extract URL from inlineCard
    for block in field.get('content', []):
        for inline in block.get('content', []):
            if inline.get('type') == 'inlineCard':
                print(inline.get('attrs', {}).get('url', ''))
                sys.exit(0)
    print('')
" 2>/dev/null || echo "")

if [[ -n "${PR_URL}" ]]; then
  echo "PR linked: ${PR_URL}"
else
  echo "WARNING: No PR linked in Jira custom field — the skill will ask for the PR URL"
fi

# 5. Write pre-fetched data for sandbox consumption (tracker-agnostic format)
PRE_OUTPUT_DIR="/tmp/fullsend-pre-output"
mkdir -p "${PRE_OUTPUT_DIR}"

python3 -c "
import json, sys

issue = json.loads(sys.argv[1])
fields = issue.get('fields', {})

output = {
    'task_id': sys.argv[2],
    'task': {
        'summary': fields.get('summary', ''),
        'description': fields.get('description', {}),
        'status': (fields.get('status') or {}).get('name', ''),
        'labels': fields.get('labels', []),
        'issue_links': [
            {
                'type': (link.get('type') or {}).get('name', ''),
                'direction': 'inward' if 'inwardIssue' in link else 'outward',
                'key': (link.get('inwardIssue') or link.get('outwardIssue') or {}).get('key', '')
            }
            for link in fields.get('issuelinks', [])
        ],
        'custom_fields': {
            k: v for k, v in fields.items()
            if k.startswith('customfield_')
        }
    },
    'pr_url': sys.argv[3],
    'source': {
        'tracker': 'jira',
        'raw': issue
    }
}
json.dump(output, sys.stdout, indent=2)
" "${ISSUE_JSON}" "${JIRA_ISSUE_ID}" "${PR_URL}" > "${PRE_OUTPUT_DIR}/verify-pr-input.json"

echo "Pre-fetched data written to ${PRE_OUTPUT_DIR}/verify-pr-input.json"
echo "Input validation passed"
