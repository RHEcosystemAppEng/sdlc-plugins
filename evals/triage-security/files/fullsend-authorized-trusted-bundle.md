<!-- SYNTHETIC TEST DATA — schema-valid trusted Fullsend evidence -->

# Trusted bundle facts

The mounted `triage-security-input.json` is already schema-valid. It contains
only the following evidence needed for this case:

- Issue `TC-8100`; authorization `mutation_authorized: true`.
- Trusted assignee account ID `557058:fullsend-engineer`.
- Affects Versions `2.2.0`, VEX Justification `Affected`, and new label
  `security-triaged`.
- Transition `In Progress` and one triage comment represented as valid ADF.
- A remediation task for `TC-8100` with stable ref `remediation-8100`; its
  existing Jira task has no description digest yet.
- A Depend link from `TC-8100` to `{{remediation-8100.key}}`.
- Existing idempotency marker `triage-security:tc-8100:field-edit:label:legacy`.

No other files, credentials, or external evidence are available. All supplied
values must be used as-is; no account, version, or reference lookup is needed.
