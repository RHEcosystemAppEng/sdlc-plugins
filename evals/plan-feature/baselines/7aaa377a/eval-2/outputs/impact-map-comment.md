# Impact Map Comment — Posted to TC-9002

This comment would be posted on the Jira feature issue TC-9002 via `jira.add_comment(TC-9002, <content>)`.

## Comment Content (ADF format)

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "content": [
        { "type": "text", "text": "Repository Impact Map" }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        { "type": "text", "text": "trustify-backend" }
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Add database migration to create indexes on frequently searched columns (SBOM name/version, advisory title/severity, package name/license) to improve full-text search query performance" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Optimize SearchService query execution to use indexed columns and improve result ranking by relevance scoring" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Extend the search API endpoint (GET /api/v2/search) to accept filter query parameters for entity type, severity, and date range" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Extend shared query builder helpers in common/src/db/query.rs to support the new search filter types" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Add and update integration tests in tests/api/search.rs covering filtered search, relevance ordering, and query performance characteristics" }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        { "type": "text", "text": "Excluded requirements" }
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "\"Better UI\" (non-MVP): No frontend repository is available in the Repository Registry. The only target repository (trustify-backend) is a Rust backend service. UI improvements require a frontend repository to be added to the project configuration." }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Specific performance targets for \"Search should be faster\": The feature states \"currently too slow\" but provides no latency benchmarks or target response times. Index and query optimizations are planned, but acceptance testing against specific latency thresholds requires the engineer to define quantified targets." }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Relevance ranking definition for \"Results should be more relevant\": The feature states \"users complain about irrelevant results\" but does not define what constitutes a relevant result, ranking criteria, or weighting factors. Basic relevance scoring (full-text search rank) is planned, but a domain-specific relevance model requires product input." }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Specific filter fields for \"Add filters\": The requirement says \"some kind of filtering capability\" without specifying which fields should be filterable. The plan assumes entity-type, severity, and date-range filters based on the existing data model. The engineer should confirm the filter set with the product owner." }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Non-functional requirement \"Should be fast enough\": No quantified performance target is provided. This NFR cannot be validated without a concrete threshold." }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "rule"
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "This comment was AI-generated by "
        },
        {
          "type": "text",
          "text": "sdlc-workflow/plan-feature",
          "marks": [
            {
              "type": "link",
              "attrs": {
                "href": "https://github.com/RHEcosystemAppEng/sdlc-plugins"
              }
            }
          ]
        },
        {
          "type": "text",
          "text": " v0.13.7."
        }
      ]
    }
  ]
}
```
