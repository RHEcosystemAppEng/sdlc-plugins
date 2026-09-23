<!-- SYNTHETIC TEST DATA — non-production Fullsend retry-idempotency contract fixture -->

# Fullsend idempotent retry result

This fixture models a rerun after the synthetic issue already has its labels,
summary comment, remediation task, and related link. The action plan therefore
must cause no duplicate Jira mutation.

```json
{
  "result": {
    "schema_version": "1",
    "mode": "mutation-authorized",
    "report": {
      "issue": "TC-42",
      "outcome": "affected",
      "summary_markdown": "Synthetic retry result.",
      "evidence": [
        {
          "source": "https://evidence.invalid/fullsend/retry",
          "detail": "Deliberate non-production retry evidence."
        }
      ]
    },
    "actions": [
      {
        "type": "field-edit",
        "marker": "triage-security:synthetic-labels",
        "issue": "TC-42",
        "fields": {
          "labels": ["ai-cve-triaged"]
        }
      },
      {
        "type": "status-transition",
        "marker": "triage-security:synthetic-status",
        "issue": "TC-42",
        "status": "In Progress"
      },
      {
        "type": "comment",
        "marker": "triage-security:synthetic-summary",
        "issue": "TC-42",
        "body_adf": {
          "type": "doc",
          "version": 1,
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "Synthetic summary already posted."
                }
              ]
            }
          ]
        }
      },
      {
        "type": "remediation-task",
        "marker": "triage-security:synthetic-remediation",
        "ref": "remediation",
        "project": "TC",
        "summary": "Fix synthetic CVE",
        "description_adf": {
          "type": "doc",
          "version": 1,
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "Synthetic remediation."
                }
              ]
            }
          ]
        },
        "labels": []
      },
      {
        "type": "link",
        "marker": "triage-security:synthetic-link",
        "link_type": "Depend",
        "inward": "TC-42",
        "outward": "{{remediation.key}}"
      }
    ]
  },
  "trusted_input": {
    "authorization": {
      "mutation_authorized": true
    },
    "idempotency": {
      "action_markers": [
        "triage-security:synthetic-labels",
        "triage-security:synthetic-summary",
        "triage-security:synthetic-remediation",
        "triage-security:synthetic-link"
      ],
      "existing_remediation": [
        {
          "key": "TC-9001",
          "summary": "Fix synthetic CVE",
          "labels": ["ai-generated-jira"],
          "comments": [
            {
              "body": "[sdlc-workflow] Description digest: sha256-adf:synthetic"
            }
          ]
        }
      ]
    },
    "issue": {
      "status": "In Progress",
      "fields": {}
    }
  }
}
```
