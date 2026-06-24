# Walkthrough - Cynox Rebranding and Frontend Library Upgrades

I have successfully completed:
1. The global renaming of **TheHive** to **Cynox** across all files, paths, configuration scripts, and Task Scheduler tasks.
2. Overwriting the UI logo SVGs with custom branded **Cynox** logo files.
3. Upgrading frontend libraries to their highest compatible stable versions (Option A) to secure and modernize the platform.

---

## 🛠️ Changes Executed

### 1. Codebase Global Renaming
* Globally replaced `TheHive` / `thehive` / `THEHIVE` with `Cynox` / `cynox` / `CYNOX` across all source code, comments, configurations, and scheduled tasks.
* Aligned docker volume mounts to point to `./Cynox-main` and `./db_data/cynox` folders.

### 2. Custom UI Branding (Bee Logo & Text)
* Copied the custom branded `logo.white.svg` and `logo.svg` from host to the container's frontend bundle JAR.
* Now, the top-left header logo cleanly displays **Cynox** with the yellow bee icon.

### 3. Frontend Upgrades (Option A)
* **AngularJS Upgrade (1.7.8 ➔ 1.8.3)**:
  * Downloaded stable production AngularJS **1.8.3** core and module files (`animate`, `sanitize`, `cookies`, `resource`, `touch`, `messages`).
  * Copied files into the container's frontend scripts folder.
  * Injected script tags immediately after `vendor.78eed977.js` to override legacy 1.7.8 modules on app bootstrap.
* **Font-Awesome Upgrade (4.7.0 ➔ 6.5.2)**:
  * Downloaded Font-Awesome **6.5.2** SVG/JS bundle along with its **v4 compatibility shims**.
  * Copied files into the container's frontend scripts folder.
  * Injected scripts to automatically convert all legacy `fa fa-` icons in HTML views into high-quality modern SVG icons.

---

## 🔬 Verification Results

### 1. Service Status
* All docker containers are running cleanly.
* API `/api/status` returns **200 OK** with Cassandra schema version `99` fully active.

### 2. Frontend HTML Script Load Check
* Inside the container's served HTML:
  * Upgraded AngularJS 1.8.3 scripts are verified as **Active**.
  * Font-Awesome 6 SVG/JS engine and v4 shims are verified as **Active**.
  * Cynox Auto-Refresh sync widget is verified as **Active**.
* **Branding Check**: `index.html` and `scripts.js` contain **0** instances of `thehive`.
