# Exercise 004 — Deploy the Radar App (Capstone)
**Lesson:** 04 — Ansible + AWS: Cloud Provisioning (Advanced) | **Level:** Capstone (builds on 001-003)

---

## 🎯 Goal
Deploy a real, working application across the 3-tier infrastructure from Exercise 003: a
live aircraft radar, with aircraft visibly moving in real time, that you can open in your browser.

**The stack:**
- **db tier** — PostgreSQL, storing the current position of every simulated aircraft
- **app tier** — a Flask API (serves the current snapshot) + a systemd timer that runs a
  flight simulator every 5s, moving each aircraft forward and refreshing the database
- **web tier** — nginx, serving the static radar page and reverse-proxying `/api/*` to the app tier

> **Why simulated, not real flight data?** An earlier version of this exercise polled the
> real [OpenSky Network](https://opensky-network.org) API. It turns out OpenSky (and similar
> free flight-tracking APIs) actively block anonymous requests from AWS/cloud IP ranges —
> confirmed by testing the exact same request from a home connection (worked instantly) vs.
> from the app tier itself (timed out every time). A simulator sidesteps that entirely, and
> as a bonus gives obviously-visible motion between polls, which real aircraft at 15-30s
> intervals barely do. `poller.py`'s docstring has the full story if you want to try wiring
> up a real feed later (e.g. an authenticated OpenSky client, or running the poller from
> outside AWS and pushing into this DB).

---

## ⚠️ Before you start
Make sure Exercise 003's three instances are up:
```bash
cd ../003-three-tier-provisioning
ansible-playbook provision_three_tier.yml
cd ../004-deploy-radar-app
```

---

## 📋 Instructions

### Step 1 — Look at what you're deploying
Skim `playbook.yml` — three plays, one per tier, in the order `db → app → web` (the app tier's
`.env` file needs the db's address already resolved; the web tier's nginx config needs the
app tier's).

### Step 2 — Deploy
```bash
ansible-playbook -i inventory.aws_ec2.yml playbook.yml
```

### Step 3 — Open it in a browser
```bash
ansible-inventory -i inventory.aws_ec2.yml --list | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('http://' + d['_meta']['hostvars'][d['role_web']['hosts'][0]]['ansible_host'] + '/')
"
```
Open that URL. Give the poller ~5-10s after deploy to run for the first time — the radar
starts empty and fills in once the first tick completes, then aircraft should visibly
drift across the screen every ~5 seconds.

### Step 4 — Verify each piece independently
```bash
# API responding?
curl http://<web-ip>/api/aircraft

# Poller actually running on schedule?
ansible role_app -i inventory.aws_ec2.yml -m shell -a "systemctl list-timers radar-poller.timer" --become

# See the poller's own log output
ansible role_app -i inventory.aws_ec2.yml -m shell -a "journalctl -u radar-poller.service -n 20 --no-pager" --become
```

### Step 5 — Click an aircraft
Click any blip on the radar — a info panel should appear with callsign, altitude, speed, heading.

### Step 6 — Tear everything down
```bash
cd ../001-first-ec2-instance
ansible-playbook teardown.yml
```

---

## ✅ Checklist
- [ ] The radar page loads and shows the static UI even before any aircraft appear
- [ ] Aircraft blips appear within ~10s of deployment and visibly move between refreshes
- [ ] Clicking a blip shows its details
- [ ] `systemctl list-timers radar-poller.timer` shows it firing every ~5s
- [ ] You can explain the full request path: browser → nginx (web) → Flask API (app) → Postgres (db)

---

## 💡 Hints
<details><summary>Hint 1 — blank page / nginx default page</summary>
Check `ansible-playbook` actually finished the web play without errors. Also confirm `/etc/nginx/sites-enabled/default` was removed — if it's still there alongside `radar`, nginx may be serving the wrong site depending on config order.
</details>

<details><summary>Hint 2 — radar page loads but /api/aircraft fails</summary>
Check the app tier directly: `ansible role_app -i inventory.aws_ec2.yml -m shell -a "systemctl status radar-api.service" --become`. A common cause: the `.env` file couldn't resolve `groups['role_db']` — confirm Exercise 003's db instance is actually running and tagged correctly.
</details>

<details><summary>Hint 3 — radar stays empty, no errors anywhere</summary>
Check `journalctl -u radar-poller.service` for "Simulated tick: N -> M aircraft" — if this isn't appearing every ~5s, the timer isn't firing (`systemctl list-timers radar-poller.timer`) or the service is failing silently (`systemctl status radar-poller.service`).
</details>

<details><summary>Hint 4 — motion is too subtle / too chaotic</summary>
Both are tunable in `app/radar-app.env.j2` (then redeploy the app tier): `radar_speed_multiplier` controls how far aircraft move per tick (displayed speed in the info panel stays realistic either way), and `RADAR_TICK_SECONDS` in `app/systemd/radar-poller.timer` controls how often. Keep them roughly matched to the frontend's 5s poll interval (`POLL_MS` in `radar.js`) so motion looks continuous rather than jumpy.
</details>

<details><summary>Hint 4 — postgresql.conf path not found</summary>
The playbook assumes PostgreSQL 14 (Ubuntu 22.04's default). If `apt` installed a different major version, adjust the `/etc/postgresql/14/main/...` paths in the db play to match (`ls /etc/postgresql/` on the db host to check).
</details>
