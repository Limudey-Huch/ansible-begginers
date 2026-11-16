# Course — Ansible
**Roadmap:** [roadmap_ansible.md](roadmap_ansible.md)

---

## Lessons

| # | Topic | Lesson | Test | Exercises |
|---|-------|--------|------|-----------|
| 1 | Introduction to Ansible & Architecture | [01/01-lesson_intro-architecture.md](01/01-lesson_intro-architecture.md) | [01/01-test_intro-architecture.md](01/01-test_intro-architecture.md) | [01/01-exercises/](01/01-exercises/) |
| 2 | Playbooks & Practical Usage | [02/02-lesson_playbooks.md](02/02-lesson_playbooks.md) | [02/02-test_playbooks.md](02/02-test_playbooks.md) | [02/02-exercises/](02/02-exercises/) |
| 3 | Terraform + Ansible: Basic Cloud Workflow | [03/03-lesson_terraform-ansible-cloud.md](03/03-lesson_terraform-ansible-cloud.md) | [03/03-test_terraform-ansible-cloud.md](03/03-test_terraform-ansible-cloud.md) | [03/03-exercises/](03/03-exercises/) |
| 4 | Ansible + AWS: Cloud Provisioning (Advanced) | [04/04-lesson_aws-provisioning.md](04/04-lesson_aws-provisioning.md) | [04/04-test_aws-provisioning.md](04/04-test_aws-provisioning.md) | [04/04-exercises/](04/04-exercises/) |

## Practice Environments
**Lessons 1-2:** [lab-environment/SETUP.md](lab-environment/SETUP.md) — 3 lightweight Docker
containers (SSH + systemd) standing in for real managed servers, meant to run on an
instructor/lab Ubuntu Server VM (Ansible itself installed on that same VM as the Control
Node). No per-student VMs or cloud account needed. The starter inventory files in
`01-exercises/` and `02-exercises/` already match this environment's IPs out of the box.

**Lessons 3-4:** Real AWS (EC2, Security Groups, Terraform, a Postgres DB) — needs an AWS
account with CLI credentials configured on the control node. **Creates real, billable
resources** — every exercise folder's teardown step (`terraform destroy` in Lesson 3,
`ansible-playbook teardown.yml` in Lesson 4) must be run when done; see
[03-lesson_terraform-ansible-cloud.md](03/03-lesson_terraform-ansible-cloud.md) and
[04-lesson_aws-provisioning.md](04/04-lesson_aws-provisioning.md) for the cost warnings and
tagging conventions that make safe cleanup possible.

## Presentation
One combined deck covers both lessons: [01-presentation_ansible-overview.pptx](01-presentation_ansible-overview.pptx)
(Part 1 = Lesson 1 concepts/architecture, Part 2 = Lesson 2 playbooks/practical use.)

## Exercise Structure
Each lesson's exercises live in a numbered subfolder, ordered from simplest to most advanced:

```
01/01-exercises/
  001-install-and-verify/
  002-inventory-and-ping/
  003-adhoc-commands/
  004-groups-targeting/

02/02-exercises/
  001-first-playbook/
  002-variables-and-tasks/
  003-handlers/
  004-multitier-stack/

03/03-exercises/
  001-terraform-first-server/
  002-configure-with-ansible/
  003-two-tier-web-db/

04/04-exercises/
  001-first-ec2-instance/
  002-dynamic-inventory/
  003-three-tier-provisioning/
  004-deploy-radar-app/        (capstone — live aircraft radar simulation on real AWS infra)
```

Each exercise folder contains `exercise.md` plus any starter files (inventory/playbook) already filled in and ready to run.

## Instructor Notes
- Lesson 1 builds the mental model (what problem Ansible solves, pros/cons, architecture) before any hands-on playbook work.
- Lesson 2's exercises build progressively to a capstone multi-tier (frontend + backend) deployment, tying together variables, handlers, and groups from Lesson 1.
- Lesson 3 moves from the local Docker lab to real cloud infrastructure, but keeps the two tools' jobs cleanly separate: Terraform provisions, Ansible configures, staged just like Lesson 2's playbooks. This is the gentler on-ramp — no dynamic inventory, no 3-tier app.
- Lesson 4 goes deeper on the AWS/Ansible side specifically — provisioning *from* Ansible, dynamic inventory, and SG-to-SG design across 3 tiers — culminating in a genuinely working live app (a self-contained moving aircraft simulation) across 3 real EC2 instances. Repeat the cost/teardown warning often in both lessons.
