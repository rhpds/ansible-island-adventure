# Ansible Island Adventure

A "teach the teacher" lab that enables Red Hatters to deploy, facilitate, and customize
gamified Capture the Flag (CTF) competitions built on Red Hat Ansible Automation Platform.

Instructors receive a fully deployed environment — CTFd scoring platform, Gitea source
control, AAP controller, Dev Spaces IDE, and RHEL managed nodes — and learn how to
run customer-facing events, modify challenges, and generate pipeline.

## Quick Start

### Prerequisites

- `oc` CLI
- `ansible-core` with collections: `kubernetes.core`, `community.general`
- Python packages: `kubernetes`, `passlib`, `pyyaml`
- A provisioned RHDP leaderboard environment (`.leaderboard.env`)

```bash
pip install kubernetes passlib pyyaml
ansible-galaxy collection install kubernetes.core community.general
```

### Deploy the Leaderboard

The leaderboard deploys all cluster services (AAP orgs, CTFd instances, Gitea, Dev Spaces)
onto a pre-provisioned OpenShift cluster with AAP and Dev Spaces already installed.

1. Place the ResourceClaim YAML from your RHDP catalog item into `.leaderboard.env`
   at the repo root.

2. Create a vault password for encrypting challenge flags:
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))" > .vault-password
   ```

3. Deploy:
   ```bash
   ansible-playbook ansible-testing/deploy_leaderboard.yml \
     -e "aia_leaderboard_env=$(pwd)/.leaderboard.env" \
     -e aia_instructor_count=4
   ```

   Or pass a manifest if AAP isn't pre-licensed:
   ```bash
   ansible-playbook ansible-testing/deploy_leaderboard.yml \
     -e "aia_leaderboard_env=$(pwd)/.leaderboard.env" \
     -e aia_aap_manifest_path=/path/to/manifest.zip \
     -e aia_instructor_count=4
   ```

After deploy, each instructor gets:
- Their own CTFd instance with 26 challenges
- A Gitea account with the `ansible-challenge` repo
- An AAP organization (Org Admin)
- Dev Spaces access
- Personalized credentials printed to the console and published via `set_stats`

## Architecture

```
rhpds.aia collection (collections/ansible_collections/rhpds/aia/)
├── deploy_leaderboard    Cluster services (CTFd, Gitea, AAP orgs, Dev Spaces validation)
└── deploy_vms            VM provisioning + AAP inventory config (separate cluster)
```

The deployment is split into two roles designed to run on separate infrastructure:

| Role | What it deploys | Cluster |
|------|----------------|---------|
| `rhpds.aia.deploy_leaderboard` | AAP orgs, CTFd (per instructor), Gitea, Dev Spaces | Leaderboard cluster (AAP + Dev Spaces pre-installed) |
| `rhpds.aia.deploy_vms` | RHEL VMs via OpenShift Virtualization, AAP inventory/credentials | VM cluster (CNV-enabled) |

The VM role accepts `aia_aap_url` and `aia_aap_admin_password` as inputs so it can
register VMs back into the leaderboard's AAP instance.

## Using as a Collection

The roles can be included directly in your own playbooks:

```yaml
- hosts: localhost
  roles:
    - role: rhpds.aia.deploy_leaderboard
      vars:
        aia_leaderboard_env: /path/to/.leaderboard.env
        aia_instructor_count: 10
```

Set `collections_path` in your `ansible.cfg` to point at the `collections/` directory,
or install the collection to `~/.ansible/collections`.

## Configuration

All defaults are in `collections/ansible_collections/rhpds/aia/roles/deploy_leaderboard/defaults/main.yml`.

| Variable | Default | Description |
|----------|---------|-------------|
| `aia_leaderboard_env` | `""` | Path to ResourceClaim YAML (required) |
| `aia_instructor_count` | `4` | Number of instructors to create |
| `aia_instructors` | `[]` | Explicit instructor list (overrides count) |
| `aia_aap_manifest_path` | `""` | AAP manifest ZIP (if license not pre-applied) |
| `aia_ctfd_admin_password` | `supersecret123!` | CTFd admin password |
| `aia_gitea_admin_password` | `supersecret123!` | Gitea admin password |
| `aia_vm_ssh_user` | `student` | SSH user created on managed node VMs |

## Challenge Flags

Challenge flag values are vault-encrypted in `ansible-testing/vars/flags.yml`.
The vault password is in `.vault-password` (gitignored).

To edit flags:
```bash
ansible-vault edit ansible-testing/vars/flags.yml
```

Challenge definitions (descriptions, hints, categories) are plaintext in
`ansible-testing/vars/challenges.yml` and reference flags via `{{ ctfd_flags.<key> }}`.

## Capacity Planning

See [ansible-testing/CAPACITY.md](ansible-testing/CAPACITY.md) for production sizing.
A 5-worker cluster (64 vCPU / 128Gi each) supports ~140 instructors with 25% headroom.

## Repository Structure

```
.
├── ansible.cfg                        Ansible config (vault password, collections path)
├── collections/
│   └── ansible_collections/rhpds/aia/ The rhpds.aia Ansible collection
│       ├── galaxy.yml
│       └── roles/
│           ├── deploy_leaderboard/    Cluster services role
│           └── deploy_vms/            VM provisioning role (stub)
├── ansible-testing/                   Test playbooks and legacy roles
│   ├── deploy_leaderboard.yml         Test entrypoint for leaderboard deploy
│   ├── vars/
│   │   ├── flags.yml                  Challenge flags (vault-encrypted)
│   │   └── challenges.yml             Challenge definitions
│   ├── CAPACITY.md                    Production sizing guide
│   └── roles/                         Legacy pre-collection roles (reference only)
├── publishing-house/                  RHDP Publishing House spec and design docs
└── content/                           Showroom lab content (AsciiDoc)
```

## Publishing House

This project is managed through the [RHDP Publishing House](https://central-api-publishing-house.apps.ocpv-infra02.wdc07.infra.demo.redhat.com)
pipeline. Run `/rhdp-publishing-house` in Claude to check project status.
