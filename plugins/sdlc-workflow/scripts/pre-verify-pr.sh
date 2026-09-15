#!/usr/bin/env bash
# pre-verify-pr.sh — Derive + gate the Jira task from the triggering PR, then
# pre-fetch Jira + GitHub data.
#
# Runs on the fullsend runner BEFORE the sandbox is created, where the Jira
# and GitHub tokens live. The sandbox never sees a token — it reads only the
# JSON this script produces.
#
# The triggering PR URL is the SOLE entry point — the Jira key is derived, not
# supplied. fullsend's harness-run exports the PR URL as FULLSEND_WORK_ITEM_URL
# on the runner (a local run must export the same var). The Jira key is resolved
# by a JQL search on the Git Pull Request custom field (customfield_10875) and
# then re-verified to be in status Review AND carry the ai-generated-jira label,
# so a stale or unqualified PR is never reviewed.
#
# 1. Validates required env vars and the PR URL shape
# 2. Resolves + gates the Jira key by JQL on customfield_10875 == PR URL
# 3. If the gate fails (no/ambiguous match, status != Review, label absent):
#    emits an ADR-0072 skip signal and exits 0 (nothing to verify)
# 4. Fetches the full Jira issue and prefetches the GitHub tier-1 read bundle
#    (diff, stat, reviews, comments, commits, head ref + commit SHA) so the
#    sandbox needs no api.github.com egress
# 5. Writes the tracker-agnostic verify-pr-input.json that host_files mounts
#    into the sandbox
#
# Required env vars:
#   FULLSEND_WORK_ITEM_URL — the triggering PR URL (harness-run / local export)
#   JIRA_SERVER_URL        — Jira instance URL
#   JIRA_EMAIL             — Jira user email
#   JIRA_API_TOKEN         — Jira API token
#   GH_TOKEN               — GitHub token (PR prefetch)
#
# Optional env vars:
#   PRE_DIR                   — output directory (default: /tmp/fullsend-pre-output).
#                               The harness host_files src is the default path.
#   FULLSEND_PRESCRIPT_OUTPUT — key=value skip-signal file created by fullsend run
#                               (pre-script output protocol v1). Guarded — older
#                               CLIs leave it unset.

set -euo pipefail

# 1. Validate required env vars are set
: "${FULLSEND_WORK_ITEM_URL:?FULLSEND_WORK_ITEM_URL (triggering PR URL) is required}"
: "${JIRA_SERVER_URL:?JIRA_SERVER_URL is required}"
: "${JIRA_EMAIL:?JIRA_EMAIL is required}"
: "${JIRA_API_TOKEN:?JIRA_API_TOKEN is required}"

PR_URL="${FULLSEND_WORK_ITEM_URL}"

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

