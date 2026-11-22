# Ansible Lab Environment — Setup Guide

A lightweight practice environment for this course: 3 SSH-reachable Docker containers
acting as "real" managed servers, running on a single Ubuntu Server VM. Ansible itself
runs on that same VM as the Control Node — no per-student VMs, no cloud account needed.

```
Ubuntu Server VM  (Control Node — Ansible installed here)
  └── Docker
        ├── node1  172.28.0.11   (web / frontend)
        ├── node2  172.28.0.12   (web)
        └── node3  172.28.0.13   (db / backend)
```

Each container is built from the local `Dockerfile`, which extends
`geerlingguy/docker-ubuntu2204-ansible` (a Ubuntu 22.04 image with systemd already set
up, purpose-built for testing Ansible playbooks — so `service`/`systemd` modules work
normally, e.g. installing and starting nginx) and adds `openssh-server`, enabled to
start automatically on boot — since the base image itself ships without SSH.

---

## 1. Generate an SSH key for the lab

Run this **outside** this folder (e.g. in your home directory) — if this folder is a
shared/mounted folder, permission bits on the private key may not be preserved there,
and SSH will refuse a key with the wrong permissions.

```bash
mkdir -p ~/ansible-lab
ssh-keygen -t ed25519 -f ~/ansible-lab/ansible_lab_key -N ""
```

## 2. Copy the public key where docker-compose expects it

```bash
cp ~/ansible-lab/ansible_lab_key.pub ~/ansible-lab/authorized_keys
```
**Not** into this course folder — `docker-compose.yml` mounts
`${HOME}/ansible-lab/authorized_keys` into each container, a normal (non-shared) path, for
the same permission reason as Step 1.

## 3. Build the image, then start the containers

```bash
docker compose build
docker compose up -d
docker compose ps   # all 3 should show "Up"
```

## 4. Verify connectivity

```bash
ssh -i ~/ansible-lab/ansible_lab_key root@172.28.0.11 hostname    # manual SSH check
ansible all -i inventory.ini -m ping    # run from this folder — ansible.cfg here is auto-loaded
```

All three hosts should report `"pong"`.

## 5. Use it with the course exercises

`inventory.ini` already defines the groups the exercises expect:
- `[web]` → node1, node2 (used in Lesson 1 exercises 002–004)
- `[db]` → node3 (used in Lesson 1 exercise 004)
- `[frontend]` / `[backend]` → node1 / node3 (used in Lesson 2's multi-tier capstone)

Each exercise's own `inventory.ini` already points at these same IPs — just run
it with `-i inventory.ini` from inside the exercise folder.

## 6. Resetting between classes

Containers are ephemeral by design — to wipe all student changes and start clean:

```bash
docker compose down && docker compose up -d
```

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `Unit ssh.service could not be found` | You're running the raw base image instead of the local build — run `docker compose build` first, then `up -d` |
| `connect to host ... port 22: Connection refused` | SSH isn't running yet, or the image wasn't rebuilt after a Dockerfile change — `docker compose up -d --build` |
| `Permission denied (publickey)` | `~/ansible-lab/authorized_keys` wasn't created (or has the wrong key) before `docker compose up -d` — `docker compose down && cp ~/ansible-lab/ansible_lab_key.pub ~/ansible-lab/authorized_keys && docker compose up -d` |
| `UNPROTECTED PRIVATE KEY FILE` from `ssh` | The private key lives on a shared/mounted filesystem that doesn't preserve permissions — regenerate it under a normal path like `~/ansible-lab/`, not inside the mounted course folder |
| `[WARNING]: Ansible is being run in a world writable directory... ignoring it as an ansible.cfg source`, then `Host key verification failed` | Happens when this course folder is a shared/mounted one — Ansible refuses to trust a config file it can't be sure only you can edit, so this folder's `ansible.cfg` (and its `host_key_checking = False`) gets skipped. Run `ansible-playbook`/`ansible` from a normal, non-shared path instead, or clear the stale key with `ssh-keygen -R <ip>` per host |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED` from plain `ssh` | The container was rebuilt (`docker compose down && up`, or Step 6) and got a new SSH host key at the same IP. Harmless here — run the `ssh-keygen -R <ip>` command the warning itself prints, then reconnect |
| `python: command not found` | Shouldn't happen with this image, but if using a different base, install `python3` in it — Ansible requires it on managed nodes |
| systemd/service module fails ("System has not been booted with systemd") | Missing `privileged: true` / `cgroup: host` / cgroup volume mount — these are required for systemd to run inside the container |
