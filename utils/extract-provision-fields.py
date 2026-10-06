#!/usr/bin/env python3
"""Extract provision fields from a ResourceClaim YAML (provision-data.yaml).

Reads the ResourceClaim, locates all provision_data blocks across resources,
and outputs the fields required to provision this infrastructure.

Usage:
    python extract-provision-fields.py [input.yaml] [output.txt]

Defaults:
    input:  provision-data.yaml
    output: provision-fields.txt
"""

import sys
from pathlib import Path

import yaml

# The fields required by the CI provisioner, in order.
# label: human-readable name shown in output
# key:   provision_data field to extract
REQUIRED_FIELDS = [
    {"label": "OpenShift API Server URL",        "key": "openshift_api_server_url"},
    {"label": "OpenShift Cluster Ingress Domain", "key": "openshift_cluster_ingress_domain"},
    {"label": "OpenShift Cluster Common Password", "key": "openshift_cluster_admin_password"},
    {"label": "Keycloak Admin Username",          "key": "keycloak_admin_user"},
    {"label": "Keycloak Admin Password",          "key": "keycloak_admin_password"},
]


def extract_provision_data(claim):
    """Walk the ResourceClaim and collect all provision_data dicts."""
    merged = {}

    summary_pd = (claim.get("summary") or claim.get("status", {}).get("summary", {})).get("provision_data", {})
    if summary_pd:
        merged.update(summary_pd)

    for resource in claim.get("status", {}).get("resources", []):
        state = resource.get("state", {})
        vars_pd = state.get("spec", {}).get("vars", {}).get("provision_data", {})
        if vars_pd:
            merged.update(vars_pd)

    top_pd = claim.get("status", {}).get("summary", {}).get("provision_data", {})
    if top_pd:
        merged.update(top_pd)

    return merged


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("provision-data.yaml")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("provision-fields.txt")

    if not input_path.exists():
        print(f"ERROR: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    claim = yaml.safe_load(input_path.read_text())
    if not claim:
        print(f"ERROR: {input_path} is empty or invalid YAML", file=sys.stderr)
        sys.exit(1)

    provision_data = extract_provision_data(claim)
    if not provision_data:
        print(f"ERROR: No provision_data found in {input_path}", file=sys.stderr)
        sys.exit(1)

    guid = provision_data.get("guid", "unknown")
    max_label = max(len(f["label"]) for f in REQUIRED_FIELDS)

    lines = []
    lines.append(f"Provision fields for guid: {guid}")
    lines.append("")

    missing = []
    for field in REQUIRED_FIELDS:
        label = field["label"]
        key = field["key"]
        value = provision_data.get(key)
        if value is None:
            missing.append(key)
            lines.append(f"  {label:<{max_label}}  *** MISSING ***")
        else:
            lines.append(f"  {label:<{max_label}}  {value}")

    if missing:
        lines.append("")
        lines.append(f"WARNING: {len(missing)} required field(s) missing: {', '.join(missing)}")

    output = "\n".join(lines)
    output_path.write_text(output + "\n")
    print(output)
    print(f"\nWritten to {output_path}")


if __name__ == "__main__":
    main()
