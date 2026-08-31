#!/usr/bin/env python3
"""Strip additional properties from JSON based on a JSON Schema.

Recursively walks the schema tree and removes properties not declared
in `properties` or `allOf/if/then/properties` at every node where
`additionalProperties: false`. Works with any schema structure
including discriminated unions (allOf with if/then).

CLI usage (called by validate-output-schema.sh):
    python3 strip_extra_properties.py <json-file> <schema-file>

Strips the JSON file in-place and exits 0. The caller validates after.
"""

import json
import sys


def _resolve_ref(ref, root):
    node = root
    for part in ref.lstrip("#/").split("/"):
        node = node[part]
    return node


def _deref(schema, root):
    if "$ref" in schema:
        return _resolve_ref(schema["$ref"], root)
    return schema


def _matching_then(instance, branches):
    """Find the allOf branch whose `if` matches the instance."""
    for branch in branches:
        if_clause = branch.get("if", {})
        if_props = if_clause.get("properties", {})
        match = all(
            instance.get(k) == v.get("const")
            for k, v in if_props.items()
            if "const" in v
        )
        if match and "then" in branch:
            return branch["then"]
    return None


def strip(instance, schema, root):
    """Recursively strip properties not allowed by the schema."""
    schema = _deref(schema, root)

    if not isinstance(instance, dict) or schema.get("type") not in ("object", None):
        return instance

    then = _matching_then(instance, schema.get("allOf", []))
    has_strict = schema.get("additionalProperties") is False
    then_strict = then is not None and then.get("additionalProperties") is False

    if has_strict or then_strict:
        allowed = set(schema.get("properties", {}).keys())
        if then:
            allowed |= set(then.get("properties", {}).keys())
        removed = [k for k in instance if k not in allowed]
        if removed:
            print(f"  stripped: {removed}")
        instance = {k: v for k, v in instance.items() if k in allowed}

    for key, prop_schema in schema.get("properties", {}).items():
        if key not in instance:
            continue
        prop_schema = _deref(prop_schema, root)
        if isinstance(instance[key], dict):
            instance[key] = strip(instance[key], prop_schema, root)
        elif isinstance(instance[key], list):
            items_schema = prop_schema.get("items", {})
            items_schema = _deref(items_schema, root)
            instance[key] = [
                strip(item, items_schema, root) if isinstance(item, dict) else item
                for item in instance[key]
            ]

    return instance


def main():
    if len(sys.argv) < 3:
        print("Usage: strip_extra_properties.py <json-file> <schema-file>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        instance = json.load(f)
    with open(sys.argv[2]) as f:
        schema = json.load(f)

    instance = strip(instance, schema, schema)

    with open(sys.argv[1], "w") as f:
        json.dump(instance, f, indent=2)


if __name__ == "__main__":
    main()
