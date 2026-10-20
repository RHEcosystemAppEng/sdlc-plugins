#!/usr/bin/env bash
# post-triage-security.sh — execute a schema-validated triage-security plan.
#
# This runs only on the trusted Fullsend runner after the sandbox exits.  It
# selects the validated iteration result and passes it together with the
# trusted pre-script authorization bundle to the action executor.
#
# Two roots, each with its own containment check:
#   - Fullsend runs this script with its own run directory as the working
#     directory and names the validated iteration through
#     FULLSEND_VALIDATED_ITERATION_DIR.  The result must resolve inside the
#     working directory.
#   - FULLSEND_RUN_DIR is the caller-provided, per-run directory the pre-script
#     wrote its bundle to (Fullsend does not set it).  The bundle must resolve
#     inside FULLSEND_RUN_DIR.

set -euo pipefail

: "${FULLSEND_RUN_DIR:?FULLSEND_RUN_DIR is required}"

RUN_DIR="$(pwd -P)"
BUNDLE_ROOT="$(cd "${FULLSEND_RUN_DIR}" && pwd -P)"
TRUSTED_INPUT="${BUNDLE_ROOT}/pre/triage-security-input.json"
if [[ ! -f "${TRUSTED_INPUT}" ]]; then
  echo "ERROR: trusted triage-security input is missing: ${TRUSTED_INPUT}" >&2
  exit 1
fi

# Print the result file in an iteration output directory, if any.
result_in() {
  if [[ -f "$1/agent-result.json" ]]; then
    printf '%s\n' "$1/agent-result.json"
  elif [[ -f "$1/result.json" ]]; then
    printf '%s\n' "$1/result.json"
  fi
}

RESULT_FILE=""
if [[ -n "${FULLSEND_VALIDATED_ITERATION_DIR:-}" ]]; then
  # Never fall back here: a scan could pick up output that failed validation.
  RESULT_FILE="$(result_in "${FULLSEND_VALIDATED_ITERATION_DIR}")"
else
  # Harnesses without a validation loop: take the last iteration's result.
  while IFS= read -r iteration_dir; do
    [[ -d "${RUN_DIR}/${iteration_dir}" ]] || continue
    candidate="$(result_in "${RUN_DIR}/${iteration_dir}")"
    [[ -n "${candidate}" ]] && RESULT_FILE="${candidate}"
  done < <(cd "${RUN_DIR}" && printf '%s\n' iteration-*/output | sort -V)
fi

if [[ -z "${RESULT_FILE}" ]]; then
  echo "ERROR: no validated triage-security result found in an iteration output directory" >&2
  exit 1
fi

RESULT_REAL="$(realpath "${RESULT_FILE}")"
INPUT_REAL="$(realpath "${TRUSTED_INPUT}")"
case "${RESULT_REAL}" in
  "${RUN_DIR}"/*) ;;
  *)
    echo "ERROR: selected result path escapes the Fullsend run directory" >&2
    exit 1
    ;;
esac
case "${INPUT_REAL}" in
  "${BUNDLE_ROOT}"/*) ;;
  *)
    echo "ERROR: trusted input path escapes FULLSEND_RUN_DIR" >&2
    exit 1
    ;;
esac

if ! jq empty "${RESULT_REAL}" >/dev/null 2>&1; then
  echo "ERROR: selected triage-security result is not valid JSON" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${SCRIPT_DIR}/execute-triage-security-actions.py" "${RESULT_REAL}" "${INPUT_REAL}"
