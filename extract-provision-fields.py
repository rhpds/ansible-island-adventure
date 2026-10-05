#!/usr/bin/env python3
"""Extract provision fields from a ResourceClaim YAML (provision-data.yaml).

Reads the ResourceClaim, locates all provision_data blocks across resources,
and writes a flat, ordered summary to provision-fields.txt.

Usage:
    python extract-provision-fields.py [input.yaml] [output.txt]

Defaults:
    input:  provision-data.yaml
    output: provision-fields.txt
"""

import sys
from collections import OrderedDict
from pathlib import Path

import yaml


# Fields grouped by purpose, in the order they're typically needed.
# The CI provisioner should consume them in this order.
FIELD_GROUPS = OrderedDict([
    ("Cluster Access", [
        "openshift_api_server_url",
        "openshift_api_url",
        "openshift_console_url",
        "openshift_cluster_console_url",
        "openshift_cluster_ingress_domain",
        "openshift_client_download_url",
    ]),
    ("Cluster Auth (use these, NOT kubeadmin)", [
        "openshift_cluster_admin_username",
        "openshift_cluster_admin_password",
        "openshift_cluster_admin_token",
    ]),
    ("Kubeadmin (DO NOT USE with Keycloak clusters)", [
        "openshift_kubeadmin_password",
    ]),
    ("Keycloak / SSO", [
        "keycloak_admin_console",
        "keycloak_admin_user",
        "keycloak_admin_password",
    ]),
    ("Bastion / SSH", [
        "bastion_public_hostname",
        "bastion_ssh_user_name",
        "bastion_ssh_password",
        "bastion_ssh_port",
    ]),
    ("AAP (Ansible Automation Platform)", [
        "aap_controller_web_url",
        "aap_controller_admin_user",
        "aap_controller_admin_password",
    ]),
    ("Gitea", [
        "gitea_console_url",
        "gitea_admin_username",
        "gitea_admin_password",
        "gitea_user",
        "gitea_password",
    ]),
    ("Dev Spaces", [
        "devspaces_url",
    ]),
    ("Sandbox (CNV host cluster)", [
        "sandbox_openshift_api_url",
        "sandbox_openshift_apps_domain",
        "sandbox_openshift_cluster",
        "sandbox_openshift_console_url",
        "sandbox_openshift_namespace",
        "sandbox_openshift_api_key",
    ]),
    ("Identity", [
        "guid",
        "cloud_provider",
    ]),
])

# Fields to redact in output (show first/last 8 chars only)
REDACT_FIELDS = {
    "openshift_cluster_admin_token",
    "sandbox_openshift_api_key",
    "openshift_api_key",
}

# Fields with long multi-line values to skip entirely
SKIP_FIELDS = {
    "openshift_api_ca_cert",
    "odf_external_config",
}


def redact(value, field_name):
    """Redact long tokens to first/last 8 chars."""
    s = str(value)
    if field_name in REDACT_FIELDS and len(s) > 24:
        return f"{s[:8]}...{s[-8:]}"
    return s


def extract_provision_data(claim):
    """Walk the ResourceClaim and collect all provision_data dicts."""
    merged = {}

    # summary.provision_data (top-level shortcut)
    summary_pd = (claim.get("summary") or claim.get("status", {}).get("summary", {})).get("provision_data", {})
    if summary_pd:
        merged.update(summary_pd)

    # Per-resource provision_data (nested in status.resources[].state.spec.vars)
    for resource in claim.get("status", {}).get("resources", []):
        state = resource.get("state", {})
        # provision_data in spec.vars
        vars_pd = state.get("spec", {}).get("vars", {}).get("provision_data", {})
        if vars_pd:
            merged.update(vars_pd)
        # provision_data at resource level
        res_pd = resource.get("provision_data", {})
        if res_pd:
            merged.update(res_pd)

    # Also check summary.provision_data at top level
    top_pd = claim.get("status", {}).get("summary", {}).get("provision_data", {})
    if top_pd:
        merged.update(top_pd)

    return merged


def format_output(provision_data, guid):
    """Format provision fields into grouped, ordered text."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  PROVISION FIELDS — guid: {guid}")
    lines.append("=" * 70)
    lines.append("")

    seen = set()

    for group_name, fields in FIELD_GROUPS.items():
        group_lines = []
        for field in fields:
            if field in provision_data and field not in SKIP_FIELDS:
                val = redact(provision_data[field], field)
                group_lines.append(f"  {field}: {val}")
                seen.add(field)

        if group_lines:
            lines.append(f"── {group_name} {'─' * max(1, 54 - len(group_name))}")
            lines.extend(group_lines)
            lines.append("")

    # Warn about kubeadmin vs cluster-admin mismatch
    kubeadmin = provision_data.get("openshift_kubeadmin_password", "")
    cluster_admin = provision_data.get("openshift_cluster_admin_password", "")
    keycloak = provision_data.get("keycloak_admin_console", "")

    if keycloak and kubeadmin and cluster_admin and kubeadmin != cluster_admin:
        lines.append("── ⚠️  WARNING ─────────────────────────────────────────")
        lines.append("  This cluster uses Keycloak SSO authentication.")
        lines.append(f"  kubeadmin password:      {kubeadmin}")
        lines.append(f"  cluster admin password:  {cluster_admin}")
        lines.append("  These are DIFFERENT. Use openshift_cluster_admin_password")
        lines.append("  for oc login, NOT openshift_kubeadmin_password.")
        lines.append("")

    # Remaining fields not in any group
    remaining = {k: v for k, v in provision_data.items()
                 if k not in seen and k not in SKIP_FIELDS}
    if remaining:
        lines.append(f"── Other Fields {'─' * 39}")
        for k in sorted(remaining):
            val = redact(remaining[k], k)
            # Skip nested dicts/lists (user lists, etc.)
            if isinstance(provision_data[k], (dict, list)):
                val = f"<{type(provision_data[k]).__name__} with {len(provision_data[k])} entries>"
            lines.append(f"  {k}: {val}")
        lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)


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

    guid = provision_data.get("guid", claim.get("status", {}).get("resourceHandle", {}).get("name", "unknown"))
    output = format_output(provision_data, guid)

    output_path.write_text(output + "\n")
    print(output)
    print(f"\nWritten to {output_path}")


if __name__ == "__main__":
    main()
