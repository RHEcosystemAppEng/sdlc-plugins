# Native Fullsend gate evals

TC-6677 moves cases 033–036 into a separate native Fullsend suite. Ordinary
`sdlc-workflow:run-evals` retains the original triage32/164 and verify6/68.
This suite invokes the actual `sdlc-workflow:triage-security` Skill for synthetic
TC-8101 through a test agent. It covers real Skill execution in Fullsend with
synthetic bundles; full production pre/post integration and native verify-pr coverage remain separate.
TC-6213 stays closed for its approved scope; hosted rollout evidence belongs to TC-6726.

**Local native execution is proven:** fresh run
`tc6677-8d4aab96a2684e47ab5f1fdf65700a8b` passed all 21/21 on 2026-10-05,
with real Skill/native tool evidence, malformed rejection and report-only final
validation. **Hosted WIF execution remains unproven until a real GitHub run.**
Static tests and preflight do not establish hosted credentials, infrastructure or grading.

## Versions and prerequisites

Use Python3.12, Git and curl on macOS or Linux (amd64/arm64). `setup` installs
only into the chosen cache. It verifies Fullsendv0.43.0 release archives against
the SHA256 values in [dependencies.json](../../evals/fullsend/dependencies.json),
and fetches canonical agent-eval-harness1.22.0 at immutable commit
`4b540c652f5ed325e18abf6b4bd0eb4414a4bb3c`. Python runtime/Vertex/build
dependencies are exactly versioned and hash-locked in
[requirements.lock](../../evals/fullsend/requirements.lock). The harness wheel
is built from that verified source with locked build tools; its generated wheel
bytes are not claimed reproducible. OpenShell, Podman, the host OS, service
configuration and the delivered model runtime inside the production image are
outside the Python lock.

