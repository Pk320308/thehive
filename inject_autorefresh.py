#!/usr/bin/env python3
import os, shutil, zipfile, sys

# These must remain as /opt/thehive inside the container since the container filesystem isn't renamed
JAR = "/opt/thehive/lib/org.thp.thehive-frontend-4.1.24-1.jar"
BACKUP = JAR + ".bak"
WORKDIR = "/tmp/frontend_patch"

SCRIPT = """<script id="cynox-autorefresh">
(function(){
'use strict';
// === CYNOX AUTO SYNC WIDGET ===
var CONFIG = { alerts: 30, cases: 60, dashboard: 60, other: 45 };

function addStyles() {
    var s = document.createElement('style');
    s.textContent = [
        '#cxw{position:fixed;bottom:18px;right:18px;z-index:99999;',
        'background:linear-gradient(135deg,#1a1a2e,#16213e);',
        'border:1px solid #0f3460;border-radius:12px;padding:10px 14px;',
        'color:#e0e0e0;font-family:"Segoe UI",sans-serif;font-size:12px;',
        'box-shadow:0 4px 20px rgba(0,0,0,.5);min-width:170px;user-select:none;}',
        '#cxw .t{color:#e94560;font-weight:700;font-size:11px;letter-spacing:1px;',
        'text-transform:uppercase;margin-bottom:6px;display:flex;align-items:center;gap:6px;}',
        '#cxw .dot{width:8px;height:8px;background:#00ff88;border-radius:50%;',
        'animation:cxp 1.5s infinite;display:inline-block;}',
        '@keyframes cxp{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.8)}}',
        '#cxw .cd{font-size:22px;font-weight:700;color:#00ff88;text-align:center;margin:4px 0;}',
        '#cxw .lbl{color:#888;font-size:10px;text-align:center;}',
        '#cxw .pb{background:#0f3460;border-radius:4px;height:4px;margin-top:8px;overflow:hidden;}',
        '#cxw .pbi{height:100%;background:linear-gradient(90deg,#e94560,#00ff88);',
        'border-radius:4px;transition:width 1s linear;}',
        '#cxw .br{display:flex;gap:6px;margin-top:8px;}',
        '#cxw button{flex:1;padding:4px 8px;border:1px solid #0f3460;border-radius:6px;',
        'background:#0f3460;color:#e0e0e0;font-size:10px;cursor:pointer;}',
        '#cxw button:hover,#cxw button.on{background:#e94560;border-color:#e94560;}'
    ].join('');
    document.head.appendChild(s);
}

function getInterval() {
    var h = (window.location.hash + window.location.pathname).toLowerCase();
    if (h.indexOf('alert') > -1)     return CONFIG.alerts;
    if (h.indexOf('case') > -1)      return CONFIG.cases;
    if (h.indexOf('dashboard') > -1) return CONFIG.dashboard;
    return CONFIG.other;
}

function getPage() {
    var h = (window.location.hash + window.location.pathname).toLowerCase();
    if (h.indexOf('alert') > -1)     return 'Alerts';
    if (h.indexOf('case') > -1)      return 'Cases';
    if (h.indexOf('dashboard') > -1) return 'Dashboard';
    if (h.indexOf('task') > -1)      return 'Tasks';
    if (h.indexOf('user') > -1)      return 'Users';
    return 'Page';
}

function doRefresh() {
    try {
        var inj = angular.element(document.body).injector();
        if (inj) { inj.get('$route').reload(); return; }
    } catch(e) {}
    window.location.reload();
}

function init() {
    addStyles();
    var w = document.createElement('div');
    w.id = 'cxw';
    document.body.appendChild(w);

    var total = getInterval(), rem = total, paused = false;

    function render() {
        var pct = Math.round(((total - rem) / total) * 100);
        w.innerHTML = '<div class="t"><span class="dot"></span>CYNOX AUTO SYNC</div>' +
            '<div class="cd">' + rem + 's</div>' +
            '<div class="lbl">' + getPage() + ' refresh hoga</div>' +
            '<div class="pb"><div class="pbi" style="width:' + pct + '%"></div></div>' +
            '<div class="br">' +
            '<button id="cxp" class="' + (paused ? 'on' : '') + '">' + (paused ? '&#9654; Resume' : '&#9646;&#9646; Pause') + '</button>' +
            '<button id="cxn">&#8635; Now</button>' +
            '</div>';
        document.getElementById('cxp').onclick = function() { paused = !paused; render(); };
        document.getElementById('cxn').onclick = function() { doRefresh(); };
    }

    render();

    setInterval(function() {
        if (!paused) {
            rem--;
            if (rem <= 0) { doRefresh(); total = getInterval(); rem = total; }
        }
        render();
    }, 1000);

    var lastHash = window.location.hash;
    setInterval(function() {
        if (window.location.hash !== lastHash) {
            lastHash = window.location.hash;
            total = getInterval(); rem = total; render();
        }
    }, 500);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
})();
</script>"""

print("=== Cynox Auto-Refresh Injector (Python) ===")

# Workdir
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR)

# Backup
if not os.path.exists(BACKUP):
    shutil.copy2(JAR, BACKUP)
    print("[OK] Backup created")

# Extract JAR
with zipfile.ZipFile(JAR, 'r') as z:
    z.extractall(WORKDIR)
print("[OK] JAR extracted")

# find index.html
target = None
for root, dirs, files in os.walk(WORKDIR):
    for f in files:
        if f == 'index.html':
            target = os.path.join(root, f)
            break

if not target:
    print("[ERROR] index.html not found!")
    sys.exit(1)

print(f"[OK] index.html found: {target}")

# Read
with open(target, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Already injected check
if 'cynox-autorefresh' in content:
    print("[INFO] Script already injected!")
else:
    # Inject
    content = content.replace('</body>', SCRIPT + '\n</body>')
    with open(target, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] Script injected!")

# Rebuild JAR
os.remove(JAR)
with zipfile.ZipFile(JAR, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, dirs, files in os.walk(WORKDIR):
        for file in files:
            filepath = os.path.join(root, file)
            arcname = os.path.relpath(filepath, WORKDIR)
            zout.write(filepath, arcname)

print("[OK] JAR rebuilt successfully!")
print("=== DONE ===")
