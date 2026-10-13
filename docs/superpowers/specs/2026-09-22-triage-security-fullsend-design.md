# Triage-Security Fullsend Dual-Mode Design

## Goal

Allow `triage-security` to perform the existing CVE decision tree in a tokenless
Fullsend sandbox while preserving the interactive Jira, web, and Git behavior when
`FULLSEND_OUTPUT_DIR` is genuinely absent.

## Scope

The implementation changes only the triage-security skill instructions, its three
companion procedure documents, and its eval contract. The existing Fullsend harness,
trusted input schema, result schema, prefetch script, action executor, and output
validator are dependencies supplied by TC-6207 through TC-6209 and are not changed.

## Mode Selection and Input

The skill detects Fullsend from the *presence* of `FULLSEND_OUTPUT_DIR`. An exported
empty value is a configuration error: it must fail closed, rather than selecting the
credentialed interactive path. When the variable is absent, every current interactive
step and confirmation gate remains in force.

When the variable is non-empty, the skill reads only
`/sandbox/workspace/.pre-script/triage-security-input.json` and validates it against
`${CLAUDE_PLUGIN_ROOT}/schemas/triage-security-input.schema.json`. Missing,
unparseable, or schema-invalid data produces a failure result and stops the workflow;
it never triggers Jira, GitHub, web, CVE, or credentialed repository fallback. Mounted
repository evidence is read-only. The sandbox never writes `security-matrix.md`.

The failure result is deliberately `{ "error": "..." }`, without the result schema's
required `schema_version`, `mode`, `report`, and `actions` members. The runner's
output validation must reject it visibly, matching verify-pr's fail-closed behavior;
the skill stops immediately after writing it.

## Analysis Flow

Fullsend preserves the interactive order: configuration and staleness evaluation;
issue extraction, enrichment, and embargo assessment; version-impact analysis; Jira
operations; remediation; and the post-triage summary. Each stage consumes the matching
validated bundle section instead of performing an external read:

| Interactive source | Fullsend source |
|---|---|
| CLAUDE.md/Jira configuration | `configuration` |
| Jira issue and remote links | `issue`, `remote_links`, `jira_metadata` |
| MITRE, OSV, lifecycle pages | `external_evidence` |
| matrices and release/source lookups | `matrix`, `source_evidence` |
| existing actions/tasks/comments/links | `idempotency` |

Evidence requirements do not weaken in Fullsend: all supported versions, released
pinned commits, development heads, retags, lock-file and dependency-chain evidence,
external fix-threshold precedence, duplicate checks, and reporter/ProdSec data retain
their current semantics.

## Result and Mutations

The sandbox accumulates a result conforming to
`triage-security-result.schema.json`: `schema_version`, `mode`, an evidence-backed
`report`, and ordered `actions`. Its stable action markers make an action-plan rerun
idempotent.

When `authorization.mutation_authorized` is false, `mode` is `report-only` and the
only action is `report-only`. The report names every withheld mutation and explains
that trusted-runner authorization is required.

When it is true, each interactive mutation becomes one existing schema action:

| Interactive operation | Fullsend action |
|---|---|
| Assignment, Affects Versions, VEX, labels | `field-edit` |
| Assigned, In Progress, Closed transitions | `status-transition` |
| Triage, digest, reconciliation, and summary comments | `comment` |
| Related, Depend, and Blocks relationships | `link` |
| Remediation task creation | `remediation-task`, followed by references and links |

Action order preserves the original protocol: task creation, description digest
comment, reference resolution, links, and later comments. Interactive confirmation
prompts become deterministic authorization in Fullsend; interactive confirmations are
unchanged.

## Documentation Changes

`SKILL.md` defines the top-level dual-mode contract and applies it to every numbered
step. `version-impact-analysis.md` substitutes trusted matrix/source/lifecycle evidence
for every external read and blocks matrix repair in the sandbox.
`jira-triage-operations.md` turns every write surface into an action or report-only
recommendation. `remediation-templates.md` specifies serialized task descriptions,
labels, links, digest comments, action-reference ordering, and report-only behavior.

## Evaluation

The triage-security evals retain current standard, already-fixed, duplicate,
split-stream, RPM, enrichment, overlap, reconciliation, and rerun scenarios. New
assertions cover gate detection, valid-bundle-only execution, no sandbox-side external
calls or writes, report-only output, authorized structured actions, preserved ordering,
and idempotent retry markers. They also assert that an absent Fullsend gate continues
to use the established interactive path.

## Non-Goals

This work does not change the JSON schemas, harness, pre/post scripts, action executor,
security-matrix format, existing interactive decision rules, or Jira state outside the
task’s normal implementation lifecycle.
