# Skill-eval CI models

The two skill-eval CI workflows both drive `claude -p` with the
`sdlc-workflow:run-evals` skill, so they must select the same models: PR results
are compared against baselines the other workflow produces.

| Workflow | File | Trigger |
|---|---|---|
| Eval PR Run | `.github/workflows/eval-pr-run.yml` | `workflow_run` on **Eval PR** completion |
| Eval Baseline | `.github/workflows/eval-baseline.yml` | push to `main` |

## Model environment variables

Both workflows set the same three variables on the step that runs the eval agent
("Run PR evals" and "Run evals and create baselines" respectively):

| Variable | Value | Effect |
|---|---|---|
| `ANTHROPIC_MODEL` | `claude-opus-5-5` | model used by the eval agent and its sub-agents |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | `claude-opus-5-5` | model behind the `opus` alias for sub-agents |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | `claude-sonnet-5-5` | model behind the `sonnet` alias for sub-agents |

`ANTHROPIC_VERTEX_PROJECT_ID` and `CLOUD_ML_REGION` are not model selectors; they
come from repository secrets and are unchanged by model migrations.

Sonnet 5.5 rejects a forced `tool_choice`. Claude Code's normal agent loop does not
force it, so any sub-agent that selects the `sonnet` alias works — the live run in
the pre-merge proof recipe below is what confirms it.

## Change both workflows together

Edit both files in the same change. `plugins/sdlc-workflow/scripts/test_skill_eval_models.py`
parses the eval step of each workflow and fails when:

- either workflow is missing one of the three variables,
- a value is not the target model, or
- the two workflows disagree on any variable.

Run it with the rest of the script suite before committing:

```bash
python3 -m pytest plugins/sdlc-workflow/scripts/ -q
```

## Baseline comparability

Baselines are committed per skill under `evals/<skill>/baselines/<commit>/` and
compared by PR runs against the ones already on `main`. A model change makes old
baselines non-comparable: until a new baseline created on the new models lands on
`main`, PR runs may report differences that come from the model, not from the PR.
Say so in the PR that performs the migration.

`eval-baseline.yml` re-baselines automatically only when the merge commit matches
its `on.push.paths` filter. A model migration edits `eval-baseline.yml` itself,
and that path is in the filter, so the merge triggers a fresh baseline. If you
move the pins somewhere else, keep that filter in mind or re-baseline manually.

## GCP project enablement prerequisite

Both workflows authenticate to Vertex AI in the project behind `secrets.GCP_PROJECT_ID`
through Workload Identity Federation. The new model IDs must be enabled in that
project before the first run, or the eval agent fails at the first API call. The
pre-merge proof run below is what proves enablement.

## Pre-merge proof recipe

`eval-pr-run.yml` is a `workflow_run` workflow that executes from `main`, and
`eval-baseline.yml` runs on push to `main` — neither can exercise its own change
from a PR branch. Prove the new models before merge with one of:

1. **Temporary workflow:** copy the `claude -p` eval step into a throwaway
   `pull_request` workflow on the task branch, pinned to the new
   `ANTHROPIC_*` values, and run at least one skill suite. A
   `workflow_dispatch` workflow cannot be used here: it is only dispatchable
   once it exists on the default branch. Confirm the run writes
   `benchmark.json`, `feedback.json`, `summary.md` and graded per-case results.
   Remove the throwaway workflow before merge.

   The task branch must live in the upstream repository. On a `pull_request`
   run whose head is a FORK, GitHub withholds repo vars/secrets and OIDC
   (id-token), so the temporary workflow cannot authenticate to Vertex AI and
   fails before proving anything — the same limitation that makes
   `fullsend-verify-pr.yml` a `pull_request_target` workflow (TC-6331). A
   `pull_request_target` copy is not a way out here either: it runs the base
   branch's version of the workflow, so it would not exercise the pins under
   test. Fork contributors should therefore use option 2, or ask a maintainer
   to push the branch to the upstream repository.
2. **Local run:** export the same `ANTHROPIC_*` values and Vertex credentials for
   the `secrets.GCP_PROJECT_ID` project, then run the same `claude -p` command
   against one skill suite locally and inspect the workspace output.

Record the run (workflow URL or local workspace path) in the PR so reviewers can
see the models produced graded results, not just a successful process exit.
