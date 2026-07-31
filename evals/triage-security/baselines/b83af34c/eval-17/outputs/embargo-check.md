# Step 1.7 -- Embargo Check

## Configuration Check

- Embargo policy URL configured: **Yes** (`https://example.com/security/embargo-policy`)
- Since an Embargo policy URL is configured, Step 1.7 proceeds (not skipped).

## Severity Evaluation

- CVE: CVE-2026-31812
- CVSS score: **7.5**
- Severity level: **High**
- Embargo trigger threshold: CVSS >= 7.0 (Critical or Important/High severity)
- Evaluation result: **7.5 >= 7.0 -- threshold MET**
- Action: **Present warning gate** (embargo check triggers)

### Threshold Logic

Per SKILL.md Step 1.7:
- CVSS >= 7.0 (Critical or Important severity): **trigger embargo warning gate**
- CVSS < 7.0 (Low or Moderate severity): **skip silently, proceed to Step 2**

CVE-2026-31812 has CVSS 7.5 which is High severity. This meets the Critical/Important threshold (>= 7.0), so the embargo warning gate is triggered.

### Low/Moderate Severity Behavior

For CVEs with CVSS < 7.0 (Low or Moderate severity), Step 1.7 is skipped silently. No warning is presented, no confirmation is required, and the skill proceeds directly to Step 2 (Version Impact Analysis). The gate only fires for high-severity vulnerabilities that may be under embargo.

Examples:
- CVSS 3.1 (Low): Step 1.7 skipped silently, proceed to Step 2
- CVSS 5.3 (Moderate): Step 1.7 skipped silently, proceed to Step 2
- CVSS 6.9 (Moderate): Step 1.7 skipped silently, proceed to Step 2
- CVSS 7.0 (High): Step 1.7 triggers embargo warning gate
- CVSS 7.5 (High): Step 1.7 triggers embargo warning gate (this CVE)
- CVSS 9.8 (Critical): Step 1.7 triggers embargo warning gate

## Warning Gate Presented to Engineer

```
EMBARGO CHECK -- CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

### Gate Behavior

This is a **confirmation prompt** requiring explicit engineer input, not merely an informational message:

- **If "No"**: Execution stops immediately. The engineer is informed to check embargo status with their security team before re-running triage. No further steps are executed -- Step 2 and beyond are not reached.
- **If "Yes"**: Triage proceeds normally to Step 2 (Version Impact Analysis).

The gate requires an explicit Yes or No response. The skill does not proceed until the engineer provides a response. There is no timeout or auto-proceed behavior. This is consistent with the existing guardrail pattern in the skill: "every Jira mutation requires confirmation."

No Jira mutations occur at this step -- the gate fires before any triage output, so stopping is safe.

## Simulated Response

For this eval, the engineer confirms: **Yes** -- proceed with triage.

Proceeding to Step 2 (Version Impact Analysis).
