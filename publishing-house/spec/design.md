# Ansible Island Adventure

## Overview

Ansible Island Adventure is a "teach the teacher" lab that enables Red Hatters to run gamified Capture the Flag (CTF) competitions around Red Hat Ansible Automation Platform for customers and partners. The lab is already built and proven with customers — this session teaches the delivery team how to deploy, run, and follow up on events independently.

Participants deploy the full Ansible Island Adventure environment on OpenShift, play through the challenges as a participant would, and learn how to position the event for pipeline generation. By the end, they can independently deploy the platform, facilitate a customer-facing CTF event, customize challenges for their audience, and convert engagement into qualified leads.

## Target Audience

- **Role:** Solution Architects, TAMs, partner engineers — anyone who delivers demos or workshops to customers
- **Experience level:** Intermediate
- **What they already know:** Basic Ansible concepts (playbooks, roles, inventories), some exposure to OpenShift (navigating the console, understanding routes and pods)
- **What they don't know:** How to deploy and operate the Ansible Island Adventure CTF platform, how to facilitate gamified customer events, how to use engagement data for pipeline generation

## Prerequisites

- Working knowledge of Ansible (writing and running playbooks)
- Familiarity with the OpenShift web console
- Access to the Red Hat Demo Platform to order environments
- No automated prerequisite validation — trust-based

## Learning Objectives

1. Deploy the Ansible Island Adventure environment on a Red Hat OpenShift cluster by running the provided Ansible playbook to produce a fully functional CTFd scoring platform, Gitea repositories, and per-player credentials
2. Demonstrate how to facilitate a customer-facing CTF event using the provided facilitation guidance, handout templates, and pacing recommendations for groups of varying size and technical background
3. Configure challenge definitions, difficulty tiers, and content to tailor the event for specific customer use cases or partner engagements
4. Analyze participant engagement metrics — challenge completion rates, time on platform, hint usage — and create a follow-up plan to convert attendees into qualified leads

## Content Type

Lab (hands-on)

## Products & Technologies

- Red Hat Ansible Automation Platform
- Red Hat OpenShift Container Platform
- CTFd (open-source CTF scoring platform)
- Gitea (open-source Git hosting)

## Module Map

| Module | Title | Duration |
|--------|-------|----------|
| 1 | Welcome to the island | 15 min |
| 2 | Prerequisites and logistics | 10 min |
| 3 | Deploy the environment | 20 min |
| 4 | Play the game | 45 min |
| 5 | From event to pipeline | 20 min |
| 6 | Wrap-up and next steps | 10 min |
| — | **Total hands-on** | **~65 min** |
| — | Intro / presentation | ~55 min |
| — | **Total lab** | **~2 hours** |

## Difficulty Level

Intermediate

## Environment

**Learner view:** A shared Red Hat OpenShift cluster provisioned via RHDP with nothing pre-deployed. Participants deploy the full environment themselves during Module 3, which provisions CTFd, Gitea, MySQL, and Redis via a single Ansible playbook. After deployment, each participant has their own player credentials and PDF handout.

**Automation needed:** Yes

- Ansible playbook to deploy CTFd, Gitea, MySQL, and Redis on OpenShift
- Automated per-player credential generation and PDF handout creation
- CTFd challenge upload and configuration
- Gitea repository setup with challenge source material

## Infrastructure Requirements

- **Cloud provider:** TBD — confirmed in infrastructure phase
- **Cluster type:** TBD — confirmed in infrastructure phase
- **OCP version:** TBD — confirmed in infrastructure phase
- **Topology:** TBD — confirmed in infrastructure phase
- **Sizing:** TBD — confirmed in infrastructure phase
- **Automation approach:** TBD — confirmed in infrastructure phase
- **AI/MaaS:** TBD — confirmed in infrastructure phase
- **External services:** TBD — confirmed in infrastructure phase
- **AAP version:** TBD — confirmed in infrastructure phase
- **Non-GA products:** TBD — confirmed in infrastructure phase
