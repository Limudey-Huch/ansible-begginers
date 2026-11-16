# Roadmap — Ansible Course
**Lesson duration:** 3 hours

---

| # | Topic | Main Content | Exercise |
|---|-------|---------------|-------|
| 1 | Introduction to Ansible & Architecture | What Configuration Management is and why it's needed, Agentless architecture (Control Node / Managed Nodes / SSH), Inventory files, basic YAML, running Ad-hoc commands | Installing Ansible, building an Inventory, running Ad-hoc commands against several machines |
| 2 | Playbooks & Practical Usage | Playbook structure (plays, tasks, modules), Variables, Handlers, running with `ansible-playbook`, brief intro to Roles, Idempotency | Writing a Playbook that installs and configures a full stack: nginx (frontend/reverse-proxy) + a backend service (e.g. Node.js/Python app) across several machines |
| 3 | Terraform + Ansible: Basic Cloud Workflow | Provisioning vs. configuration as two separate tools/jobs, Terraform basics (`init`/`plan`/`apply`/`destroy`, state file, resource dependencies), handing a Terraform-created IP to a static Ansible inventory, staged playbooks (update/install/configure/verify) against real EC2, a first look at SG-to-SG rules | Provision one, then two, real EC2 servers with Terraform; configure them with staged Ansible playbooks (nginx web tier, PostgreSQL db tier) |
| 4 | Ansible + AWS: Cloud Provisioning (Advanced) | Provisioning real EC2 instances *from Ansible itself* with `amazon.aws.ec2_instance`, SSH key pairs, Security Groups (incl. SG-to-SG rules across 3 tiers), dynamic inventory (`aws_ec2` plugin) vs static inventory, tag-based resource management & teardown | Provision a 3-tier stack on real AWS EC2 (nginx static frontend / Flask app server / Postgres DB) and deploy a live, self-contained aircraft-radar simulation end-to-end |

---

**Total:** 4 lessons | ~12 hours of study
