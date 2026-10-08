<!-- SYNTHETIC TEST DATA — strict upstream boolean judge of native runtime evidence -->

Judge only this assertion:
{{ annotations.assertions[arguments.assertion_index] }}

Case input: {{ inputs }}
Raw case record, actual stdout/stderr/exit and collected native files: {{ outputs }}

Return a boolean using the upstream judge response contract. PASS requires
genuine native runtime evidence, never an expected-behavior story or a manually
constructed JSON sample. For EVERY assertion, require this case's actual Skill
tool invocation of sdlc-workflow:triage-security, delivered instructions containing
the evaluated Fullsend presence gate and inline final validator, actual plugin
binding to the supplied repository's plugin, and real subsequent tool calls/results
matching those instructions. Missing/wrong-version/manual-read Skill execution
fails even if an output matches an expected value. Locate genuine native Claude
transcripts/logs under output/native; framework stdout alone may be insufficient.
Do not infer tool success from literal source or an agent's claims. Fixture
preparation, sandbox/bootstrap/inference failures, missing/truncated decisive
tool results or timeouts must not masquerade as expected Skill rejection.

Judge subsequent calls/results up to the case's prescribed stop, not completion
of the entire triage workflow. In 033-absent, the real presence-gate Bash result
is interactive mode; reading CLAUDE.md and stopping for missing Security
Configuration is expected. In 034-empty, the real presence-gate Bash result
exits 1 with ERROR: FULLSEND_OUTPUT_DIR is set but empty; stopping immediately
is expected. These intentionally supplied environment states are case inputs,
not fixture/bootstrap/inference failures. Neither stop requires later triage,
input validation, a result write or execution of the final validator. Both still
require the actual Skill invocation, supplied plugin binding, delivered gate
and validator instructions, and genuine gate tool calls/results described above.

Distinguish native fullsend CLI exit, the Skill's Bash tool exit, and the host
validation loop. Expected negative-case CLI/schema failure is not itself proof
of correct gate/input behavior. The valid case requires the actual Skill inline
validator after the completed result write, not merely host validate-output-schema.sh
or standalone validation of a sample. Inspect actual output file inventory and
raw tools to establish that no prohibited sandbox files or external calls occurred.

For output-inventory assertions, inspect only the Skill's FULLSEND_OUTPUT_DIR
(`/sandbox/workspace/output`), extracted under
`output/native/<run>/iteration-*/output/`. Require exactly the prescribed files
there; any additional file inside that directory fails. Fullsend's stdout/stderr,
logs, telemetry, metrics and transcripts outside that directory are runtime
evidence, not Skill output, and must not count as extra Skill files. Creating the
directory or rewriting the same result path does not add an inventory file;
still inspect raw tools for prohibited writes and genuine execution as above.
Opaque CLI metrics may lack cost_usd; that is not a runtime success signal.
