// ==UserScript==
// @name         Cynox Cynox - Auto Refresh All Pages
// @namespace    http://cynox.security/
// @version      2.0
// @description  Cynox ke sab pages automatic refresh hote rahenge
// @author       Cynox Security
// @match        http://localhost:9001/*
// @match        http://127.0.0.1:9001/*
// @grant        none
// @run-at       document-end
// ==/UserScript==

(function () {
    'use strict';

    // ============================
    // CONFIGURATION
    // ============================
    const CONFIG = {
        alertsRefresh:    30,   // seconds - Alerts page
        casesRefresh:     60,   // seconds - Cases page
        dashboardRefresh: 60,   // seconds - Dashboard
        defaultRefresh:   45,   // seconds - Baaki sab pages
    };

    // ============================
    // STYLES
    // ============================
    const style = document.createElement('style');
    style.textContent = `
        #cynox-refresh-widget {
            position: fixed;
            bottom: 18px;
            right: 18px;
            z-index: 99999;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border: 1px solid #0f3460;
            border-radius: 12px;
            padding: 10px 14px;
            color: #e0e0e0;
            font-family: 'Segoe UI', sans-serif;
            font-size: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            min-width: 180px;
            transition: all 0.3s ease;
            cursor: default;
            user-select: none;
        }
        #cynox-refresh-widget:hover { transform: scale(1.02); }
        #cynox-refresh-widget .title {
            color: #e94560;
            font-weight: bold;
            font-size: 11px;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        #cynox-refresh-widget .dot {
            width: 8px; height: 8px;
            background: #00ff88;
            border-radius: 50%;
            animation: pulse 1.5s infinite;
            display: inline-block;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.8); }
        }
        #cynox-refresh-widget .countdown {
            font-size: 22px;
            font-weight: bold;
            color: #00ff88;
            text-align: center;
            margin: 4px 0;
        }
        #cynox-refresh-widget .label {
            color: #888;
            font-size: 10px;
            text-align: center;
        }
        #cynox-refresh-widget .progress-bar-wrap {
            background: #0f3460;
            border-radius: 4px;
            height: 4px;
            margin-top: 8px;
            overflow: hidden;
        }
        #cynox-refresh-widget .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #e94560, #00ff88);
            border-radius: 4px;
            transition: width 1s linear;
        }
        #cynox-refresh-widget .btn-row {
            display: flex;
            gap: 6px;
            margin-top: 8px;
        }
        #cynox-refresh-widget button {
            flex: 1;
            padding: 4px 8px;
            border: 1px solid #0f3460;
            border-radius: 6px;
            background: #0f3460;
            color: #e0e0e0;
            font-size: 10px;
            cursor: pointer;
            transition: all 0.2s;
        }
        #cynox-refresh-widget button:hover { background: #e94560; border-color: #e94560; }
        #cynox-refresh-widget button.paused { background: #e94560; border-color: #e94560; }
    `;
    document.head.appendChild(style);

    // ============================
    // DETECT CURRENT PAGE
    // ============================
    function getRefreshInterval() {
        const hash = window.location.hash || '';
        const path = window.location.pathname || '';
        const full = (hash + path).toLowerCase();

        if (full.includes('alert'))     return CONFIG.alertsRefresh;
        if (full.includes('case'))      return CONFIG.casesRefresh;
        if (full.includes('dashboard')) return CONFIG.dashboardRefresh;
        return CONFIG.defaultRefresh;
    }

    function getPageName() {
        const hash = window.location.hash || '';
        const path = window.location.pathname || '';
        const full = (hash + path).toLowerCase();

        if (full.includes('alert'))     return 'Alerts';
        if (full.includes('case'))      return 'Cases';
        if (full.includes('dashboard')) return 'Dashboard';
        if (full.includes('user'))      return 'Users';
        if (full.includes('org'))       return 'Organizations';
        if (full.includes('task'))      return 'Tasks';
        return 'Page';
    }

    // ============================
    // REFRESH DATA (without full page reload)
    // ============================
    function refreshData() {
        // AngularJS scope ko trigger karo fresh data ke liye
        try {
            const injector = angular.element(document.body).injector();
            if (injector) {
                const $rootScope = injector.get('$rootScope');
                $rootScope.$broadcast('refresh');
                $rootScope.$apply();
            }
        } catch(e) {}

        // Agar AngularJS refresh kaam na kare to page reload
        try {
            const injector = angular.element(document.body).injector();
            const $route = injector.get('$route');
            if ($route) {
                $route.reload();
                return;
            }
        } catch(e) {}

        // Fallback: full page reload
        window.location.reload();
    }

    // ============================
    // WIDGET
    // ============================
    const widget = document.createElement('div');
    widget.id = 'cynox-refresh-widget';
    document.body.appendChild(widget);

    let totalSeconds = getRefreshInterval();
    let remaining   = totalSeconds;
    let isPaused    = false;
    let timer       = null;

    function updateWidget() {
        const pct = ((totalSeconds - remaining) / totalSeconds) * 100;
        widget.innerHTML = `
            <div class="title">
                <span class="dot"></span>
                CYNOX AUTO SYNC
            </div>
            <div class="countdown">${remaining}s</div>
            <div class="label">${getPageName()} refresh hoga</div>
            <div class="progress-bar-wrap">
                <div class="progress-bar" style="width:${pct}%"></div>
            </div>
            <div class="btn-row">
                <button id="cynox-pause-btn" class="${isPaused ? 'paused' : ''}">
                    ${isPaused ? '▶ Resume' : '⏸ Pause'}
                </button>
                <button id="cynox-now-btn">🔄 Now</button>
            </div>
        `;

        document.getElementById('cynox-pause-btn').onclick = () => {
            isPaused = !isPaused;
            updateWidget();
        };

        document.getElementById('cynox-now-btn').onclick = () => {
            remaining = 0;
            refreshData();
            remaining = totalSeconds;
            updateWidget();
        };
    }

    function tick() {
        if (!isPaused) {
            remaining--;
            if (remaining <= 0) {
                refreshData();
                // Re-detect interval (page change ho sakta hai)
                totalSeconds = getRefreshInterval();
                remaining    = totalSeconds;
            }
        }
        updateWidget();
    }

    // Start
    updateWidget();
    timer = setInterval(tick, 1000);

    // URL change detect karo (AngularJS SPA)
    let lastHash = window.location.hash;
    setInterval(() => {
        if (window.location.hash !== lastHash) {
            lastHash     = window.location.hash;
            totalSeconds = getRefreshInterval();
            remaining    = totalSeconds;
            updateWidget();
        }
    }, 500);

})();
