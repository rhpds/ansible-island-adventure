# Ansible Island Adventure

## Overview

Ansible Island Adventure is a "teach the teacher" lab that enables Red Hatters to use, deliver, and customize gamified Capture the Flag (CTF) competitions around Red Hat Ansible Automation Platform for customers and partners. The lab is already built and proven with customers — this session teaches the delivery team how to facilitate events, customize challenges, and generate pipeline.

The environment arrives pre-deployed from the Red Hat Demo Platform (RHDP). Participants explore the architecture, play through the challenges as a participant would, modify challenge content using the idempotent Ansible deployer, and learn how to position the event for pipeline generation. By the end, they can independently order the platform from RHDP, facilitate a customer-facing CTF event, customize challenges for their audience, and convert engagement into qualified leads.

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
3. Configure challenge definitions, difficulty tiers, and content to tailor the event for specific customer use cases or partner engagements, and re-deploy changes using the idempotent Ansible playbook
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
| 1 | Welcome to the island | 15 min |
| 2 | Prerequisites and logistics | 10 min |
| 3 | Explore the environment | 15 min |
| 4 | Play the game | 45 min |
| 5 | Customize and extend | 20 min |
| 6 | From event to pipeline | 15 min |
| — | **Total hands-on** | **~65 min** |
| — | Intro / presentation | ~55 min |
| — | **Total lab** | **~2 hours** |

## Difficulty Level

Intermediate

## Environment

**Learner view:** A Red Hat OpenShift cluster provisioned via RHDP with the full Ansible Island Adventure environment pre-deployed — CTFd, Gitea, AAP, Dev Spaces, managed nodes, and per-player credentials are all ready at lab start. Students receive the deployment artifacts (`deploy.yml`, roles, `rosa.creds`, `player.creds`, `keys/`) so they can understand how the environment was provisioned, re-run the idempotent deployer safely, and modify challenges.

**Automation needed:** Yes (pre-deployed by platform)

- Ansible playbook to deploy CTFd, Gitea, AAP, Dev Spaces, managed nodes on OpenShift (run by RHDP at provisioning time)
- Automated per-player credential generation and PDF handout creation
- CTFd challenge upload and configuration
- Gitea repository setup with challenge source material
- Deployment artifacts provided to students for exploration, customization, and reuse in their own environments

## Infrastructure Requirements

- **Cloud provider:** AWS (ROSA open environment)
- **Cluster type:** Multinode
- **OCP version:** 4.20
- **Topology:** Per-student (each student gets their own ROSA open environment with AIA pre-deployed)
- **Sizing:** ROSA open environment defaults (control plane managed by ROSA)
- **Automation approach:** Ansible (operators installed from redhat-operators; CTFd stack deployed via Ansible playbook with k8s module — run by platform at provisioning time)
- **AI/MaaS:** None
- **External services:** registry.redhat.io (Red Hat operator images), github.com (rhpds/gitea-operator), docker.io (CTFd, MariaDB, Redis images)
- **AAP version:** 2.7 (stable-2.7 channel)
- **Non-GA products:** None (all products are GA)
