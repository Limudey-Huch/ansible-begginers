# Exercise 002 — Configure It with Ansible, Stage by Stage
**Lesson:** 03 — Terraform + Ansible: Basic Cloud Workflow | **Level:** Beginner (builds on 001)

---

## 🎯 Goal
Terraform built the box in Exercise 001. Now hand it to Ansible, exactly like Lessons 01-02 —
except the target is a real EC2 instance instead of a local container. `playbook.yml` installs
and configures nginx in four clear stages: update → install → configure → verify.

---

## ⚠️ Before you start
Exercise 001's instance must still be running:
```bash
cd ../001-terraform-first-server/infra
terraform plan   # should say "No changes." — if it wants to create things, run `terraform apply`
cd ../../002-configure-with-ansible
```

---

## 📋 Instructions

### Step 1 — Point the inventory at your real server
`inventory.ini` has a placeholder IP. Replace it with Exercise 001's actual output:
```bash
IP=$(cd ../001-terraform-first-server/infra && terraform output -raw web_public_ip)
sed -i "s/REPLACE_WITH_TERRAFORM_IP/$IP/" inventory.ini
cat inventory.ini
```
This is the same `[web]` group syntax from Lesson 01 — just with a real cloud IP instead of
a lab container's.

### Step 2 — Read the playbook's stages
Open `playbook.yml`. Four tasks, each commented with which stage it belongs to:
1. **Update** — refresh apt's package index
2. **Install** — put nginx on the box
3. **Configure** — deploy a real `index.html` from a Jinja2 template (notifies a handler)
4. **Verify** — make sure the service is started *and* enabled (survives a reboot)

### Step 3 — Run it
```bash
ansible-playbook -i inventory.ini playbook.yml
```
Watch the task names scroll by in order — that order *is* the staging.

### Step 4 — See it in a browser
```bash
echo "http://$(cd ../001-terraform-first-server/infra && terraform output -raw web_public_ip)/"
```
Open that URL.

### Step 5 — Change one thing, prove idempotency + the handler
Edit `site_title` in `playbook.yml`'s `vars:` to something else, then run it again:
```bash
ansible-playbook -i inventory.ini playbook.yml
```
Look at the `PLAY RECAP`: only the **template** task shows `changed` (the content was
different) — which is the only task that **notifies** the handler, so only now does nginx
restart. `apt`/`service` tasks report `ok` (nothing to do) exactly like in Lesson 02.

### Step 6 — Tear everything down
Done with the single-server chapter — clean up before Exercise 003 builds its own, separate pair:
```bash
cd ../001-terraform-first-server/infra
terraform destroy
```
Type `yes`. Verify in the AWS Console that the instance is `terminated`.

---

## ✅ Checklist
- [ ] `inventory.ini` has a real IP, Terraform's own output — not typed by hand
- [ ] The playbook ran all four stages successfully
- [ ] The page is visible in a browser
- [ ] A second run only restarts nginx when the template content actually changed
- [ ] `terraform destroy` removed the instance, security group, and key pair

---

## 💡 Hints
<details><summary>Hint 1 — "UNREACHABLE" / SSH errors</summary>
Check the path in <code>inventory.ini</code>'s <code>ansible_ssh_private_key_file</code> still
points at Exercise 001's <code>.pem</code> file, and that the instance is still running
(<code>terraform plan</code> in 001's <code>infra/</code> should say "No changes.").
</details>

<details><summary>Hint 2 — "Destination directory /var/www/html does not exist"</summary>
It shouldn't — nginx's own package creates it. If you see this, double-check nginx actually
installed (Step 2's task) before the template task runs.
</details>

<details><summary>Hint 3 — nginx didn't restart after changing site_title</summary>
Handlers only fire when a task that **notifies** them reports `changed`. If the rendered
template is byte-for-byte identical to what's already on disk, Ansible correctly does
nothing — that's idempotency working as intended, not a bug.
</details>
