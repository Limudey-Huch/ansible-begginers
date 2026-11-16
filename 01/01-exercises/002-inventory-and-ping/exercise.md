# Exercise 002 — Build an Inventory & Ping Your Hosts
**Lesson:** 01 — Introduction to Ansible & Architecture | **Level:** Beginner (builds on 001)

---

## 🎯 Goal
Create your first inventory file and confirm Ansible can reach your managed hosts over SSH — no playbook yet, just connectivity.

---

## 📋 Instructions

### Step 1 — Prepare 2-3 target hosts
Use VMs, containers, or cloud instances you can SSH into. Make sure key-based SSH access works manually first:
```bash
ssh user@host1 "hostname"
```

### Step 2 — Write the inventory file
Create `inventory.ini` (a starter template is already provided in this folder):
```ini
[web]
host1 ansible_host=192.168.1.10
host2 ansible_host=192.168.1.11

[web:vars]
ansible_user=your_ssh_user
```

### Step 3 — Ping all hosts
```bash
ansible all -i inventory.ini -m ping
```

### Step 4 — Ping just the `web` group
```bash
ansible web -i inventory.ini -m ping
```

---

## ✅ Checklist
- [ ] `ansible all -m ping` returns `"ping": "pong"` for every host
- [ ] You understand the difference between `all` and a named group
- [ ] You can explain what `ansible_host` and `ansible_user` do

---

## 💡 Hints
<details><summary>Hint 1 — UNREACHABLE error</summary>
Usually means SSH key auth isn't set up. Test with plain `ssh` first before blaming Ansible.
</details>

<details><summary>Hint 2 — permission denied</summary>
Check `ansible_user` matches the account you SSH in as, and that your public key is in that user's `~/.ssh/authorized_keys`.
</details>
