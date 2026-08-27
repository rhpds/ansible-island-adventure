# Module 03 — Explore the environment

### Brief Overview

This module introduces students to the pre-deployed Ansible Island Adventure environment. Rather than deploying from scratch, students tour the running architecture on OpenShift — CTFd, Gitea, AAP, Dev Spaces, managed nodes — and review the deployment artifacts that provisioned it. They examine the playbook structure, understand how stateful files (rosa.creds, player.creds, keys/) coordinate the deployment, and learn how to order the environment from RHDP for their own customer events.

### Audience and Time

- **Personas:** Solution Architects, TAMs, partner engineers
- **Prerequisites for this module:** Completion of Modules 1-2; working knowledge of Ansible (writing and running playbooks); familiarity with the OpenShift web console; access to the pre-deployed RHDP environment
- **Estimated duration:** 15 minutes

### Learning Objectives

- Navigate the pre-deployed Ansible Island Adventure environment on Red Hat OpenShift, identifying all architecture components and their roles in the CTF platform
- Analyze the deployment playbook structure to understand how roles (cluster_scale, players, managed_nodes, devspaces, ctfd, gitea, aap, verifier) provision the full environment
- Identify the stateful files (rosa.creds, player.creds, keys/) that coordinate deployment state and explain how the platform provides them to students

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Architecture tour on OpenShift | 5 min |
| 2 | Deployment artifacts walkthrough | 5 min |
| 3 | RHDP ordering and provisioning flow | 5 min |

### Detailed Steps

1. Log into the OpenShift console using the provided cluster-admin credentials and navigate to the project namespaces where AIA components are deployed
2. Identify the running workloads: CTFd scoring platform, Gitea source control, MariaDB, Redis, AAP controller, Dev Spaces, and managed node pods
3. Verify the OpenShift routes are accessible: open CTFd, Gitea, AAP console, and Dev Spaces URLs in the browser
4. Review the deployment playbook (`deploy.yml`): understand the pre_tasks (loading rosa.creds, logging into OpenShift, discovering the cluster apps domain) and the role execution order
5. Examine the role structure: cluster_scale → players → managed_nodes → devspaces → ctfd → gitea → aap → verifier
6. Open `rosa.creds` and understand how RHDP provides the ResourceClaim with cluster connection details, AWS credentials, and bastion access
7. Open `player.creds` and understand the cached credential model: passwords and verification tokens generated once and reused on subsequent runs
8. Review `keys/` (SSH keypair) and how it provides managed node access
9. Understand the RHDP ordering workflow: order the "Ansible Island Adventure" catalog item, receive a pre-deployed environment, and begin facilitation

### Key Takeaways

- The environment arrives fully deployed from RHDP — no manual installation is required for customer events
- The deployment playbook and roles are provided as artifacts so facilitators understand what was deployed and can customize it
- Three stateful files (rosa.creds, player.creds, keys/) bridge the platform provisioning and the deployment automation — the deployer loads cached credentials on re-runs rather than regenerating them
- Ordering from RHDP is the supported path for running customer-facing events

### Infrastructure Notes

- All infrastructure is pre-deployed by RHDP at environment provisioning time
- Students use cluster-admin credentials provided by the platform to explore the OpenShift console
- The deployment artifacts are available in the student's Dev Spaces workspace or bastion host
