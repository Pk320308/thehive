import http.server
import socketserver
import sys
import json
import urllib.parse
import urllib.request
import uuid
import time
import os

PORT = 8085
FRONTEND_DIR = r"E:\Cynox New\Cynox-main\Cynox-main\frontend\app"

# Bower components redirects mapping
BOWER_MAPPINGS = {
    "bower_components/jquery/dist/jquery.js": "https://unpkg.com/jquery@3.4.1/dist/jquery.js",
    "bower_components/angular/angular.js": "https://unpkg.com/angular@1.7.8/angular.js",
    "bower_components/angular-animate/angular-animate.js": "https://unpkg.com/angular-animate@1.7.8/angular-animate.js",
    "bower_components/angular-bootstrap/ui-bootstrap-tpls.js": "https://unpkg.com/angular-ui-bootstrap@2.5.0/dist/ui-bootstrap-tpls.js",
    "bower_components/angular-cookies/angular-cookies.js": "https://unpkg.com/angular-cookies@1.7.8/angular-cookies.js",
    "bower_components/moment/moment.js": "https://unpkg.com/moment@2.24.0/moment.js",
    "bower_components/angular-moment/angular-moment.js": "https://unpkg.com/angular-moment@0.10.3/angular-moment.js",
    "bower_components/angular-resource/angular-resource.js": "https://unpkg.com/angular-resource@1.7.8/angular-resource.js",
    "bower_components/angular-sanitize/angular-sanitize.js": "https://unpkg.com/angular-sanitize@1.7.8/angular-sanitize.js",
    "bower_components/humanize-duration/humanize-duration.js": "https://unpkg.com/humanize-duration@3.27.0/humanize-duration.js",
    "bower_components/angular-timer/dist/angular-timer.js": "https://unpkg.com/angular-timer@1.3.5/dist/angular-timer.js",
    "bower_components/angular-touch/angular-touch.js": "https://unpkg.com/angular-touch@1.7.8/angular-touch.js",
    "bower_components/angular-ui-router/release/angular-ui-router.js": "https://unpkg.com/angular-ui-router@0.4.3/release/angular-ui-router.js",
    "bower_components/bootstrap/dist/js/bootstrap.js": "https://unpkg.com/bootstrap@3.4.1/dist/js/bootstrap.js",
    "bower_components/bootstrap/dist/css/bootstrap.min.css": "https://unpkg.com/bootstrap@3.4.1/dist/css/bootstrap.min.css",
    "bower_components/font-awesome/css/font-awesome.min.css": "https://unpkg.com/font-awesome@4.7.0/css/font-awesome.min.css",
    "bower_components/font-awesome/fonts/fontawesome-webfont.woff2": "https://unpkg.com/font-awesome@4.7.0/fonts/fontawesome-webfont.woff2",
    "bower_components/font-awesome/fonts/fontawesome-webfont.woff": "https://unpkg.com/font-awesome@4.7.0/fonts/fontawesome-webfont.woff",
    "bower_components/font-awesome/fonts/fontawesome-webfont.ttf": "https://unpkg.com/font-awesome@4.7.0/fonts/fontawesome-webfont.ttf",
    "bower_components/bootstrap-sass-official/assets/javascripts/bootstrap.js": "https://unpkg.com/bootstrap@3.4.1/dist/js/bootstrap.js",
    "bower_components/dropzone/dist/min/dropzone.min.js": "https://unpkg.com/dropzone@4.3.0/dist/min/dropzone.min.js",
    "bower_components/dropzone/dist/min/dropzone.min.css": "https://unpkg.com/dropzone@4.3.0/dist/min/dropzone.min.css",
    "bower_components/ng-csv/build/ng-csv.min.js": "https://unpkg.com/ng-csv@0.3.6/build/ng-csv.min.js",
    "bower_components/ng-tags-input/ng-tags-input.js": "https://unpkg.com/ng-tags-input@3.2.0/build/ng-tags-input.js",
    "bower_components/ng-tags-input/ng-tags-input.css": "https://unpkg.com/ng-tags-input@3.2.0/build/ng-tags-input.css",
    "bower_components/ng-tags-input/ng-tags-input.bootstrap.min.css": "https://unpkg.com/ng-tags-input@3.2.0/build/ng-tags-input.bootstrap.min.css",
    "bower_components/underscore/underscore-umd.js": "https://unpkg.com/underscore@1.9.1/underscore.js",
    "bower_components/angular-ui-notification/dist/angular-ui-notification.js": "https://unpkg.com/angular-ui-notification@0.3.6/dist/angular-ui-notification.js",
    "bower_components/angular-ui-notification/dist/angular-ui-notification.css": "https://unpkg.com/angular-ui-notification@0.3.6/dist/angular-ui-notification.css",
    "bower_components/d3/d3.js": "https://unpkg.com/d3@3.5.17/d3.js",
    "bower_components/c3/c3.js": "https://unpkg.com/c3@0.4.24/c3.js",
    "bower_components/c3/c3.css": "https://unpkg.com/c3@0.4.24/c3.css",
    "bower_components/angular-messages/angular-messages.js": "https://unpkg.com/angular-messages@1.7.8/angular-messages.js",
    "bower_components/ng-file-upload/ng-file-upload.js": "https://unpkg.com/ng-file-upload@12.2.13/dist/ng-file-upload.js",
    "bower_components/ng-file-upload-shim/ng-file-upload-shim.js": "https://unpkg.com/ng-file-upload@12.2.13/dist/ng-file-upload-shim.js",
    "bower_components/es5-shim/es5-shim.js": "https://unpkg.com/es5-shim@4.5.15/es5-shim.js",
    "bower_components/es6-shim/es6-shim.js": "https://unpkg.com/es6-shim@0.35.6/es6-shim.js",
    "bower_components/angular-clipboard/angular-clipboard.js": "https://unpkg.com/angular-clipboard@1.7.0/angular-clipboard.js",
    "bower_components/angular-local-storage/dist/angular-local-storage.js": "https://unpkg.com/angular-local-storage@0.7.1/dist/angular-local-storage.js",
    "bower_components/angular-highlightjs/build/angular-highlightjs.js": "https://unpkg.com/angular-highlightjs@0.7.1/build/angular-highlightjs.js",
    "bower_components/marked/lib/marked.js": "https://unpkg.com/marked@0.8.2/lib/marked.js",
    "bower_components/angular-marked/dist/angular-marked.js": "https://unpkg.com/angular-marked@1.2.2/dist/angular-marked.js",
    "bower_components/bootstrap-markdown/js/bootstrap-markdown.js": "https://unpkg.com/bootstrap-markdown@2.10.0/js/bootstrap-markdown.js",
    "bower_components/bootstrap-markdown/css/bootstrap-markdown.min.css": "https://unpkg.com/bootstrap-markdown@2.10.0/css/bootstrap-markdown.min.css",
    "bower_components/angular-markdown-editor-ghiscoding/src/angular-markdown-editor.js": "https://unpkg.com/angular-markdown-editor@1.1.5/src/angular-markdown-editor.js",
    "bower_components/angular-markdown-editor-ghiscoding/styles/angular-markdown-editor.css": "https://unpkg.com/angular-markdown-editor@1.1.5/styles/angular-markdown-editor.css",
    "bower_components/angular-ui-ace/ui-ace.js": "https://unpkg.com/angular-ui-ace@0.2.3/src/ui-ace.js",
    "bower_components/angular-page-loader/dist/angular-page-loader.js": "https://unpkg.com/angular-page-loader/dist/angular-page-loader.js",
    "bower_components/angular-page-loader/dist/angular-page-loader.css": "https://unpkg.com/angular-page-loader/dist/angular-page-loader.css",
    "bower_components/angular-images-resizer/angular-images-resizer.js": "https://unpkg.com/angular-images-resizer@2.0.3/angular-images-resizer.js",
    "bower_components/angular-base64-upload/src/angular-base64-upload.js": "https://unpkg.com/angular-base64-upload@0.1.19/src/angular-base64-upload.js",
    "bower_components/jquery-ui/jquery-ui.js": "https://unpkg.com/jquery-ui-dist@1.12.1/jquery-ui.js",
    "bower_components/angular-ui-sortable/sortable.js": "https://unpkg.com/angular-ui-sortable@0.19.0/dist/sortable.js",
    "bower_components/js-base64/base64.js": "https://unpkg.com/js-base64@2.5.2/base64.js",
    "bower_components/angular-scroll/angular-scroll.js": "https://unpkg.com/angular-scroll@1.0.2/angular-scroll.js",
    "bower_components/underscore.string/dist/underscore.string.js": "https://unpkg.com/underscore.string@3.3.5/dist/underscore.string.js",
    "bower_components/angular-drag-and-drop-lists/angular-drag-and-drop-lists.js": "https://unpkg.com/angular-drag-and-drop-lists@2.1.0/angular-drag-and-drop-lists.js",
    "bower_components/angular-bootstrap-colorpicker/js/bootstrap-colorpicker-module.js": "https://unpkg.com/angular-bootstrap-colorpicker@3.0.32/js/bootstrap-colorpicker-module.js",
    "bower_components/angular-bootstrap-colorpicker/css/colorpicker.css": "https://unpkg.com/angular-bootstrap-colorpicker@3.0.32/css/colorpicker.css",
    "bower_components/file-saver/FileSaver.js": "https://unpkg.com/file-saver@1.3.4/dist/FileSaver.js",
    "bower_components/js-url/url.js": "https://unpkg.com/js-url/url.js",
    "bower_components/bootstrap-sass/assets/javascripts/bootstrap.js": "https://unpkg.com/bootstrap@3.4.1/dist/js/bootstrap.js",
    "bower_components/angular-bootstrap-multiselect/dist/angular-bootstrap-multiselect.js": "https://unpkg.com/angular-bootstrap-multiselect@1.1.11/dist/angular-bootstrap-multiselect.js",
    "bower_components/qrcode.js/lib/qrcode.js": "https://unpkg.com/qrcode-generator@1.4.4/qrcode.js",
    "bower_components/qrcode/lib/qrcode.js": "https://unpkg.com/qrcode-generator@1.4.4/qrcode.js",
    "bower_components/angular-qr/src/angular-qr.js": "https://unpkg.com/angular-qrcode/angular-qrcode.js",
    "bower_components/animate.css/animate.css": "https://unpkg.com/animate.css@3.7.2/animate.css",
    "bower_components/roboto-fontface/css/roboto/roboto-fontface.css": "https://unpkg.com/roboto-fontface@0.10.0/css/roboto/roboto-fontface.css",
    "bower_components/css-spaces/dist/spaces.css": "https://unpkg.com/css-spaces@0.3.5/dist/spaces.css",
    "bower_components/smalot-bootstrap-datetimepicker/css/bootstrap-datetimepicker.css": "https://cdnjs.cloudflare.com/ajax/libs/smalot-bootstrap-datetimepicker/2.4.4/css/bootstrap-datetimepicker.min.css",
    "bower_components/smalot-bootstrap-datetimepicker/js/bootstrap-datetimepicker.min.js": "https://cdnjs.cloudflare.com/ajax/libs/smalot-bootstrap-datetimepicker/2.4.4/js/bootstrap-datetimepicker.min.js",
    "bower_components/cryptojslib/components/core-min.js": "https://unpkg.com/crypto-js@3.1.9-1/core.js",
    "bower_components/cryptojslib/components/sha256-min.js": "https://unpkg.com/crypto-js@3.1.9-1/sha256.js",
    "bower_components/cryptojslib/components/md5-min.js": "https://unpkg.com/crypto-js@3.1.9-1/md5.js",
    "bower_components/ace-builds/src-min-noconflict/ace.js": "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js"
}