The operator must provide installed **OpenShell CLI and gateway0.0.116**, Podman,
an approved running gateway and container-driver configuration, and an accessible
production sandbox image. The pin is Fullsendv0.43.0's
[OpenShell pin file](https://github.com/fullsend-ai/fullsend/blob/d5f36921ac754705619f38c637ef692873809fbc/.github/scripts/openshell-version.sh).
The agents `LOCAL.md` copy mentions older0.0.83; do not use that version.
The inspected0.0.116 CLI has `gateway add/select/list`, **no `gateway start`**;
provision/run `openshell-gateway` using your existing approved authenticated
configuration. The Python entrypoint does not install or start host services, create
credentials, change gateway/TLS configuration, or relax sandbox policy.

Platform differences:

- **macOS:** Python3.12 and curl may need separate installation; Podman needs
  an initialized/running machine. Paths are resolved to physical paths (including
  `/private/tmp`) for delivery. Setup downloads the Darwin host binary and the
  matching Linux binary for the sandbox. The VM/image CPU architecture must match
  the selected host architecture; cross-architecture execution is not prepared here.
- **Linux/CI:** provide Python3.12 with venv support, Git, curl and CA certificates.
  Rootless Podman needs valid subordinate UID/GID mappings and an active API socket,
  normally `${XDG_RUNTIME_DIR}/podman/podman.sock`. Provision these through the
  runner's approved host setup, along with OpenShell's authenticated gateway and
  required supervisor image. The existing Fullsend
  [functional CI source](https://github.com/fullsend-ai/fullsend/blob/d5f36921ac754705619f38c637ef692873809fbc/.github/workflows/functional-tests.yml)
  documents this host dependency. The trusted CI wrapper reuses the pinned upstream
  installers and rootless Podman setup; Python `setup` remains dependency-only.

For further platform context, consult the pinned
[Fullsend local guide](https://github.com/fullsend-ai/fullsend/blob/d5f36921ac754705619f38c637ef692873809fbc/docs/guides/user/running-agents-locally.md).
Use the actual installed OpenShell CLI/help and approved gateway configuration
where older guide commands differ.

## Common local and CI commands

Run from the reviewed repository checkout. The following two commands perform
**dependency/CLI checks only** and need no inference credentials:

```bash
python3.12 evals/fullsend/run.py setup --cache /tmp/tc-6677-eval-deps
python3.12 evals/fullsend/run.py preflight --cache /tmp/tc-6677-eval-deps
```

`setup` fetches pinned source/packages/releases; it performs no global install.
It overrides host pip user-install defaults and keeps pip's cache in the selected
directory. curl retains normal host TLS verification; SHA256 verification is
mandatory before installing a binary. A corrupt cached archive fails visibly;
remove that specific archive and repeat setup after investigating the mismatch.
`preflight` checks exact package versions, clean pinned framework source,
upstream workspace/execute/collect/score CLI imports, suite configuration,
Fullsend CLI flags, and OpenShell/Podman versions. It does not prove gateway
reachability, authentication, image availability, environment propagation or tools.

For actual execution, the operator supplies existing Vertex inference credentials
and host judge credentials through these environment variables:

| Variable | Required input |
|---|---|
| `GOOGLE_APPLICATION_CREDENTIALS` | Absolute path to the operator-provided GCP credential file, accessible to native Fullsend and the host judge |
| `ANTHROPIC_VERTEX_PROJECT_ID` | Vertex project with access to the selected Claude models |
| `GOOGLE_CLOUD_PROJECT` | GCP project used by the production Vertex environment mount |
| `CLOUD_ML_REGION` | Vertex region supporting both selected models |

The production credential provider/profile/environment mount is reused unchanged.
The test harness uses the existing native host-file pattern to upload the
operator-provided `GOOGLE_APPLICATION_CREDENTIALS` file directly to
`/tmp/.gcp-credentials.json`, the path referenced by that environment template.
This mount is required and is not expanded as text. The adapter never reads or
stages credential contents in `native-config`, the checkout or output. Native
Fullsend controls the upload into the sandbox; the host judge keeps using the
original operator-provided path.
Do not print environment values, place credential files in the checkout/output,
or redirect `GOOGLE_APPLICATION_CREDENTIALS` to its sandbox path for host scoring.
`FULLSEND_MINT_URL` must be unset for this synthetic suite: the adapter refuses it
because native Fullsend would otherwise attempt live forge-token minting. No Jira
or GitHub fixture/token/issue URL is needed. No live prefetch, post-script or status
notification is configured.

After host services and those inputs are ready, the operator can run:

```bash
python3.12 evals/fullsend/run.py run \
  --cache /tmp/tc-6677-eval-deps \
  --output /tmp/tc-6677-native-evals \
  --model claude-opus-4-8 \
  --judge-model claude-opus-4-6 \
  --effort high
```

This command **does perform paid inference**: four serial native Fullsend runs
and21 upstream Boolean LLM judgments. Select model IDs supported by your Vertex
project/region. Model availability is not checked by preflight. The native
agent timeout is30minutes, the opaque CLI case timeout40minutes, and the test
validation loop has one iteration. Framework budget hints are advisory, not a
spend cap. A zero/unknown framework cost is not evidence of zero actual cost;
the unchanged native metrics use `total_cost_usd`, while CliRunner looks for
`cost_usd`. Use the retained native metrics.

## Automatic CI, WIF and rollout

TC-6726 extends `Eval PR` → `Eval PR Run`. The path-filtered trigger includes
native cases/tooling and triage Skill, fixtures, schemas, policy, profile,
provider and environment companions. Native discovery is initially restricted
to **PR299, targeting main, with source branch `verify-pr-fullsend`**. Other PRs
continue ordinary evals. Collaborators with write/admin permission retain automatic
execution; external authors require the existing `eval-protected` approval.

Discovery resolves the triggering head against the GitHub API, checks the exact
merge commit's base/head parents and stores all three SHAs. Every checkout uses
an immutable SHA with `persist-credentials: false`. Before WIF, native execution
rechecks the approved PR identity, head, base and merge; a changed revision fails
and needs a new run/approval. Results/reviews bind to that exact head and merge,
rather than a floating `refs/pull/.../merge` or newer PR revision.

The native job has only `contents: read` and `id-token: write`. Its workflow,
Python entrypoint/adapter, dependency lock, dataset/judge, synthetic pre-script,
policy/profile/provider and **host schema validator executable** all come from
the trusted base checkout. The pinned upstream Fullsend checkout supplies its
OpenShell0.0.116 and Podman installers. The selected PR plugin is copied into a
separate sandbox-plugin path with `--plugin-root`; PR validator/policy bytes cannot
replace trusted host resources. Symlinks in tested plugin content are rejected
before copying. No PR setup, pip requirements or pre/post scripts execute on the
credentialed host. Production dispatch/mint/Jira hooks are absent.

Authentication reuses `FULLSEND_GCP_WIF_PROVIDER`, `FULLSEND_GCP_PROJECT_ID` and
`vars.FULLSEND_GCP_REGION`. No service-account key or GitHub App is added.
The wrapper preserves auth-created ADC in `HOST_GOOGLE_APPLICATION_CREDENTIALS`,
then runs upstream `prepare-sandbox-credentials.sh`. Its known outputs are parsed
as data, not sourced as executable shell. `GOOGLE_APPLICATION_CREDENTIALS` remains
the original host ADC for Anthropic Vertex scoring;
`TC6726_SANDBOX_CREDENTIALS` selects the separate file-based ADC for Fullsend.
`GCP_OIDC_TOKEN_FILE` is uploaded to `/sandbox/workspace/.gcp-oidc-token` and
`FULLSEND_GCP_OIDC_URL`/`FULLSEND_GCP_OIDC_AUTH_FILE` enable upstream native refresh.
The upstream reserved-variable boundary keeps refresh authentication on the host.
Missing credentials/settings fail; they never produce a successful skip.
Local invocation without the separate credential variable retains its original
single-ADC behavior.

The pinned harness owns workspace → execute → collect → score and all 21 Boolean
judgments. Expected negative native exits remain intact and are collected/scored;
missing/null/skipped/error outcomes fail. Ordinary and native results appear as
source-bound PR reviews. The combined `Eval PR Run` status fails if either requested
suite fails, is skipped, or native evidence is missing/incomplete.

Only `native-result.json` (validated revision pins, Boolean outcomes, counts and
exit/completeness status) is uploaded, with 14-day retention. Arbitrary rationales,
transcripts, credentials, generated environment/config files and raw logs are
excluded by an allowlist. Raw evidence stays private in the runner's temporary
directory and is not published as an artifact; CI reports therefore cannot replace
inspection of the local full-evidence run. The Python report export does not modify
upstream evidence or judgments. Reporting uses a separate job with GitHub write
permissions and no inference credentials.

Human delivery sequence:

1. Review and merge this real bootstrap into main. The worker prepares only the
   isolated bootstrap commit; root pushes, opens the bootstrap PR and records its
   Jira URL. Neither agent merges.
2. Root integrates the suite and activation on PR299 while preserving its existing
   fixes. Normal activation removes the PR299/source-branch rollout restriction in
   discovery and the native recheck, retaining all revision/trust checks.
3. After bootstrap merge, trigger the existing PR eval flow for a fresh PR299
   revision and inspect its source-bound ordinary/native results. A real WIF-backed
   hosted 21/21 is required; local 21/21 and static checks cannot substitute.
4. Hand off PR299 merge to a human only after that validation. Once activation
   reaches main, relevant PRs run native evals through the same approval flow.

The worker does not dispatch paid inference or provision a local sandbox. Hosted
WIF policy/audience, installer/gateway behavior, image/model availability and refresh
must still be validated in the real run. This bootstrap does not broaden main's
active verify-pr dispatch or close TC-6201/unrelated issues.

## Cases and raw evidence

| Case | Input/gate | Strict assertions |
|---|---|---:|
| 033-absent | Test fragment unsets native gate; target CLAUDE.md lacks Security Configuration | 4 |
| 034-empty | Test fragment exports an empty gate; no target CLAUDE.md/input | 5 |
| 035-malformed | Native nonempty gate; exact retained malformed bytes mounted | 5 |
| 036-valid | Native nonempty gate; retained trusted report-only bundle mounted | 7 |

The input mount is `/sandbox/workspace/.pre-script/triage-security-input.json`.
The native output directory is `/sandbox/workspace/output`, **not `/sandbox/output`**.
Negative gate injection uses a mounted test-only `.env.d` fragment sourced before
model launch, as supported by Fullsendv0.43.0 `bootstrapEnv` and Claude runtime
`buildRunCommand`. It is deliberate negative configuration, not a normal Fullsend
configuration. Source support does not establish runtime propagation.

The test agent bypasses only the production agent's input-before-Skill startup
guard by invoking the actual Skill first. It does not duplicate gate/validator
logic or run nested model CLIs. The absent case must reach the existing interactive
missing-configuration guard before credentials. Empty must fail at the precise
gate instruction. Malformed must execute the actual input validator and error-only
abort. Valid must perform real analysis, write the completed result, then execute
the actual inline final JSON/schema validator. Every assertion requires genuine
Skill/tool records and intended plugin binding; narrated outcomes fail.

Each local case copies the unchanged delivered plugin (including script companions),
test agent/pre-script and the three retained synthetic fixtures into its isolated
`native-config` directory. Resource paths and fixture/schema references point
inside that directory, which Fullsend uses as the resolver workspace root through
`--fullsend-dir`. The separate synthetic target is a fresh local `git init`
repository, with no remote or commit. Its only project file is the absent case's
`CLAUDE.md`; the other cases have no project configuration or input content.
Pinned Fullsend0.43.0 `UploadDir` includes `.git`, and read-only setup requires
that metadata directory; neither operation requires a commit. The fresh local 21/21 run exercised this source
contract; hosted setup still needs its own real WIF run. The target never points at the
real repository. No containment check is disabled and external resource symlinks
are not used.

Generated host mounts resolve to `native-config/pre/`. The test pre-script writes
the required exact gate fragment there for every case, and the exact retained
input for malformed/valid. It uses the known configuration root; Fullsend0.43.0
does not provide `FULLSEND_RUN_DIR` to pre-scripts or host-file bootstrap (only
host validation commands receive it). Both generated mounts are optional during
early environment/file validation because preparation has not run yet. A failed
or stale preparation returns nonzero and Fullsend aborts before sandbox creation;
optional mounting does not turn that failure into success. The unchanged strict
runtime assertions still require the real mounted gate state and Skill execution.

The run prints its fresh destination:
`<output>/triage-security-gate/<run-id>/`. Keep that entire directory and, if needed
for diagnosing framework failures, the printed upstream temporary workspace.
Upstream `workspace.py`, `execute.py`, `collect.py`, and `score.py` own case iteration,
artifact collection and grading. The adapter forwards native stdout/stderr and
actual exit unchanged; collection copies native bytes without rewriting records.

Expected retained evidence includes:

- `cases/<id>/run_result.json`, `stdout.log`, `stderr.log`: upstream actual process
  exit and native console output, distinct from individual Bash tool exits.
- `cases/<id>/output/native/agent-*/iteration-1/transcripts/`: actual native runtime
  records showing Skill invocation/body, subsequent tool calls/results and failures.
- `cases/<id>/output/native/agent-*/iteration-1/output/`: retained native output inventory after host validation.
  Malformed may produce no file or sole `agent-result.json` containing `{}` after host stripping;
  valid produces sole `agent-result.json`, while absent/empty produce none.
- Native metrics/logs/traces and the unchanged root metrics copy when uniquely found.
- Upstream judge results and summary, with all21 individual Boolean results/rationales.

Negative cases may cause a nonzero native CLI exit because the production host
schema intentionally rejects absent/no result or the malformed abort result.
For malformed input, actual delivered Skill/tool records must prove invalid JSON
rejection with parser detail and tool exit1, native nonzero and no successful
analysis, fallback or actions. Either no result file with host rejection of the
absent result, or sole collected `agent-result.json` containing `{}` after intentional
stripping, is the expected negative outcome. An absent output directory or failed
attempted abort write **after proven real Skill invalid JSON rejection** is accepted
on the no-result path, not a disqualifying bootstrap/inference failure. No recovery
write is required when the abort creates no file. If the error-only file was written, raw tools must prove
the prescribed object was successfully written **before host validation**, followed
by host `strip_extra_properties.py` removing `error` and rejecting the success schema.
Empty output or nonzero alone cannot pass; genuine rejection and host records for
the applicable path are mandatory. Nonempty unexpected output or a success report
fails. No extra sandbox evidence file is required. The host validation loop is
separate from the Skill inline validator.
For malformed, infrastructure/inference failure is disqualifying when it prevents
actual Skill input validation. Without genuine invalid JSON proof, the case fails.
Failures preventing the required Skill execution remain failures for every case. The
entrypoint continues collection/scoring after upstream execution failure while
retaining raw exits; it refuses missing case results and delegates verdicts to
upstream judges.

At the pinned framework revision, partial judge exceptions yield `value:null`
and are omitted from aggregate values. After successful upstream scoring, the
entrypoint checks the unchanged `summary.yaml`: exactly four expected cases and
all21 applicable Boolean outcomes (4/5/5/7) are mandatory. Missing, null,
non-Boolean, error or skipped applicable outcomes fail the command. Invalid YAML,
duplicate keys, wrong run/case identities and unexpected assertion names also
fail. The scorer emits seven named records per case; only the configured
nonapplicable assertions may have its precise conditional-skip record.

This is a result-completeness gate, not grading: `False` remains a complete
outcome, upstream thresholds decide pass/fail, and nonzero upstream scoring exits
are preserved. No summary bytes, scores, rationales or native exits are changed.
Operators must still reconcile judgments/rationales against genuine raw execution
records; a complete summary alone does not prove correct Skill execution.
No task/bug closure follows from static tests, host schema validation or a
successful dependency preflight.

## Deterministic development checks

```bash
python3 -m pytest plugins/sdlc-workflow/scripts/ -q
python3 -m pytest plugins/sdlc-workflow/skills/run-evals/scripts/ -q
git diff --check
uvx skillsaw
claude plugin validate plugins/sdlc-workflow
```

The fixture/CLI tests use explicitly synthetic process doubles and never execute
an agent. Production source-contract tests establish instruction contracts only.
The fresh local run proves the four paths locally; hosted WIF acceptance remains
pending until the bootstrap is merged and PR299 runs successfully.

An optional no-inference resolver regression uses actual Fullsend APIs from a
temporary snapshot of pinned source `d5f36921ac754705619f38c637ef692873809fbc`.
It needs Go1.26.5 or newer and already cached module dependencies (downloads and
automatic toolchain installation are disabled). It proves resource resolution and
early environment validation without a generated run-directory variable, confirms
generated source paths and exact prepared bytes, and rejects external profiles
and symlink escapes; it does not launch
Fullsend or a model. Consumer setup/run commands do not require this source or Go.

```bash
TC6677_FULLSEND_SOURCE=/path/to/read-only/fullsend-clone \
TC6677_GO_CACHE=/tmp/tc-6677-go-build-cache \
python3 -m pytest plugins/sdlc-workflow/scripts/test_fullsend_gate_eval.py \
  -q -k actual_pinned_fullsend_resolver
```
