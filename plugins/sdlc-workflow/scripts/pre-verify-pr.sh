#!/usr/bin/env bash
# pre-verify-pr.sh — Validate inputs and pre-fetch Jira + GitHub data.
#
# Runs on the fullsend runner BEFORE the sandbox is created, where the Jira
# and GitHub tokens live. The sandbox never sees a token — it reads only the
# JSON this script produces.
#
# 1. Validates required env vars and JIRA_ISSUE_ID format
# 2. Fetches the full Jira issue and extracts the linked PR URL
# 3. If no PR URL: emits an ADR-0072 skip signal and exits 0 (nothing to verify)
# 4. If a PR URL: prefetches the GitHub tier-1 read bundle (diff, stat,
#    reviews, comments, commits, head ref + commit SHA) so the sandbox needs
#    no api.github.com egress
# 5. Writes the tracker-agnostic verify-pr-input.json that host_files mounts
#    into the sandbox
#
# Required env vars:
#   JIRA_ISSUE_ID     — Jira issue key (e.g., TC-4741)
#   JIRA_SERVER_URL   — Jira instance URL
#   JIRA_EMAIL        — Jira user email
#   JIRA_API_TOKEN    — Jira API token
#   GH_TOKEN          — GitHub token (only needed once a PR URL is resolved)
#
# Optional env vars:
#   PRE_DIR                   — output directory (default: /tmp/fullsend-pre-output).
#                               The harness host_files src is the default path.
#   FULLSEND_PRESCRIPT_OUTPUT — key=value skip-signal file created by fullsend run
#                               (pre-script output protocol v1). Guarded — older
#                               CLIs leave it unset.

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
PRE_OUTPUT_DIR="${PRE_DIR:-/tmp/fullsend-pre-output}"
mkdir -p "${PRE_OUTPUT_DIR}"

# request_skip REASON — emit an ADR-0072 skip signal and exit cleanly.
# The pre-script output protocol (v1) is line-based key=value; the guard on
# FULLSEND_PRESCRIPT_OUTPUT matches the scaffold's GITHUB_OUTPUT guard, so a
# missing variable (older CLI) fails open to a normal run rather than erroring.
request_skip() {
  local reason="$1"
  echo "SKIP: ${reason}"
  if [[ -n "${FULLSEND_PRESCRIPT_OUTPUT:-}" ]]; then
    {
      echo "skipped=true"
      echo "reason=${reason}"
    } >> "${FULLSEND_PRESCRIPT_OUTPUT}"
  fi
  exit 0
}

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

# 5. No PR linked — nothing to verify. Signal a skip (ADR-0072) and stop before
#    the sandbox is created.
if [[ -z "${PR_URL}" ]]; then
  request_skip "no PR URL on the Jira issue"
fi

echo "PR linked: ${PR_URL}"

# 6. Parse owner/repo/number from the PR URL.
if [[ ! "${PR_URL}" =~ ^https://github\.com/([^/]+/[^/]+)/pull/([0-9]+) ]]; then
  echo "ERROR: PR URL '${PR_URL}' is not a github.com pull request URL"
  exit 1
fi
PR_REPO="${BASH_REMATCH[1]}"
PR_NUM="${BASH_REMATCH[2]}"
echo "PR: ${PR_REPO}#${PR_NUM}"

# 7. GitHub tier-1 prefetch — runs on the trusted runner where GH_TOKEN lives.
#    Every read the verify-pr skill performs against the PR is captured here so
#    the sandbox needs no api.github.com egress.
: "${GH_TOKEN:?GH_TOKEN is required to prefetch PR ${PR_REPO}#${PR_NUM}}"

HEAD_REF=$(gh pr view "${PR_NUM}" -R "${PR_REPO}" --json headRefName --jq .headRefName)
COMMIT_SHA=$(gh pr view "${PR_NUM}" -R "${PR_REPO}" --json commits --jq '.commits[-1].oid')

gh pr diff "${PR_NUM}" -R "${PR_REPO}"                  > "${PRE_OUTPUT_DIR}/pr.diff"
# `gh pr diff` has no --stat flag; derive the per-file diffstat from the patch we
# just fetched using a supported git command. Guard the empty-diff case: `git
# apply --stat` errors on an empty patch, which would abort under set -euo pipefail.
if [[ -s "${PRE_OUTPUT_DIR}/pr.diff" ]]; then
  git apply --stat "${PRE_OUTPUT_DIR}/pr.diff"         > "${PRE_OUTPUT_DIR}/pr.stat"
else
  : > "${PRE_OUTPUT_DIR}/pr.stat"
fi
# GitHub REST returns ~30 items per page; without --paginate the reviews and
# comments are silently truncated on any active PR. --slurp aggregates the
# per-page arrays into an array-of-pages, which `jq 'add'` concatenates back
# into the single flat array that pre_verify_pr.py's build_github_bundle
# expects. (--slurp cannot be combined with gh's built-in --jq, so the merge
# uses a standalone jq.) pipefail makes a failed gh or jq abort the script.
gh api --paginate --slurp "repos/${PR_REPO}/pulls/${PR_NUM}/reviews"  | jq 'add' > "${PRE_OUTPUT_DIR}/reviews.json"
gh api --paginate --slurp "repos/${PR_REPO}/pulls/${PR_NUM}/comments" | jq 'add' > "${PRE_OUTPUT_DIR}/review-comments.json"
gh api --paginate --slurp "repos/${PR_REPO}/issues/${PR_NUM}/comments" | jq 'add' > "${PRE_OUTPUT_DIR}/issue-comments.json"
gh pr view "${PR_NUM}" -R "${PR_REPO}" --json commits --jq .commits > "${PRE_OUTPUT_DIR}/commits.json"

echo "GitHub read bundle prefetched to ${PRE_OUTPUT_DIR}"

# 8. Write pre-fetched data for sandbox consumption (tracker-agnostic format,
#    with the GitHub bundle embedded under `github`).
printf '%s\n' "${ISSUE_JSON}" | python3 "${SCRIPT_DIR}/pre_verify_pr.py" transform \
  "${JIRA_ISSUE_ID}" "${PR_URL}" \
  --github-dir "${PRE_OUTPUT_DIR}" \
  --pr-repo "${PR_REPO}" \
  --pr-number "${PR_NUM}" \
  --head-ref "${HEAD_REF}" \
  --commit-sha "${COMMIT_SHA}" > "${PRE_OUTPUT_DIR}/verify-pr-input.json"

echo "Pre-fetched data written to ${PRE_OUTPUT_DIR}/verify-pr-input.json"
echo "Input validation passed"
