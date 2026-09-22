#!/usr/bin/env bash
# post-triage-security.sh — execute a schema-validated triage-security plan.
#
# This runs only on the trusted Fullsend runner after the sandbox exits.  It
# selects the final iteration result and passes it together with the trusted
# pre-script authorization bundle to the action executor.

set -euo pipefail

: "${FULLSEND_RUN_DIR:?FULLSEND_RUN_DIR is required}"

RUN_DIR="$(cd "${FULLSEND_RUN_DIR}" && pwd -P)"
TRUSTED_INPUT="${RUN_DIR}/pre/triage-security-input.json"
if [[ ! -f "${TRUSTED_INPUT}" ]]; then
  echo "ERROR: trusted triage-security input is missing: ${TRUSTED_INPUT}" >&2
  exit 1
fi

RESULT_FILE=""
while IFS= read -r iteration_dir; do
  [[ -d "${iteration_dir}" ]] || continue
  if [[ -f "${iteration_dir}/agent-result.json" ]]; then
    RESULT_FILE="${iteration_dir}/agent-result.json"
  elif [[ -f "${iteration_dir}/result.json" ]]; then
    RESULT_FILE="${iteration_dir}/result.json"
  fi
done < <(cd "${RUN_DIR}" && printf '%s\n' iteration-*/output | sort -V)

if [[ -z "${RESULT_FILE}" ]]; then
  echo "ERROR: no validated triage-security result found in an iteration output directory" >&2
  exit 1
fi

RESULT_FILE="${RUN_DIR}/${RESULT_FILE}"
RESULT_REAL="$(realpath "${RESULT_FILE}")"
INPUT_REAL="$(realpath "${TRUSTED_INPUT}")"
case "${RESULT_REAL}" in
  "${RUN_DIR}"/*) ;;
  *)
    echo "ERROR: selected result path escapes FULLSEND_RUN_DIR" >&2
    exit 1
    ;;
esac
case "${INPUT_REAL}" in
  "${RUN_DIR}"/*) ;;
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
