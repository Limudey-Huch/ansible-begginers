# Exercise 003 — Three-Tier Provisioning
**Lesson:** 04 — Ansible + AWS: Cloud Provisioning (Advanced) | **Level:** Advanced (builds on 001-002)

---

## ⚠️ Before you start
Make sure Exercise 001's instance is torn down first (`cd ../001-first-ec2-instance && ansible-playbook teardown.yml`)
so you're not paying for 4 instances at once. This exercise provisions **3 new ones**.

---

## 🎯 Goal
Provision the full infrastructure for the radar app: a public **web** tier, a private **app**
tier, and a private **db** tier — each only reachable from the tier in front of it.

---

## 📋 Instructions

### Step 1 — Read the security group design
Open `provision_three_tier.yml` and find the three `ec2_security_group` tasks. Notice:
- `radar-web-sg` — SSH from you, HTTP (80) from the whole internet
- `radar-app-sg` — SSH from you, port 5000 **only from `radar-web-sg`** (not a CIDR!)
- `radar-db-sg` — SSH from you, port 5432 **only from `radar-app-sg`**

### Step 2 — Provision
```bash
cd ~/00_devops_course_iccp/ansible/courses/ansible/04/04-exercises/003-three-tier-provisioning
ansible-playbook provision_three_tier.yml
```

### Step 3 — Confirm the dynamic inventory sees all three
```bash
ansible-inventory -i inventory.aws_ec2.yml --graph
```
You should see `role_web`, `role_app`, and `role_db` groups, one instance each.

### Step 4 — Prove the isolation actually works
From your control node, try to reach the app tier's port directly — it should **fail**,
because your IP isn't in `radar-app-sg`'s allow-list (only `radar-web-sg` is):
```bash
APP_IP=$(ansible-inventory -i inventory.aws_ec2.yml --list | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['role_app']['hosts'][0])")
nc -zv -w3 $APP_IP 5000
```
This should time out / refuse — that's the SG doing its job. (It'll start answering once
Exercise 004 deploys the app there — don't worry if nothing's listening yet.)

### Step 5 — Tear down when done
```bash
cd ../001-first-ec2-instance
ansible-playbook teardown.yml
```
(The teardown playbook tears down **everything** tagged `Project: ansible-course-radar` —
that includes these 3 instances too, not just Exercise 001's.)

---

## ✅ Checklist
- [ ] Three instances running, tagged `web`/`app`/`db`
- [ ] `role_web`/`role_app`/`role_db` groups appear in the dynamic inventory
- [ ] Connecting directly to the app or db tier's service port from your own machine fails (not open to the world)
- [ ] You can explain, in your own words, why `group_name` is safer here than a CIDR range

---

## 💡 Hints
<details><summary>Hint 1 — this isn't full production isolation</summary>
All 3 instances here still get a **public IP** (default-VPC simplicity, to keep this lesson's AWS bill and setup low). In real production you'd put app/db in private subnets with *no* public IP at all, reachable only via a NAT gateway, bastion host, or AWS Systems Manager Session Manager. The security-group isolation you just built is one real layer of defense — not the only one you'd use.
</details>

<details><summary>Hint 2 — `group_name` rule not working</summary>
SG-to-SG rules only work within the same VPC. Since all three security groups here were created without specifying a VPC, they land in your account's **default VPC** together — if you ever specify a non-default `vpc_id`, make sure all three security groups use the *same* one.
</details>
