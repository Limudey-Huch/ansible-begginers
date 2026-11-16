# Lesson 03 — Terraform + Ansible: Basic Cloud Workflow
**Course:** Ansible | **Duration:** ~3 hours

---

## 🎯 Learning Objectives
Lessons 01-02 assumed the servers already existed. This lesson asks: where did they come
from? By the end, students will be able to:
- Explain the difference between *provisioning* (creating infrastructure) and *configuration*
  (installing/configuring software on infrastructure that already exists)
- Use Terraform to create a real EC2 instance: `init`, `plan`, `apply`, `destroy`
- Read a `terraform plan` preview and explain what it's comparing against
- Hand a Terraform-created server's IP to a static Ansible inventory and configure it in
  clear, ordered stages (update → install → configure → verify)
- Scale the same workflow to two servers with different roles, using groups and `hostvars`

---

## 📋 Lesson Content

### 1. Two Jobs, Two Tools
So far, Ansible's job has been **configuration**: given a server that already exists, install
packages, deploy files, start services. But the server itself had to come from somewhere —
in Lessons 01-02, that was a Docker container someone else set up for you.

**Provisioning** is the step before that: creating the server (and its networking, firewall
rules, storage) in the first place. This lesson uses two tools, kept deliberately separate:
- **Terraform** — builds the infrastructure (the EC2 instance, its security group, its SSH key)
- **Ansible** — configures what runs on top of it (installs nginx, deploys files, starts services)

This split is extremely common in real teams, and it's why this lesson keeps the two
completely separate: Terraform never installs software, Ansible never creates a server.
(Lesson 04 revisits this and shows Ansible *can* provision too — and why most teams still
prefer Terraform for that part.)

---

### 2. Terraform in Four Commands
```bash
terraform init      # download the providers this project needs (once per project)
terraform plan       # preview: what would change, computed against Terraform's own record
terraform apply       # actually make those changes (asks for confirmation first)
terraform destroy      # remove everything Terraform created, using that same record
```

**Key points:**
- That "record" is a **state file** (`terraform.tfstate`), written after every `apply` —
  it's how `plan` knows what already exists without re-scanning everything from scratch
- `plan` is the thing Ansible provisioning (Lesson 04) doesn't have: an exact diff, shown to
  you **before** anything happens
- `destroy` works from that same state file — no separate teardown script to maintain, unlike
  an Ansible-provisioned setup

---

### 3. A Minimal EC2 Resource
```hcl
resource "aws_security_group" "web" {
  name   = "basic-course-web-sg"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [local.my_ip]
  }
}

resource "aws_instance" "web" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.web.id]
}
```

**Key points:**
- `aws_instance.web` references `aws_security_group.web.id` — Terraform reads that reference
  and automatically creates the security group **first**. You never write the order yourself.
- `data "aws_vpc" "default"` and similar `data` blocks **read** existing AWS information
  (your default VPC) rather than creating anything
- Every value that might change (region, instance size) lives in `variables.tf`, not hardcoded
  inside the resource — the same instinct as using Ansible variables instead of literals

---

### 4. Handing Off to Ansible
Once `terraform apply` finishes, `terraform output` gives you the new server's IP:
```bash
IP=$(terraform output -raw web_public_ip)
```
From here, it's Lesson 01/02 all over again — a static `inventory.ini` with a `[web]` group,
and a playbook that runs in clear stages:
```yaml
tasks:
  - name: Update apt cache          # stage 1
    ansible.builtin.apt: {update_cache: true}
  - name: Install nginx             # stage 2
    ansible.builtin.apt: {name: nginx, state: present}
  - name: Deploy the page           # stage 3
    ansible.builtin.template: {src: index.html.j2, dest: /var/www/html/index.html}
    notify: Restart nginx
  - name: Ensure nginx is running   # stage 4
    ansible.builtin.service: {name: nginx, state: started, enabled: true}
```

**Key points:**
- Nothing here is new — it's the exact same `apt`/`template`/`service`/handler pattern from
  Lesson 02, just pointed at a real cloud IP instead of a local container
- Idempotency still works the same way: re-running the playbook only changes what's actually
  different (Terraform's idempotency, via its state file, is a separate, earlier layer)

---

### 5. Scaling to Two Tiers
Adding a second server (a db tier) means: one more `aws_instance` block in Terraform, one
more `[db]` group in the inventory, one more play in the playbook. Nothing conceptually new —
just more of the same pattern, which is the point.

```yaml
- hosts: db
  tasks: [... install PostgreSQL ...]

- hosts: web
  tasks: [... install nginx, template a page that reads {{ hostvars[groups['db'][0]]['private_ip'] }} ...]
```

**Key points:**
- Play order matters: the db play runs first because the web tier's page references it —
  same reasoning as Lesson 02's backend-before-frontend multi-tier exercise
- `hostvars[groups['db'][0]]` reads a variable that belongs to a **different** host in the
  same inventory — useful any time one tier needs to know about another
- The db tier's security group allows traffic on its port **only from the web tier's security
  group**, not from any IP range — a first, simple look at SG-to-SG rules (Lesson 04 goes
  much further with this, across three tiers and dynamic inventory)

---

### 6. Always Tear Down
Every exercise here creates **real, billable** AWS resources. `terraform destroy` removes
everything a project created, read from its own state file — run it as the last step of
every exercise, every time, before moving on.

---

## 🔗 Links & Resources
- [Terraform AWS provider docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform CLI: init/plan/apply/destroy](https://developer.hashicorp.com/terraform/cli/commands)
- [Ubuntu AMI locator](https://cloud-images.ubuntu.com/locator/ec2/) (if the course's pinned AMI ID goes stale)

---

## 📝 Instructor Notes
- Keep the Terraform/Ansible boundary sharp in this lesson — "Terraform never installs
  software, Ansible never creates a server." Lesson 04 is where that boundary gets
  deliberately blurred (Ansible provisioning), so students need the clean version first.
- `terraform plan`'s preview is worth dwelling on — it's the single clearest "why would I
  reach for a dedicated provisioning tool" answer available at this point in the course.
- Say the cost warning out loud, more than once, same as every other AWS-touching lesson.
- This lesson is intentionally simpler than Lesson 04: no dynamic inventory, no 3-tier app,
  no live-moving demo. Students who want that depth move on to Lesson 04 afterward.
