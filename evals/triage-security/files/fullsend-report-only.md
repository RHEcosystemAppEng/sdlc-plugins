<!-- SYNTHETIC TEST DATA — non-production Fullsend report-only contract fixture -->

# Fullsend report-only result

This fixture represents a valid sandbox result whose proposed outcome is reported
to the engineer without any Jira mutation authorization.

```json
{
  "result": {
    "schema_version": "1",
    "mode": "report-only",
    "report": {
      "issue": "TC-42",
      "outcome": "needs-review",
      "summary_markdown": "Synthetic evidence requires engineer review.",
      "evidence": [
        {
          "source": "https://evidence.invalid/fullsend/report-only",
          "detail": "Deliberate non-production report-only evidence."
        }
      ]
    },
    "actions": [
      {
        "type": "report-only",
        "marker": "triage-security:synthetic-report-only"
      }
    ]
  },
  "trusted_input": {
    "authorization": {
      "mutation_authorized": false
    },
    "idempotency": {}
  }
}
```