# ── In-memory databases ────────────────────────────────────────────────────────
DB = {
    "organisations": [
        {"_id": "admin", "name": "admin", "description": "Default admin organisation",
         "_createdAt": 1700000000000, "_updatedAt": 1700000000000, "_createdBy": "system"}
    ],
    "users": [
        {"_id": "admin_user", "login": "admin@cynox.local", "name": "Administrator",
         "organisation": "admin", "profile": "admin",
         "roles": ["admin", "read", "write"],
         "permissions": ["managePlatform","manageProfile","manageTaxonomy",
                         "manageOrganisation","manageUser","manageCaseTemplate",
                         "manageCustomField","manageObservableTemplate"],
         "_createdAt": 1700000000000, "_updatedAt": 1700000000000}
    ],
    "cases": [],
    "alerts": [],
    "profiles": [
        {"_id": "admin",     "name": "admin",     "permissions": ["managePlatform","manageOrganisation","manageUser","manageCaseTemplate","manageCustomField","manageObservableTemplate"], "editable": False},
        {"_id": "analyst",   "name": "analyst",   "permissions": ["manageCase","manageTask","manageObservable","manageAlert"], "editable": True},
        {"_id": "read-only", "name": "read-only", "permissions": [], "editable": True}
    ]
}

CURRENT_USER = {
    "login": "admin@cynox.local",
    "name": "Administrator",
    "organisation": "admin",
    "profile": "admin",
    "roles": ["admin", "read", "write"],
    "permissions": ["managePlatform","manageProfile","manageTaxonomy",
                    "manageOrganisation","manageUser","manageCaseTemplate",
                    "manageCustomField","manageObservableTemplate"]
}

