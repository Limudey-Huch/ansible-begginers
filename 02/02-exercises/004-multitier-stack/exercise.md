# Exercise 004 — Multi-Tier Stack: Frontend + Backend
**Lesson:** 02 — Playbooks & Practical Usage | **Level:** Capstone (builds on 001-003)

---

## 🎯 Goal
Combine everything from this lesson into one playbook that deploys a two-tier application: a backend service plus an nginx frontend that reverse-proxies to it.

---

## 📋 Instructions

This exercise has its own `inventory.ini` (already filled in — `frontend`/`backend`
groups, matching the lab environment). Set this once per terminal session:
```bash
INV=inventory.ini
```

### Step 1 — Review the inventory (`frontend` and `backend` groups)
```ini
[frontend]
fe1 ansible_host=172.28.0.11

[backend]
be1 ansible_host=172.28.0.13

[app:children]
frontend
backend

[app:vars]
ansible_user=root
ansible_ssh_private_key_file=~/ansible-lab/ansible_lab_key
```

### Step 2 — Write the backend play
Starter provided in `playbook.yml` — installs Node.js and starts a simple app service listening on port 3000.

### Step 3 — Write the frontend play
Deploys nginx as a reverse proxy, forwarding requests to the backend host, using the `reverse_proxy.conf.j2` Jinja2 template provided.

### Step 4 — Run the full playbook
```bash
ansible-playbook -i $INV playbook.yml
```

### Step 5 — Verify end-to-end
```bash
curl http://<frontend-ip>/
```
Confirm the response actually comes from the backend service (through the proxy).

---

## ✅ Checklist
- [ ] Backend play installs Node.js and starts the app service
- [ ] Frontend play installs nginx and deploys the reverse-proxy config from a template
- [ ] Changing the template triggers a handler that restarts nginx
- [ ] `curl` against the frontend IP returns the backend's response

---

## 💡 Hints
<details><summary>Hint 1 — template needs the backend IP</summary>
Pass the backend host's address into the template using a variable (e.g. `backend_host: "{{ hostvars['be1']['ansible_host'] }}"`) rather than hardcoding it.
</details>

<details><summary>Hint 2 — order of plays matters</summary>
Put the backend play first in the playbook file — by the time the frontend play configures the proxy, the backend service should already be running.
</details>

<details><summary>Hint 3 — connection refused through the proxy</summary>
Confirm the backend service is actually listening on the expected port with `ansible backend -i $INV -m shell -a "ss -ltnp"` before debugging nginx.
</details>
