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

Distinguish native fullsend CLI exit, the Skill's Bash tool exit, and the host
validation loop. Expected negative-case CLI/schema failure is not itself proof
of correct gate/input behavior. The valid case requires the actual Skill inline
validator after the completed result write, not merely host validate-output-schema.sh
or standalone validation of a sample. Inspect actual output file inventory and
raw tools to establish that no prohibited sandbox files or external calls occurred.
Opaque CLI metrics may lack cost_usd; that is not a runtime success signal.
