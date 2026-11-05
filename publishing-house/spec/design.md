# Ansible Island Adventure

## Overview

Ansible Island Adventure is a "teach the teacher" lab that enables Red Hatters to use, deliver, and customize gamified Capture the Flag (CTF) competitions around Red Hat Ansible Automation Platform for customers and partners. The lab is already built and proven with customers — this session teaches the delivery team how to facilitate events, customize challenges, and generate pipeline.

The environment and event content are prepared before training using the Red Hat Demo Platform (RHDP) catalog items and organizer post-deploy. Learners play as participants first, then explore architecture and instructor administration, demonstrate a personal-board reset, customize content with a progress-preserving update, and discuss pipeline generation using saved gameplay results.

## Target Audience

- **Role:** Solution Architects, TAMs, partner engineers — anyone who delivers demos or workshops to customers
- **Experience level:** Intermediate
- **What they already know:** Basic Ansible concepts (playbooks, roles, inventories), some exposure to OpenShift (navigating the console, understanding routes and pods)
- **What they don't know:** How to deploy and operate the Ansible Island Adventure CTF platform, how to facilitate gamified customer events, how to use engagement data for pipeline generation

## Prerequisites

- Working knowledge of Ansible (writing and running playbooks)
- Familiarity with the OpenShift web console
- Access to the Red Hat Demo Platform (environment is pre-deployed; no manual installation required)
- No automated prerequisite validation — trust-based

## Learning Objectives

1. Navigate the pre-deployed Ansible Island Adventure environment on Red Hat OpenShift, identifying the architecture components (CTFd, Gitea, MariaDB, Redis, AAP, Dev Spaces) and understanding the deployment artifacts that provisioned them
2. Demonstrate how to facilitate a customer-facing CTF event using the provided facilitation guidance, handout templates, and pacing recommendations for groups of varying size and technical background
3. Configure challenge definitions, difficulty tiers, and content for customer use cases, applying progress-preserving updates and distinguishing them from board resets
4. Analyze participant engagement metrics — challenge completion rates, time on platform, hint usage — and create a follow-up plan to convert attendees into qualified leads

## Content Type

Lab (hands-on)

## Products & Technologies

- Red Hat Ansible Automation Platform 2.7
- Red Hat OpenShift Container Platform
- Red Hat OpenShift Dev Spaces
- CTFd (open-source CTF scoring platform)
- Gitea (open-source Git hosting, via rhpds/gitea-operator)
- MariaDB
- Redis

## Module Map

| Module | Title | Duration |
|--------|-------|----------|
| 1 | Welcome to the island | 10 min |
| 2 | Prerequisites and logistics | 10 min |
| 3 | Play the game | 50 min |
| 4 | Explore the environment | 20 min |
| 5 | Customize and extend | 20 min |
| 6 | From event to pipeline | 10 min |
| — | **Total lab** | **~2 hours** |

Module 3 includes 10 minutes access/workspace setup, 35 minutes scored play including Warm Up, and 5 minutes debrief and recording results. Module 4 includes instructor CLI/vault setup and a deliberate reset after the practice round. Re-solve one Warm Up challenge for Module 5's content-update preservation check. Use the saved Module 3 observations in Module 6 because the reset clears original gameplay progress.

Customer events follow the Showroom schedule of **1–1.5 hours**: welcome and access setup, **one 30–45-minute scoring window including Warm Up with a strict 45-minute limit**, and wrap-up. Optional extended networking/debrief is additional. Provisioning and organizer post-deploy are completed before learners arrive, outside both session clocks.

## Difficulty Level

Intermediate

## Environment

**Learner view:** The leaderboard CI provides shared OpenShift services; linked student CIs provide personal identities, CTFd instances, and separately provisioned managed VMs. Learners use the CTFd player account and survival kit first. Later they open their `aia-instructor` repository, authenticate with their personal OpenShift identity, and create a local vault-password file with the lab password. Root `deploy.yml` resets personal board progress; `update-challenges.yml` updates content while retaining solves. Neither recreates the catalog infrastructure. Organizer administrator credentials remain private.

**Automation needed:** Yes (pre-deployed by platform)

- The leaderboard and linked student catalog items provision shared services and per-instructor resources; the organizer completes post-deploy before the session
- Per-instructor credential handouts published via `set_stats` for Showroom display
- CTFd challenge archive build and import with vault-encrypted flags
- Gitea repository setup with challenge source material
- RHEL9 VMs provisioned via OpenShift Virtualization with cloud-init (SSH-accessible managed nodes for Ansible challenges)

## Assessment Strategy

- **Modules 1–2 (Welcome, Prerequisites):** Trust-based — presentation and discussion, no automated validation
- **Module 3 (Play the game):** Player flag submissions and saved score/challenge observations from the time-boxed round
- **Module 4 (Explore the environment):** Personal identity/vault checks, reset preview, cleared progress with retained accounts/infrastructure, and one new Warm Up solve
- **Module 5 (Customize and extend):** Edited challenge appears after `update-challenges.yml`; the unchanged Warm Up solve remains
- **Module 6 (From event to pipeline):** Discussion and planning using saved Module 3 results; customer-event results are retained before any reset

## Infrastructure Requirements

- **Cloud provider:** CNV (OpenShift Virtualization)
- **Cluster type:** Multinode — 5 workers (64 vCPU, 128Gi RAM each)
- **OCP version:** 4.21
- **Topology:** Shared-cluster (all instructors share one cluster; per-instructor namespaces for isolation)
- **Per-instructor VM:** 1 RHEL9 VM (1 vCPU, 2Gi guest, 30Gi disk) — Ansible managed node for CTF challenges, provisioned via OpenShift Virtualization
- **Shared services:** AAP 2.7 (Gateway + Controller, per-instructor organizations), Gitea, Dev Spaces, CTFd (per-instructor instances)
- **Capacity:** ~140 instructors per cluster with 25% headroom; see `deploy/CAPACITY.md` for sizing details
- **Automation approach:** Ansible (operators installed from redhat-operators; all services deployed via Ansible playbook with kubernetes.core — run by platform at provisioning time)
- **AI/MaaS:** None
- **External services:** registry.redhat.io (operator images), registry.access.redhat.com (RHEL VM images), github.com (ansible-survival-kit repo), docker.io (CTFd, MariaDB, Redis), quay.io (verifier image)
- **AAP version:** 2.7 (stable-2.7 channel, AnsibleAutomationPlatform CR with Gateway)
- **Non-GA products:** None (all products are GA)
