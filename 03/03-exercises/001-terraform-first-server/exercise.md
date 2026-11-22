# Exercise 001 — Your First Server with Terraform
**Lesson:** 03 — Terraform + Ansible: Basic Cloud Workflow | **Level:** Beginner (start here)

---

## 🎯 Goal
Use **Terraform** — not Ansible, not the AWS Console — to create a real EC2 instance: an
SSH key pair, a security group, and the instance itself. Nothing gets *installed* on it in
this exercise — that's Ansible's job, next exercise. Here you're only building the box.

---

## ⚠️ Before you start
This creates a **real, billable** AWS resource (a `t3.micro` instance is cheap, but not
free forever). Keep it running until Exercise 002 is done with it — the teardown step is
at the end of *that* exercise, not this one.

---

## 📋 Instructions

### Step 1 — Look at the files
Open the `infra/` folder. Five small files, each with one job:
- `versions.tf` — which providers this project needs (aws, tls, http, local) and their versions
- `variables.tf` — things you might want to change (region, instance size...) without editing the resources themselves
- `network.tf` — reads your default VPC/subnet and your own public IP (used to lock SSH down to you)
- `key_pair.tf` — generates an SSH key pair and saves the private half as `basic-course-key.pem`
- `security_group.tf` — a firewall: SSH (22) only from your IP, HTTP (80) from anywhere
- `instance.tf` — the actual EC2 instance
- `outputs.tf` — what Terraform prints after it's done

### Step 2 — Initialize
```bash
cd .../ansible/courses/ansible/03/03-exercises/001-terraform-first-server/infra   # the prefix depends on where you placed the course
terraform init
```
This downloads the providers listed in `versions.tf`. Run it once per project folder.

### Step 3 — Preview before touching anything
```bash
terraform plan
```
This is the feature Ansible provisioning doesn't have: an exact, readable list of what
*would* change, computed against Terraform's own record of what already exists — **before**
anything actually happens. You should see `Plan: 5 to add, 0 to change, 0 to destroy.` — the
security group, the instance, and 3 resources for the key pair (`tls_private_key` generates
it, `aws_key_pair` registers it with AWS, `local_sensitive_file` saves the `.pem`).

### Step 4 — Apply
```bash
terraform apply
```
Type `yes` when prompted. Terraform figures out the order itself — the security group and
key pair before the instance that needs them — you never had to write that order down.

### Step 5 — Prove it's really just a blank box
```bash
ssh -i basic-course-key.pem ubuntu@$(terraform output -raw web_public_ip)
which nginx; which postgres   # should print nothing — nothing is installed yet
exit
```

### Step 6 — Run `plan` again (idempotency, Terraform's way)
```bash
terraform plan
```
You should see `No changes.` — Terraform compares the real world against its state file
(`terraform.tfstate`, created in Step 4) and finds nothing to do. Same idea as Ansible
idempotency from Lesson 02, but backed by an actual record of what it created, not just a
live re-check.

---

## ✅ Checklist
- [ ] `terraform plan` showed exactly what would be created, before anything happened
- [ ] `terraform apply` created one key pair, one security group, one instance
- [ ] You can SSH into the instance — and confirm nothing is installed on it yet
- [ ] A second `terraform plan` reports `No changes.`

---

## 💡 Hints
<details><summary>Hint 1 — "UnauthorizedOperation" or permission errors</summary>
Your IAM user needs EC2 permissions (RunInstances, CreateKeyPair, CreateSecurityGroup, DescribeX...). Check with whoever manages the AWS account.
</details>

<details><summary>Hint 2 — SSH "Connection refused" right after apply</summary>
The instance is still booting (cloud-init). `terraform apply` only waits for the instance to reach "running" in AWS's eyes, not for SSH inside it to be ready. Wait 30-60 seconds and retry.
</details>

<details><summary>Hint 3 — "No valid credential sources found"</summary>
Terraform's AWS provider reads credentials the same way the AWS CLI does. Run `aws sts get-caller-identity` first — if that fails, Terraform will too.
</details>
