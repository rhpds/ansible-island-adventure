# Module 03 — Deploy the environment

### Brief Overview

This is the first hands-on module. Attendees deploy the full Ansible Island Adventure environment on a shared OpenShift cluster by running a single Ansible playbook. They review the architecture — CTFd, Gitea, MySQL, and Redis — understand how the playbook automates credential generation, challenge upload, and repository setup, and verify the deployment by confirming routes and logging into CTFd and Gitea.

### Audience and Time

- **Personas:** Solution Architects, TAMs, partner engineers
- **Prerequisites for this module:** Completion of Modules 1-2; working knowledge of Ansible (writing and running playbooks); familiarity with the OpenShift web console; access to a provisioned RHDP environment
- **Estimated duration:** 20 minutes

### Learning Objectives

- Deploy the Ansible Island Adventure environment on a Red Hat OpenShift cluster by running the provided Ansible playbook to produce a fully functional CTFd scoring platform, Gitea repositories, and per-player credentials
- Analyze the playbook structure to understand how credential generation, CTFd configuration, challenge upload, and Gitea repository setup are automated
- Verify the deployment by confirming OpenShift routes, logging into CTFd and Gitea, and validating player accounts

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Architecture walkthrough | 5 min |
| 2 | Run the deployment playbook | 8 min |
| 3 | Post-deploy verification | 7 min |

### Detailed Steps

1. Review the architecture diagram: CTFd scoring platform, Gitea source control, MySQL database, and Redis cache — all deployed as containers on OpenShift
2. Examine the deployment playbook structure before running it: note how it handles credential generation, CTFd configuration, challenge upload, and Gitea repository setup in a single automated workflow
3. Run `ansible-playbook deploy.yml` against the shared OpenShift cluster
4. Observe the provisioning workflow as it progresses: watch pods come up, configurations applied, and challenges loaded
5. After the playbook completes, confirm the OpenShift routes are created and accessible
6. Log into the CTFd scoring platform and verify the challenge categories and scoring are configured correctly
7. Log into Gitea and verify the challenge source repositories are populated
8. Verify that per-player accounts and credentials have been generated successfully
9. Review the generated PDF handouts that would be distributed to participants at a customer event

### Key Takeaways

- The entire Ansible Island Adventure environment deploys from a single Ansible playbook — no manual configuration required
- The playbook automates credential generation, CTFd challenge upload, Gitea repository setup, and PDF handout creation
- Post-deployment verification is a critical step to ensure the environment is ready before a customer event
- Understanding the playbook structure helps with troubleshooting and customization

### Infrastructure Notes

- Requires a Red Hat OpenShift cluster provisioned via the Red Hat Demo Platform
- The deployment playbook provisions CTFd, Gitea, MySQL, and Redis as containerized workloads on OpenShift
- All attendees deploy against a shared cluster during this module
- Deployment takes several minutes; the playbook output provides progress feedback
