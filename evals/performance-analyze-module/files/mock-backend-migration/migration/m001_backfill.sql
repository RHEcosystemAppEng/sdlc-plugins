-- SYNTHETIC TEST DATA — Migration with planted anti-patterns for eval
-- PLANTED ANTI-PATTERN: Step 7.8.1 — Missing Statistics Refresh (Missing ANALYZE)
-- PLANTED ANTI-PATTERN: Step 7.8.2 — Non-Materialized CTE Re-evaluation
--
-- This migration creates a dictionary table and backfills it from existing
-- SBOM license data. It has two planted issues:
-- 1. No ANALYZE before the bulk INSERT...SELECT (stale planner statistics)
-- 2. A CTE with a function call that is referenced twice without MATERIALIZED

-- Step 1: Create dictionary table
CREATE TABLE IF NOT EXISTS expanded_license (
    id SERIAL PRIMARY KEY,
    expanded_text TEXT NOT NULL,
    text_hash TEXT GENERATED ALWAYS AS (md5(expanded_text)) STORED UNIQUE
);

-- Step 2: Create junction table
CREATE TABLE IF NOT EXISTS sbom_license_expanded (
    sbom_id UUID NOT NULL,
    license_id INTEGER NOT NULL,
    expanded_license_id INTEGER NOT NULL REFERENCES expanded_license(id),
    PRIMARY KEY (sbom_id, license_id)
);

CREATE INDEX IF NOT EXISTS idx_sle_expanded_license_id
ON sbom_license_expanded (expanded_license_id);

-- PLANTED (7.8.1): No ANALYZE statement before the backfill queries.
-- The sbom_package_license and license tables may have stale statistics
-- (especially if recently bulk-loaded), causing the planner to misestimate
-- row counts for the JOIN and produce a suboptimal plan.

-- Backfill Step 1: Insert unique expanded texts into dictionary
INSERT INTO expanded_license (expanded_text)
SELECT DISTINCT expand_license_expression_with_mappings(
    l.text,
    COALESCE(lim.license_mapping, ARRAY[]::license_mapping[])
)
FROM sbom_package_license spl
JOIN license l ON l.id = spl.license_id
LEFT JOIN (
    SELECT array_agg(ROW(license_id, name)::license_mapping) AS license_mapping, sbom_id
    FROM licensing_infos
    GROUP BY sbom_id
) lim ON lim.sbom_id = spl.sbom_id
WHERE NOT EXISTS (
    SELECT 1 FROM sbom_license_expanded sle
    WHERE sle.sbom_id = spl.sbom_id
)
ON CONFLICT (text_hash) DO NOTHING;

-- PLANTED (7.8.2): Non-materialized CTE with function call, referenced twice.
-- The CTE 'license_expansions' calls expand_license_expression_with_mappings()
-- and is used in both the INSERT target columns (ne.expanded) and the JOIN
-- condition (md5(ne.expanded)). Without MATERIALIZED, PostgreSQL 12+ may
-- inline the CTE and evaluate the function twice per row.
WITH license_expansions AS (
    SELECT DISTINCT
        spl.sbom_id,
        spl.license_id,
        expand_license_expression_with_mappings(
            l.text,
            COALESCE(lim.license_mapping, ARRAY[]::license_mapping[])
        ) AS expanded
    FROM sbom_package_license spl
    JOIN license l ON l.id = spl.license_id
    LEFT JOIN (
        SELECT array_agg(ROW(license_id, name)::license_mapping) AS license_mapping, sbom_id
        FROM licensing_infos
        GROUP BY sbom_id
    ) lim ON lim.sbom_id = spl.sbom_id
    WHERE NOT EXISTS (
        SELECT 1 FROM sbom_license_expanded sle
        WHERE sle.sbom_id = spl.sbom_id AND sle.license_id = spl.license_id
    )
)
INSERT INTO sbom_license_expanded (sbom_id, license_id, expanded_license_id)
SELECT ne.sbom_id, ne.license_id, el.id
FROM license_expansions ne
JOIN expanded_license el ON el.text_hash = md5(ne.expanded)
ON CONFLICT (sbom_id, license_id) DO UPDATE
SET expanded_license_id = EXCLUDED.expanded_license_id;
