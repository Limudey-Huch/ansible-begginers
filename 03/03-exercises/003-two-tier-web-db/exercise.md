# Exercise 003 — Scale to Two Tiers: Web + Database
**Lesson:** 03 — Terraform + Ansible: Basic Cloud Workflow | **Level:** Intermediate (builds on 001-002)

---

## 🎯 Goal
Same two tools, same workflow as Exercises 001-002 — just more of each. Terraform provisions
**two** servers this time (web + db), with the db tier locked down so only the web tier can
reach it. Ansible then configures each one differently, in the same staged style as before,
split across **two plays** in one playbook.

---

## ⚠️ Before you start
This is a fresh, independent pair of servers — you don't need Exercise 001/002's instance
(it should already be destroyed). This creates **two real, billable** resources.

---

## 📋 Instructions

### Step 1 — Provision both servers
```bash
cd ~/00_devops_course_iccp/ansible/courses/ansible/03/03-exercises/003-two-tier-web-db/infra
terraform init
terraform plan    # Plan: 7 to add — 2 security groups, 2 instances, and 3 resources for the
                  # key pair (tls_private_key generates it, aws_key_pair registers it with AWS,
                  # local_sensitive_file saves the .pem)
terraform apply
```

### Step 2 — Look at the one new idea: SG-to-SG
Open `security_groups.tf`. The web tier's security group allows HTTP from anywhere
(`cidr_blocks`). The db tier's security group allows Postgres (5432) only
`security_groups = [aws_security_group.web.id]` — not an IP range, but **membership in
another security group**. Nothing outside the web tier can reach Postgres directly, even
with the right IP. (Lesson 04 builds a full 3-tier app around this same idea.)

### Step 3 — Fill in the inventory
```bash
cd ..
WEB_IP=$(cd infra && terraform output -raw web_public_ip)
DB_IP=$(cd infra && terraform output -raw db_public_ip)
DB_PRIVATE_IP=$(cd infra && terraform output -raw db_private_ip)
sed -i "s/REPLACE_WITH_WEB_IP/$WEB_IP/; s/REPLACE_WITH_DB_PRIVATE_IP/$DB_PRIVATE_IP/" inventory.ini
sed -i "s/REPLACE_WITH_DB_IP/$DB_IP/" inventory.ini
cat inventory.ini
```
Two groups, `[web]` and `[db]` — the same group syntax from Lesson 01, now pointing at two
different real servers.

### Step 4 — Read the playbook's two plays
Open `playbook.yml`. **Play 1** (`hosts: db`) runs first — installs PostgreSQL and creates an
application database/user. **Play 2** (`hosts: web`) runs second — installs nginx and deploys
a page that reads the db tier's private IP via `hostvars`. Order matters here for the same
reason it did in Lesson 02's multi-tier exercise: the web tier's page references the db tier,
so the db tier should be configured (or at least exist) first.

### Step 5 — Run it
```bash
ansible-playbook -i inventory.ini playbook.yml
```

### Step 6 — Verify each tier
```bash
echo "http://$(cd infra && terraform output -raw web_public_ip)/"   # open in a browser

ansible db -i inventory.ini -m shell -a "systemctl is-active postgresql" --become
ansible web -i inventory.ini -m shell -a "systemctl is-active nginx" --become
```
The web page should show the db tier's **private** IP — proving Ansible read one host's
variables (`hostvars[groups['db'][0]]`) while configuring a different host.

### Step 7 — Tear everything down
```bash
cd infra
terraform destroy
```
Type `yes`. Verify in the AWS Console that both instances are `terminated`.

---

## ✅ Checklist
- [ ] `terraform apply` created 2 instances, 2 security groups, 1 key pair
- [ ] `inventory.ini` has both real IPs, filled in from Terraform's outputs
- [ ] The db play ran before the web play
- [ ] The web page displays the db tier's private IP
- [ ] `systemctl is-active` confirms both services are running
- [ ] `terraform destroy` removed everything

---

## 💡 Hints
<details><summary>Hint 1 — "password authentication failed" / postgresql tasks fail</summary>
Check `apt` actually installed the <code>acl</code> package in the db play — without it,
<code>become_user: postgres</code> can fail to switch users cleanly on Ubuntu.
</details>

<details><summary>Hint 2 — web page shows a blank or wrong db IP</summary>
Check `inventory.ini`'s `[db]` line has `private_ip=` filled in correctly — that's a plain
inventory variable, not something Ansible invents on its own from a static file.
</details>

<details><summary>Hint 3 — "Connection timed out" SSHing to the db host</summary>
The db security group allows SSH (22) only from your own IP, same as the web tier — if your
IP changed since `terraform apply` (e.g. new wifi network), re-run `terraform apply` to pick
up the new `data.http.my_ip` value and update the rule.
</details>