# 2. Parse owner/repo/number from the PR URL. End-anchor the pattern (allowing
#    only an optional trailing slash) so a malformed value like `.../pull/42abc`
#    or `.../pull/42/extra` is rejected outright instead of silently truncating
#    the pull number to 42 and prefetching the wrong PR.
if [[ ! "${PR_URL}" =~ ^https://github\.com/([^/]+/[^/]+)/pull/([0-9]+)/?$ ]]; then
  echo "ERROR: PR URL '${PR_URL}' is not a github.com pull request URL"
  exit 1
fi
PR_REPO="${BASH_REMATCH[1]}"
PR_NUM="${BASH_REMATCH[2]}"
echo "PR: ${PR_REPO}#${PR_NUM} (${PR_URL})"

# 3. Resolve + gate the Jira key by JQL on the Git Pull Request custom field.
#    The JQL `~` recall is broad; resolve-gated-issue re-confirms the exact PR
#    URL and enforces status=Review + the ai-generated-jira label in Python.
#    `--all` follows nextPageToken across every page so an exact match beyond the
#    first 50 recall results is never dropped (which would emit a false ADR-0072
#    skip); the Python exact-match verification remains the source of truth.
PR_JQL=$(python3 "${SCRIPT_DIR}/pre_verify_pr.py" build-pr-jql "${PR_URL}")
SEARCH_JSON=$(python3 "${SCRIPT_DIR}/jira-client.py" search_jql \
  --jql "${PR_JQL}" --fields "status,labels,customfield_10875" --all \
  2>"/tmp/fullsend-pre-jira-stderr.txt") || {
  JIRA_STDERR=$(cat /tmp/fullsend-pre-jira-stderr.txt 2>/dev/null || echo "")
  if echo "${JIRA_STDERR}" | grep -qi "401\|unauthorized"; then
    echo "ERROR: Jira authentication failed — check JIRA_EMAIL and JIRA_API_TOKEN"
  elif echo "${JIRA_STDERR}" | grep -qi "403\|forbidden"; then
    echo "ERROR: Jira permission denied — check that the API token can search issues"
  else
    echo "ERROR: Failed to search Jira for PR ${PR_URL}"
    echo "${JIRA_STDERR}"
  fi
  rm -f /tmp/fullsend-pre-jira-stderr.txt
  exit 1
}
rm -f /tmp/fullsend-pre-jira-stderr.txt

# resolve-gated-issue exits 3 when a gate fails (→ ADR-0072 skip), 0 with the
# resolved key on success, and 1 on an unexpected error. Capture without letting
# set -e abort on the non-zero gate/skip exit.
set +e
GATE_OUT=$(printf '%s\n' "${SEARCH_JSON}" | python3 "${SCRIPT_DIR}/pre_verify_pr.py" resolve-gated-issue "${PR_URL}")
GATE_RC=$?
set -e
if [[ ${GATE_RC} -eq 3 ]]; then
  request_skip "${GATE_OUT}"
elif [[ ${GATE_RC} -ne 0 ]]; then
  echo "ERROR: failed to resolve the Jira issue for PR ${PR_URL}"
  echo "${GATE_OUT}"
  exit 1
fi
JIRA_ISSUE_ID="${GATE_OUT}"
echo "Jira issue resolved + gated: ${JIRA_ISSUE_ID} (status=Review, label=ai-generated-jira)"

# 4. Fetch full issue details (pre-fetches the task context for the sandbox)
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

# 5. GitHub tier-1 prefetch — runs on the trusted runner where GH_TOKEN lives.
#    Every read the verify-pr skill performs against the PR is captured here so
#    the sandbox needs no api.github.com egress.
: "${GH_TOKEN:?GH_TOKEN is required to prefetch PR ${PR_REPO}#${PR_NUM}}"

HEAD_REF=$(gh pr view "${PR_NUM}" -R "${PR_REPO}" --json headRefName --jq .headRefName)
# Derive the head SHA from the ref tip OID, not from `.commits[-1].oid`: gh's
# `pr view` commits connection is bounded, so on a PR with more commits than the
# cap `.commits[-1]` is the last commit of a truncated page rather than the head
# — a silently-wrong SHA that still satisfies the result schema's hex pattern.
COMMIT_SHA=$(gh pr view "${PR_NUM}" -R "${PR_REPO}" --json headRefOid --jq .headRefOid)

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
# The bundled commits list uses gh's bounded `pr view` commits connection, so it
# may be truncated on a very large PR. The authoritative head SHA is taken from
# headRefOid above; this list is best-effort context for commit-traceability. If
# a consumer ever treats it as authoritative, switch to a paginated
# `gh api --paginate .../pulls/${PR_NUM}/commits` (which returns a different,
# `sha`-shaped object needing reshaping to match the `oid` contract).
gh pr view "${PR_NUM}" -R "${PR_REPO}" --json commits --jq .commits > "${PRE_OUTPUT_DIR}/commits.json"

echo "GitHub read bundle prefetched to ${PRE_OUTPUT_DIR}"

# 6. Idempotency prefetch — the sandbox has no Jira token, but Steps 6d/6f/7c
#     dedupe against the task's existing sub-tasks and linked (e.g., root-cause)
#     issues. Fetch each related issue here on the trusted runner (summary,
#     labels, description, issuetype, and comments) so the sandbox can run those
#     checks tokenlessly. No `|| true`: a related issue the token created should
#     be readable, so a fetch failure is a real error surfaced under set -e.
REL_DIR="${PRE_OUTPUT_DIR}/related-issues"
rm -rf "${REL_DIR}"
mkdir -p "${REL_DIR}"
RELATED_KEYS=$(printf '%s\n' "${ISSUE_JSON}" | python3 "${SCRIPT_DIR}/pre_verify_pr.py" related-keys)
for key in ${RELATED_KEYS}; do
  python3 "${SCRIPT_DIR}/jira-client.py" get_issue "${key}" \
    --fields "summary,labels,description,issuetype,comment" \
    > "${REL_DIR}/${key}.json"
done
echo "Idempotency read bundle prefetched to ${REL_DIR}"

# 7. Write pre-fetched data for sandbox consumption (tracker-agnostic format,
#    with the GitHub bundle embedded under `github` and the idempotency
#    related-issue metadata under `idempotency`).
printf '%s\n' "${ISSUE_JSON}" | python3 "${SCRIPT_DIR}/pre_verify_pr.py" transform \
  "${JIRA_ISSUE_ID}" "${PR_URL}" \
  --github-dir "${PRE_OUTPUT_DIR}" \
  --pr-repo "${PR_REPO}" \
  --pr-number "${PR_NUM}" \
  --head-ref "${HEAD_REF}" \
  --commit-sha "${COMMIT_SHA}" \
  --idempotency-dir "${REL_DIR}" > "${PRE_OUTPUT_DIR}/verify-pr-input.json"

echo "Pre-fetched data written to ${PRE_OUTPUT_DIR}/verify-pr-input.json"
echo "Input validation passed"
