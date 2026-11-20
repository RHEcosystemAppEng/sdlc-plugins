# Dependency Update Conventions

This contract is shared by `triage-security` and `implement-task`. It defines how a
project supplies dependency-update and verification policy without adding a central
package-manager command catalog to the SDLC workflow.
Use `GLOSSARY.md` for the shared meanings of batch update, targeted update, resolved
dependency graph, and waiting for fix.

## Project convention format

Add a `## Dependency Updates` section to the target repository's `CONVENTIONS.md`.
The section contains exactly one fenced `json` block with a `policies` array. Use
`"*"` for a repository-wide default and an Ecosystem Mappings value for an override:

```json
{
  "policies": [
    {
      "ecosystem": "*",
      "strategy": "batch",
      "update_command": "<project-approved batch update command>",
      "targeted_fallback_command": "<project-approved targeted fallback command, or empty if prohibited>",
      "graph_command": "<project-approved command that shows all dependency paths>",
      "constraint_changes": false,
      "verification": ["<project-approved test or build command>"]
    },
    {
      "ecosystem": "<ecosystem from Ecosystem Mappings>",
      "strategy": "targeted",
      "update_command": "<project-approved command; use {package} and {fixed_version} where needed>",
      "targeted_fallback_command": "",
      "graph_command": "<project-approved command that shows all dependency paths>",
      "constraint_changes": true,
      "verification": ["<project-approved test or build command>"]
    }
  ]
}
```

Each policy has exactly these fields: `ecosystem`, `strategy` (`batch` or `targeted`),
`update_command`, `targeted_fallback_command` (empty when no targeted retry is approved),
`graph_command`, `constraint_changes` (boolean), and `verification` (an array of
project-approved checks; it may be empty when no extra checks are needed).
Commands are project data, not plugin defaults. Do not copy example commands from
another ecosystem unless they are the target project's approved commands.

`constraint_changes` governs changing an existing declared requirement/range
specifically because it excludes the fixed version. It does not prohibit the normal
dependency or lockfile update already authorized by the task when the current
requirement admits the fixed version.

The block must be valid JSON and have no duplicate ecosystem entries (case-insensitive).
An empty array explicitly declares that no strategy is supplied; treat it as a missing
applicable policy. A per-ecosystem policy overrides `"*"`. A valid section may omit
both a default and the affected ecosystem; in that case no policy applies to that task.
Only whitespace and HTML comments may appear outside the JSON block, preventing
unvalidated prose from contradicting the structured policy. A missing section is
distinct from a malformed section.

## Precedence and safety

1. Task scope and Acceptance Criteria bound the files and dependency constraints that
   may change.
2. A constraint adjustment requires permission from both the task and the applicable
   project policy (`constraint_changes: true`). A policy permission is not task
   authorization: the task must also explicitly include the affected manifest or
   requirement change in its scope/Acceptance Criteria.
3. An applicable ecosystem policy overrides the repository-wide `"*"` policy.
4. The repository-wide policy applies when there is no ecosystem override.
5. Interactive flows ask and stop if no policy applies. Fullsend may generate the
   targeted-update task fallback only when no policy applies; it never executes an
   update command.

## Triage policy gate

Use the existing stream `Ecosystem Mappings` row and Repository Registry to determine
ecosystem, repository, and remediation shape. RPM/system packages retain their
separate release-repository path. Configured source repositories use the existing
upstream task plus downstream propagation, or the dependency-bump variant when public
upstream evidence already shows the fix. If the mapping cannot distinguish these
paths, interactive triage asks and Fullsend reports the ambiguity; do not add a new
dependency-type field or language allowlist.

Run the policy gate only after impact analysis shows that a source remediation task is
needed, and before Jira mutations. Interactive triage reads the repository's
`CONVENTIONS.md`; if the matching policy is absent or malformed, it asks for correction
and stops. Fullsend uses only the matching trusted `source_evidence.conventions`
record. Missing policy or no matching/default policy emits targeted-update task
guidance. A malformed present policy emits a `needs-review` report-only result with
exactly one `report-only` action, even when mutation authorization is true. If no
supported version is affected and no remediation task is needed, this gate does not
block the existing not-affected path.

Triage records the selected strategy and commands in the task; it does not execute
the update command, graph command, or resolver. The graph command is for later
`implement-task` verification only. Public fixed-version evidence, pinned lock-file
contents, and the configured check command remain the triage evidence sources.

If task instructions conflict with a present policy, interactive flows ask the
engineer to reconcile them. Fullsend returns a report-only blocked result. A malformed
or contradictory `Dependency Updates` section is never treated as absent: interactive
flows stop and ask for correction, while Fullsend returns a report-only blocked result.

For a batch policy, implementation tries the declared batch command first. A
task-scoped constraint may be changed only with both authorizations above, and the
batch command is retried after that change. If the task does not authorize the
manifest/requirement adjustment that is needed to select the fix, interactive
implementation asks for scope clarification and stops. A targeted retry is a last
resort only after applicable batch attempts fail, and only when a
`targeted_fallback_command` is present. A targeted policy is followed as written.

The declared graph command must support inspection of all relevant resolved
dependency paths. A fix is verified only when every relevant path resolves outside
the vulnerable range and at or above the fixed version. If a permitted update cannot
remove every vulnerable path, leave the issue open in its existing status and
resolution, preserve labels while adding `waiting-for-fix`, do not comment or close,
and stop before dependent tests, commit, or PR completion.