STATUS_DATA = {
    "config": {
        "freeTagDefaultColour": "#000000",
        "pollingDuration": 1000,
        "theme": "default",
        "authentication": {"providers": [{"name": "local"}]},
        "maxArtifactSize": 10737418240,
        "ssoAutoLogin": False,
        "authType": ["local"],
        "capabilities": ["changePassword", "authByKey", "mfa", "setPassword"],
        "protectDownloadsWith": None
    },
    "versions": {"Cynox": "4.1.24-1", "Scalligraph": "1.0.0", "Play": "2.8.8"},
    "connectors": {
        "cortex": {"enabled": False, "servers": []},
        "misp":   {"enabled": False, "servers": []}
    },
    "schemaStatus": []
}

MOCK_STREAM_ID = "mock-stream-001"

def ts():
    return int(time.time() * 1000)

def send_json(handler, data, code=200):
    body = json.dumps(data).encode()
    handler.send_response(code)
    handler.send_header('Content-type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(body)))
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.send_header('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,X-Organisation')
    handler.end_headers()
    handler.wfile.write(body)

def read_body(handler):
    try:
        length = int(handler.headers.get('Content-Length', 0))
        if length > 0:
            raw = handler.rfile.read(length)
            return json.loads(raw.decode('utf-8'))
    except Exception as e:
        sys.stderr.write(f"[read_body error] {e}\n")
    return {}

class LocalServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    # ── OPTIONS (CORS preflight) ───────────────────────────────────────────────
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,X-Organisation')
        self.end_headers()

    # ── GET ────────────────────────────────────────────────────────────────────
    def do_GET(self):
        raw_path = urllib.parse.unquote(self.path)
        # Separate path and query string
        url_path = raw_path.lstrip('/').split('?')[0]
        p = url_path.rstrip('/')

        # ── Static files / Bower Component Redirection ──
        if not p.startswith('api'):
            # Detect nested SPA asset requests and normalize them
            asset_dirs = ['/scripts/', '/bower_components/', '/styles/', '/images/', '/views/']
            normalized_p = p
            for ad in asset_dirs:
                if ad in raw_path:
                    # Extract from the directory name onwards
                    idx = raw_path.index(ad)
                    normalized_p = raw_path[idx+1:].split('?')[0]
                    break
            
            # If we normalized it, update p, url_path and self.path
            if normalized_p != p:
                p = normalized_p
                url_path = normalized_p
                self.path = '/' + normalized_p

            # Intercept angular-qr and patch it
            if "angular-qr/src/angular-qr.js" in url_path:
                try:
                    url = "https://unpkg.com/angular-qr@0.2.2/src/angular-qr.js"
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        content = response.read().decode('utf-8')
                    # Patch require statements to work directly in browser
                    content = content.replace("var qrcode = require('qrcode-genetator');", "var qrcode = window.qrcode || window.QRCode;")
                    # Remove CommonJS exports that throw in browser
                    content = content.replace("module.exports = 'ja.qr';", "")
                    content_bytes = content.encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-type', 'application/javascript; charset=utf-8')
                    self.send_header('Content-Length', str(len(content_bytes)))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(content_bytes)
                    return
                except Exception as e:
                    sys.stderr.write(f"[angular-qr patch error] {e}\n")

            # Intercept angular-page-loader and patch it
            if "angular-page-loader/dist/angular-page-loader.js" in url_path:
                try:
                    url = "https://unpkg.com/angular-page-loader@1.0.0/dist/angular-page-loader.js"
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        content = response.read().decode('utf-8')
                    
                    old_code = """        if( attr.flag ) {

            scope.$watch('isLoading', function(n) {
                return n ? elem.removeClass('ng-hide') : elem.addClass('ng-hide');
            });

        }"""
                    new_code = """        if( attr.flag ) {

            scope.$watch('isLoading', function(n) {
                return n ? elem.removeClass('ng-hide') : elem.addClass('ng-hide');
            });

            var stopLoader = function() {
                scope.isLoading = false;
                if (typeof $timeout !== 'undefined') {
                    $timeout(function() {
                        elem.addClass('ng-hide');
                    }, 50);
                } else {
                    elem.addClass('ng-hide');
                }
            };
            scope.$on('$stateChangeSuccess', stopLoader);
            scope.$on('$stateChangeError', stopLoader);
            scope.$on('$routeChangeSuccess', stopLoader);
            scope.$on('$routeChangeError', stopLoader);
            scope.$on('$locationChangeSuccess', stopLoader);
        }"""
                    if old_code in content:
                        content = content.replace(old_code, new_code)
                    else:
                        content = content.replace("if( attr.flag ) {", "if( attr.flag ) {\n            var stopLoader = function() { scope.isLoading = false; elem.addClass('ng-hide'); };\n            scope.$on('$stateChangeSuccess', stopLoader);\n            scope.$on('$stateChangeError', stopLoader);\n            scope.$on('$routeChangeSuccess', stopLoader);\n            scope.$on('$routeChangeError', stopLoader);")
                    
                    content_bytes = content.encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-type', 'application/javascript; charset=utf-8')
                    self.send_header('Content-Length', str(len(content_bytes)))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(content_bytes)
                    return
                except Exception as e:
                    sys.stderr.write(f"[angular-page-loader patch error] {e}\n")

            # 1. Intercept Bower requests and redirect them to UNPKG/CDN
            for pattern, cdn_url in BOWER_MAPPINGS.items():
                if url_path.startswith(pattern):
                    self.send_response(307)
                    self.send_header('Location', cdn_url)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    return

            # Fallback for dynamic bower component redirects
            if url_path.startswith("bower_components/"):
                rest = url_path.replace("bower_components/", "", 1)
                target_url = f"https://unpkg.com/{rest}"
                self.send_response(307)
                self.send_header('Location', target_url)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                return

            # Check if the actual file exists on disk
            disk_path = os.path.join(FRONTEND_DIR, p)
            if os.path.isfile(disk_path):
                return super().do_GET()

            # SPA fallback: serve index.html for all Angular routes
            index_path = os.path.join(FRONTEND_DIR, 'index.html')
            if os.path.isfile(index_path):
                with open(index_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            return super().do_GET()

        # ── API routes ─────────────────────────────────────────────────────────
        # api/status
        if p == 'api/status':
            return send_json(self, STATUS_DATA)

        # api/v1/describe/_all or api/v0/describe/_all (FilteringSrv metadata)
        if 'describe/_all' in p:
            describe_data = {
                "alert": {
                    "attributes": [
                        {"name": "title", "type": "string"},
                        {"name": "description", "type": "string"}
                    ]
                },
                "audit": {
                    "attributes": []
                },
                "case": {
                    "attributes": [
                        {"name": "title", "type": "string"},
                        {"name": "description", "type": "string"},
                        {"name": "status", "type": "string"}
                    ]
                },
                "caseTemplate": {
                    "attributes": [
                        {"name": "name", "type": "string"},
                        {"name": "displayName", "type": "string"},
                        {"name": "description", "type": "string"}
                    ]
                },
                "customField": {
                    "attributes": [
                        {"name": "name", "type": "string"}
                    ]
                },
                "dashboard": {
                    "attributes": [
                        {"name": "title", "type": "string"}
                    ]
                },
                "log": {
                    "attributes": []
                },
                "observable": {
                    "attributes": [
                        {"name": "title", "type": "string"}
                    ]
                },
                "observableType": {
                    "attributes": [
                        {"name": "name", "type": "string"}
                    ]
                },
                "organisation": {
                    "attributes": [
                        {"name": "name", "type": "string"},
                        {"name": "description", "type": "string"}
                    ]
                },
                "pattern": {
                    "attributes": []
                },
                "procedure": {
                    "attributes": []
                },
                "profile": {
                    "attributes": [
                        {"name": "name", "type": "string"}
                    ]
                },
                "tag": {
                    "attributes": [
                        {"name": "name", "type": "string"}
                    ]
                },
                "task": {
                    "attributes": [
                        {"name": "title", "type": "string"}
                    ]
                },
                "taxonomy": {
                    "attributes": []
                },
                "user": {
                    "attributes": [
                        {"name": "login", "type": "string"},
                        {"name": "name", "type": "string"},
                        {"name": "organisation", "type": "string"},
                        {"name": "profile", "type": "string"}
                    ]
                },
                "job": {
                    "attributes": []
                },
                "action": {
                    "attributes": []
                }
            }
            return send_json(self, describe_data)

        # api/stream/<id>  → return empty event list so StreamSrv stays happy
        if p.startswith('api/stream'):
            return send_json(self, [])

        # api/user/current
        if p in ('api/user/current', 'api/v1/user/current', 'api/user'):
            return send_json(self, CURRENT_USER)

        # api/organisation list
        if p == 'api/organisation':
            return send_json(self, DB["organisations"])

        # api/organisation/<id>/links
        if '/links' in p and 'organisation' in p:
            return send_json(self, [])

        # api/organisation/<id>
        if p.startswith('api/organisation/'):
            org_id = p.split('/')[2] if len(p.split('/')) > 2 else None
            match = next((o for o in DB["organisations"] if o["name"] == org_id or o["_id"] == org_id), None)
            return send_json(self, match or {})

        # api/config/organisation (UiSettingsSrv)
        if 'api/config/organisation' in p or 'api/config' in p:
            return send_json(self, {})

        # api/ui
        if 'api/ui' in p:
            return send_json(self, {})

        # api/taxonomy
        if 'api/taxonomy' in p:
            return send_json(self, [])

        # api/profile
        if 'api/profile' in p:
            return send_json(self, DB["profiles"])

        # api/case
        if 'api/case' in p:
            return send_json(self, DB["cases"])

        # api/alert
        if 'api/alert' in p:
            return send_json(self, DB["alerts"])

        # api/dashboard
        if 'api/dashboard' in p:
            return send_json(self, {"data": []})

        # default api fallback
        return send_json(self, {})

    # ── POST ───────────────────────────────────────────────────────────────────
    def do_POST(self):
        raw_path = urllib.parse.unquote(self.path)
        # Separate path and query string
        url_path = raw_path.lstrip('/').split('?')[0]
        p = url_path.rstrip('/')
        body = read_body(self)

        if not p.startswith('api'):
            self.send_error(404)
            return

        # api/stream  → return a plain string stream ID (not an object!)
        if p == 'api/stream':
            return send_json(self, MOCK_STREAM_ID)

        # api/login / api/auth
        if 'api/login' in p or 'api/auth' in p:
            return send_json(self, CURRENT_USER)

        # api/v1/query or api/v0/query  (PaginatedQuerySrv / QuerySrv)
        if 'api/v1/query' in p or 'api/v0/query' in p:
            ops = body if isinstance(body, list) else body.get('query', [])
            name = ops[0].get('_name', '') if ops else ''

            res_list = []
            
            # Check for organisation-users query
            has_users = any(op.get('_name') == 'users' for op in ops)
            
            if has_users:
                org_op = next((op for op in ops if op.get('_name') == 'getOrganisation'), None)
                if org_op:
                    org_id = org_op.get('idOrName', '')
                    res_list = [u for u in DB["users"] if u.get("organisation") == org_id]
                else:
                    res_list = DB["users"]
            elif name == 'listOrganisation':
                res_list = DB["organisations"]
            elif name == 'getOrganisation':
                org_id = ops[0].get('idOrName', '')
                match = next((o for o in DB["organisations"] if o["name"] == org_id or o["_id"] == org_id), None)
                res_list = [match] if match else []
            elif name == 'listProfile':
                res_list = DB["profiles"]
            elif name == 'listCase':
                res_list = DB["cases"]
            elif name == 'listAlert':
                res_list = DB["alerts"]
            elif name in ('listUser', 'users'):
                res_list = DB["users"]
            elif name == 'freetags':
                res_list = []
            elif name == 'countUnreadAlert':
                res_list = [a for a in DB["alerts"] if not a.get("read", False)]
            elif name in ('myTasks', 'waitingTasks'):
                res_list = []
            else:
                res_list = []

            # Check if count is requested (either last op is 'count'/'limitedCount', or name has 'count')
            is_count = False
            if ops and ops[-1].get('_name') in ('count', 'limitedCount'):
                is_count = True
            elif 'count' in name.lower():
                is_count = True

            if is_count:
                return send_json(self, len(res_list))
            else:
                return send_json(self, res_list)

        # api/organisation  → create new org
        if p.startswith('api/organisation'):
            name = body.get("name", "")
            if not name:
                return send_json(self, {"type": "AuthorizationError", "message": "Name required"}, 400)
            if any(o["name"] == name for o in DB["organisations"]):
                return send_json(self, {"type": "Conflict", "message": "Organisation already exists"}, 409)
            new_org = {
                "_id": name,
                "name": name,
                "description": body.get("description", ""),
                "_createdAt": ts(),
                "_updatedAt": ts(),
                "_createdBy": "admin@cynox.local"
            }
            DB["organisations"].append(new_org)
            sys.stderr.write(f"[ORG CREATED] {name}\n")
            return send_json(self, new_org, 201)

        # api/case
        if p.startswith('api/case'):
            new_case = {**body, "_id": str(uuid.uuid4()), "_createdAt": ts()}
            DB["cases"].append(new_case)
            return send_json(self, new_case, 201)

        # default POST
        return send_json(self, {"status": "success", "_id": str(uuid.uuid4())})

    # ── PATCH ──────────────────────────────────────────────────────────────────
    def do_PATCH(self):
        raw_path = urllib.parse.unquote(self.path)
        url_path = raw_path.lstrip('/').split('?')[0]
        p = url_path.rstrip('/')
        body = read_body(self)
        if p.startswith('api/organisation/'):
            org_id = p.split('/')[2] if len(p.split('/')) > 2 else None
            for org in DB["organisations"]:
                if org["_id"] == org_id or org["name"] == org_id:
                    org.update(body)
                    return send_json(self, org)
        return send_json(self, {"status": "updated"})

    # ── DELETE ─────────────────────────────────────────────────────────────────
    def do_DELETE(self):
        raw_path = urllib.parse.unquote(self.path)
        url_path = raw_path.lstrip('/').split('?')[0]
        p = url_path.rstrip('/')
        if p.startswith('api/organisation/'):
            org_id = p.split('/')[2] if len(p.split('/')) > 2 else None
            before = len(DB["organisations"])
            DB["organisations"] = [o for o in DB["organisations"]
                                   if o["_id"] != org_id and o["name"] != org_id]
            sys.stderr.write(f"[ORG DELETED] {org_id}, removed {before - len(DB['organisations'])}\n")
        return send_json(self, {"status": "deleted"})

    def log_message(self, fmt, *args):
        sys.stderr.write(f"{self.address_string()} [{self.log_date_time_string()}] {fmt % args}\n")


# ── Start ──────────────────────────────────────────────────────────────────────
httpd = None
for port in range(PORT, PORT + 50):
    try:
        httpd = socketserver.TCPServer(("", port), LocalServerHandler)
        PORT = port
        break
    except OSError:
        continue

if not httpd:
    print("No open port found."); sys.exit(1)

print(f"====================================================")
print(f"   CYNOX 4  —  MOCK API + LOCAL STATIC SERVER    ")
print(f"====================================================")
print(f" Dir : {FRONTEND_DIR}")
print(f" Port: {PORT}")
print(f" URL : http://localhost:{PORT}/index.html")
print(f"====================================================")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
