<!-- SYNTHETIC TEST DATA — non-production Fullsend invalid-bundle contract fixture -->

# Fullsend invalid result

This fixture deliberately combines a mutation-authorized mode with an empty
field edit. The trusted executor must reject it before attempting a Jira write.

```json
{
  "result": {
    "schema_version": "1",
    "mode": "mutation-authorized",
    "report": {
      "issue": "TC-42",
      "outcome": "affected",
      "summary_markdown": "Synthetic evidence is contradictory and incomplete.",
      "evidence": [
        {
          "source": "https://evidence.invalid/fullsend/contradictory",
          "detail": "Deliberate contradictory non-production evidence."
        }
      ]
    },
    "actions": [
      {
        "type": "field-edit",
        "marker": "triage-security:synthetic-empty-edit",
        "issue": "TC-42",
        "fields": {}
      }
    ]
  },
  "trusted_input": {
    "authorization": {
      "mutation_authorized": true
    },
    "idempotency": {}
  }
}
```
