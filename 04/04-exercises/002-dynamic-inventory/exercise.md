# Exercise 002 — Dynamic Inventory
**Lesson:** 04 — Ansible + AWS: Cloud Provisioning (Advanced) | **Level:** Advanced (builds on 001)

---

## 🎯 Goal
Stop hand-writing IPs into an `inventory.ini`. Instead, let Ansible ask AWS directly, every
time, "what instances exist right now?" — using the instance from Exercise 001.

---

## 📋 Instructions

### Step 0 — Make sure Exercise 001's instance is running
```bash
cd ../001-first-ec2-instance
ansible-playbook provision.yml   # idempotent — does nothing if it's already up
cd ../002-dynamic-inventory
```

### Step 1 — Look at the dynamic inventory file
`inventory.aws_ec2.yml` is already provided. The filename matters — Ansible recognizes the
`aws_ec2` plugin by the file *ending in* `aws_ec2.yml`.

### Step 2 — See what Ansible discovers
```bash
ansible-inventory -i inventory.aws_ec2.yml --graph
```
You should see a `role_lab` group (auto-created from the `Role: lab` tag) containing your instance.

### Step 3 — Ping it through the dynamic inventory
```bash
ansible role_lab -i inventory.aws_ec2.yml -m ping
```

### Step 4 — Prove it's actually dynamic
```bash
cd ../001-first-ec2-instance
ansible-playbook teardown.yml
ansible-playbook provision.yml
cd ../002-dynamic-inventory
ansible-inventory -i inventory.aws_ec2.yml --graph
```
The instance now has a **different public IP** (new instance, same tags) — yet the exact same
`ansible role_lab -i inventory.aws_ec2.yml -m ping` command from Step 3 still works, with zero
changes to any inventory file. A static `inventory.ini` would have gone stale the moment you
tore the old instance down.

---

## ✅ Checklist
- [ ] `--graph` shows a `role_lab` group built automatically from the `Role` tag
- [ ] `ansible role_lab -m ping` succeeds using the dynamic inventory
- [ ] After destroying and recreating the instance (new IP), the same command still works unmodified

---

## 💡 Hints
<details><summary>Hint 1 — empty inventory / no hosts found</summary>
Check the instance is actually `running` (not `stopped`/`terminated`) and tagged exactly `Project: ansible-course-radar` — the `filters:` block in the inventory file must match.
</details>

<details><summary>Hint 2 — "failed to connect" but the host shows up</summary>
Check `compose:` in `inventory.aws_ec2.yml` — it sets `ansible_host` to the **public** IP and points `ansible_ssh_private_key_file` at Exercise 001's `.pem`. If you moved that file, update the path.
</details>
