**Summary:** TC-9008: Fail-closed tracker-gated release verification
**Issue type:** Epic (level 1, assumed. See planning-decisions.md)
**Parent:** TC-9008
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**fixVersions:** omitted (TC-9008 has none)

Groups the work to authenticate tracker calls with the service-account token through the gateway, gate release verification on a "Ready for Verification" linked issue, and make every layer (client, gate, shell wrapper) fail closed so that an unauthenticated empty search can never produce a green run without verification.

Tasks: Task 1 (client auth + fail-closed search), Task 2 (gate resolution), Task 3 (pre-verify wrapper).
