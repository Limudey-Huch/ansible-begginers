# Test — Terraform + Ansible: Basic Cloud Workflow
**Course:** Ansible | **Lesson:** 03

---

## Part A — Multiple Choice

**1. In this lesson's workflow, which tool creates the EC2 instance itself?**
- a. Ansible, using `amazon.aws.ec2_instance`
- b. Terraform ✓
- c. Either one, chosen at random
- d. Neither — the AWS Console

**2. What does `terraform plan` do?**
- a. Applies the changes immediately
- b. Shows exactly what would change, compared against Terraform's state file, before anything happens ✓
- c. Deletes all resources
- d. Validates AWS credentials only

**3. Why does `aws_instance.web` referencing `aws_security_group.web.id` matter?**
- a. It doesn't — Terraform creates resources in file order
- b. Terraform uses that reference to know the security group must be created first ✓
- c. It's only for documentation
- d. It forces the two resources into the same file

**4. What does `terraform destroy` use to know what to remove?**
- a. A fresh scan of the whole AWS account
- b. Its own state file, recording exactly what it created ✓
- c. The resource names, guessed from the `.tf` files
- d. Nothing — it asks AWS to list everything tagged `Project`

**5. In the two-tier exercise, why does the db play run before the web play?**
- a. Alphabetical order in the YAML file
- b. The web tier's deployed page reads a variable from the db host via `hostvars` ✓
- c. Ansible always runs the shortest play first
- d. PostgreSQL must be installed before nginx, with no other reason

**6. What does an SG-to-SG rule (`security_groups = [aws_security_group.web.id]`) allow that a CIDR rule doesn't?**
- a. Nothing — they're equivalent
- b. Traffic only from instances that belong to a specific security group, regardless of their IP ✓
- c. Traffic from a wider IP range
- d. HTTPS instead of HTTP

---

## Part B — Open Questions

**1.** Explain, in your own words, why this lesson keeps Terraform and Ansible's jobs
strictly separate (Terraform never installs software; Ansible never creates a server).
_Answer space:_

**2.** A classmate says "idempotency is idempotency — Terraform's and Ansible's work the
same way." Do you agree? What's actually different about how each one checks "has this
already been done"?
_Answer space:_

**3.** You add a *third* server (an app tier) to the two-tier exercise. List, in order, every
file you'd need to touch — in `infra/`, in the inventory, and in the playbook — to make it work.
_Answer space:_

---

## Part C — Practical Task

Extend `003-two-tier-web-db`'s `infra/` with a **third** instance, `aws_instance.cache`,
in its own security group that allows port `6379` (Redis) only from the web tier's security
group — not from any CIDR range.

**Success criteria:**
- [ ] A new `aws_security_group.cache` resource, referencing `aws_security_group.web.id` in its ingress rule (not a `cidr_blocks` range)
- [ ] A new `aws_instance.cache` resource, tagged with the same `Project` value and `Role = "cache"`
- [ ] `terraform plan` shows exactly 2 resources to add — nothing about the existing web/db resources changes
- [ ] A new `outputs.tf` entry for the cache instance's IP
