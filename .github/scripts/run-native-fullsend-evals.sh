#!/usr/bin/env bash
# Trusted CI setup/run wrapper; PR plugin files are only sandbox test subjects.
set -euo pipefail

cache="${RUNNER_TEMP:?}/tc6726-deps"
upstream="${GITHUB_WORKSPACE:?}/upstream-fullsend"
test "$(git -C "$upstream" rev-parse HEAD)" = d5f36921ac754705619f38c637ef692873809fbc

reviewed="${GITHUB_WORKSPACE}/native-eval-source"
: "${NATIVE_EVAL_SOURCE_SHA:?Reviewed eval source pin is required}"
if [ "$(git -C "$reviewed" rev-parse HEAD)" != "$NATIVE_EVAL_SOURCE_SHA" ]; then
  echo '::error::Reviewed native eval source changed'
  exit 1
fi
runner="$reviewed/evals/fullsend/run.py"

case "${1:?setup or run}" in
  setup)
    python3.12 "$runner" setup --cache "$cache"
    source "$upstream/.github/scripts/openshell-version.sh"
    mkdir -p "$HOME/.config/openshell"
    echo 'OPENSHELL_BIND_ADDRESS=0.0.0.0' > "$HOME/.config/openshell/gateway.env"
    cat > "$HOME/.config/openshell/gateway.toml" <<EOF
[openshell]
version = 1
[openshell.gateway]
supervisor_image = "ghcr.io/nvidia/openshell/supervisor:${OPENSHELL_VERSION}"
EOF
    bash "$upstream/.github/scripts/install-podman.sh"
    whoami_user="$(whoami)"
    if ! grep -q "^${whoami_user}:" /etc/subuid; then
      sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 "$whoami_user"
    fi
    podman system migrate
    socket_path="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/podman/podman.sock"
    mkdir -p "$(dirname "$socket_path")"
    podman system service --time=0 "unix://${socket_path}" > "$RUNNER_TEMP/tc6726-podman.log" 2>&1 &
    for _i in $(seq 1 30); do
      if [ -S "$socket_path" ] && podman --url "unix://${socket_path}" info >/dev/null 2>&1; then
        break
      fi
      sleep 1
    done
    test -S "$socket_path"
    bash "$upstream/.github/scripts/install-openshell.sh"
    export PATH="$cache/venv/bin:$PATH"
    python3.12 "$runner" preflight --cache "$cache"
    ;;
  run)
    : "${GOOGLE_APPLICATION_CREDENTIALS:?WIF host ADC is required}"
    : "${ANTHROPIC_VERTEX_PROJECT_ID:?Vertex project is required}"
    : "${CLOUD_ML_REGION:?Vertex region is required}"
    : "${TC6726_HEAD_SHA:?Exact source is required}"
    HOST_GOOGLE_APPLICATION_CREDENTIALS="$GOOGLE_APPLICATION_CREDENTIALS"
    # The native synthetic job requires external-account WIF; no key fallback.
    test "$(jq -r '.type' "$HOST_GOOGLE_APPLICATION_CREDENTIALS")" = external_account
    for credential_var in GOOGLE_APPLICATION_CREDENTIALS GOOGLE_GHA_CREDS_PATH CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE; do
      credential_value="${!credential_var:-}"
      if [ -n "$credential_value" ]; then echo "::add-mask::$credential_value"; fi
    done
    # Reuse upstream conversion without replacing the scoring process's ADC.
    # Parse only known outputs as data; never source an environment file.
    prepared_env="$RUNNER_TEMP/tc6726-sandbox.env"
    GITHUB_ENV="$prepared_env" bash "$upstream/internal/scaffold/fullsend-repo/scripts/prepare-sandbox-credentials.sh"
    while IFS= read -r credential_line || [ -n "$credential_line" ]; do
      if [ -z "$credential_line" ]; then continue; fi
      if [[ "$credential_line" == *'<<'* && "${credential_line%%<<*}" != *'='* ]]; then
        credential_name="${credential_line%%<<*}"
        credential_delimiter="${credential_line#*<<}"
        credential_value=''
        credential_separator=''
        credential_closed=false
        while IFS= read -r credential_line || [ -n "$credential_line" ]; do
          if [ "$credential_line" = "$credential_delimiter" ]; then
            credential_closed=true
            break
          fi
          credential_value+="${credential_separator}${credential_line}"
          credential_separator=$'\n'
        done
        if [ "$credential_closed" != true ]; then
          echo '::error::Unterminated upstream credential value'
          exit 1
        fi
      elif [[ "$credential_line" == *'='* ]]; then
        credential_name="${credential_line%%=*}"
        credential_value="${credential_line#*=}"
      else
        continue
      fi
      case "$credential_name" in
        GOOGLE_APPLICATION_CREDENTIALS|GCP_OIDC_TOKEN_FILE|FULLSEND_GCP_OIDC_URL|FULLSEND_GCP_OIDC_AUTH_FILE) ;;
        *) continue ;;
      esac
      # Escape multiline mask data so its lines cannot become workflow commands.
      credential_mask="${credential_value//%/%25}"
      credential_mask="${credential_mask//$'\r'/%0D}"
      credential_mask="${credential_mask//$'\n'/%0A}"
      printf '::add-mask::%s\n' "$credential_mask"
      if [ "$credential_name" = GOOGLE_APPLICATION_CREDENTIALS ]; then
        export TC6726_SANDBOX_CREDENTIALS="$credential_value"
      else
        export "$credential_name=$credential_value"
      fi
    done < "$prepared_env"
    : "${TC6726_SANDBOX_CREDENTIALS:?Prepared sandbox ADC is required}"
    : "${GCP_OIDC_TOKEN_FILE:?Native OIDC mount is required}"
    : "${FULLSEND_GCP_OIDC_URL:?Native OIDC refresh is required}"
    : "${FULLSEND_GCP_OIDC_AUTH_FILE:?Native OIDC refresh authentication is required}"
    export GOOGLE_APPLICATION_CREDENTIALS="$HOST_GOOGLE_APPLICATION_CREDENTIALS"
    export PATH="$cache/venv/bin:$PATH"
    # Native stdout/stderr/transcripts can contain credential paths or arbitrary
    # PR-generated bytes. Keep raw logs private; only export allowlisted results.
    status=0
    python3.12 "$runner" run --cache "$cache" \
      --plugin-root "$GITHUB_WORKSPACE/pr-head/plugins/sdlc-workflow" \
      --output "$RUNNER_TEMP/tc6726-private" --report-dir "$RUNNER_TEMP/tc6726-safe" \
      > "$RUNNER_TEMP/tc6726-private-run.log" 2>&1 || status=$?
    echo "Native Fullsend execution/scoring finished (exit $status); safe source-bound result only."
    exit "$status"
    ;;
  *) echo '::error::Expected setup or run'; exit 1 ;;
esac
