-- SYNTHETIC TEST DATA — Migration with planted anti-patterns for eval
-- PLANTED ANTI-PATTERN: Step 7.8.4 — Expensive PL/pgSQL Function Pattern
--
-- The expand_license_expression_with_mappings function uses regexp_replace()
-- with dynamically concatenated patterns inside a FOREACH loop. The regex is
-- recompiled on every iteration because the pattern includes a loop variable.

DO $$
BEGIN
    CREATE TYPE license_mapping AS (license_id TEXT, name TEXT);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

CREATE OR REPLACE FUNCTION expand_license_expression_with_mappings(
    license_text TEXT,
    license_mappings license_mapping[]
) RETURNS TEXT AS $$
DECLARE
    result_text TEXT := license_text;
    mapping license_mapping;
BEGIN
    IF license_text IS NULL
       OR POSITION('LicenseRef-' IN license_text) = 0
       OR license_mappings IS NULL
       OR array_length(license_mappings, 1) IS NULL THEN
        RETURN license_text;
    END IF;

    FOREACH mapping IN ARRAY license_mappings
    LOOP
        IF POSITION('LicenseRef-' IN result_text) = 0 THEN
            EXIT;
        END IF;
        -- PLANTED: Dynamic regexp pattern concatenation inside loop
        -- The regex '\m' || mapping.license_id || '(?![a-zA-Z0-9.\-])' is
        -- recompiled on every FOREACH iteration because the pattern includes
        -- the loop variable mapping.license_id.
        result_text := regexp_replace(
            result_text,
            '\m' || mapping.license_id || '(?![a-zA-Z0-9.\-])',
            mapping.name, 'g'
        );
    END LOOP;

    RETURN result_text;
END;
$$ LANGUAGE plpgsql IMMUTABLE PARALLEL SAFE;
