import http.server
import socketserver
import sys
import os
import urllib.parse
import urllib.request
import urllib.error

PORT = 9000
FRONTEND_DIR = r"E:\Cynox New\Cynox-main\Cynox-main\frontend\app"
BACKEND_URL = "http://127.0.0.1:9001"

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
    "jquery-ui/jquery-ui.js": "https://unpkg.com/jquery-ui-dist@1.12.1/jquery-ui.js",
    "angular-ui-sortable/sortable.js": "https://unpkg.com/angular-ui-sortable@0.19.0/dist/sortable.js",
    "js-base64/base64.js": "https://unpkg.com/js-base64@2.5.2/base64.js",
    "angular-scroll/angular-scroll.js": "https://unpkg.com/angular-scroll@1.0.2/angular-scroll.js",
    "underscore.string/dist/underscore.string.js": "https://unpkg.com/underscore.string@3.3.5/dist/underscore.string.js",
    "angular-drag-and-drop-lists/angular-drag-and-drop-lists.js": "https://unpkg.com/angular-drag-and-drop-lists@2.1.0/angular-drag-and-drop-lists.js",
    "angular-bootstrap-colorpicker/js/bootstrap-colorpicker-module.js": "https://unpkg.com/angular-bootstrap-colorpicker@3.0.32/js/bootstrap-colorpicker-module.js",
    "angular-bootstrap-colorpicker/css/colorpicker.css": "https://unpkg.com/angular-bootstrap-colorpicker@3.0.32/css/colorpicker.css",
    "file-saver/FileSaver.js": "https://unpkg.com/file-saver@1.3.4/dist/FileSaver.js",
    "js-url/url.js": "https://unpkg.com/js-url/url.js",
    "bootstrap-sass/assets/javascripts/bootstrap.js": "https://unpkg.com/bootstrap@3.4.1/dist/js/bootstrap.js",
    "angular-bootstrap-multiselect/dist/angular-bootstrap-multiselect.js": "https://unpkg.com/angular-bootstrap-multiselect@1.1.11/dist/angular-bootstrap-multiselect.js",
    "qrcode.js/lib/qrcode.js": "https://unpkg.com/qrcode-generator@1.4.4/qrcode.js",
    "qrcode/lib/qrcode.js": "https://unpkg.com/qrcode-generator@1.4.4/qrcode.js",
    "angular-qr/src/angular-qr.js": "https://unpkg.com/angular-qrcode/angular-qrcode.js",
    "animate.css/animate.css": "https://unpkg.com/animate.css@3.7.2/animate.css",
    "roboto-fontface/css/roboto/roboto-fontface.css": "https://unpkg.com/roboto-fontface@0.10.0/css/roboto/roboto-fontface.css",
    "css-spaces/dist/spaces.css": "https://unpkg.com/css-spaces@0.3.5/dist/spaces.css",
    "bower_components/smalot-bootstrap-datetimepicker/css/bootstrap-datetimepicker.css": "https://cdnjs.cloudflare.com/ajax/libs/smalot-bootstrap-datetimepicker/2.4.4/css/bootstrap-datetimepicker.min.css",
    "bower_components/smalot-bootstrap-datetimepicker/js/bootstrap-datetimepicker.min.js": "https://cdnjs.cloudflare.com/ajax/libs/smalot-bootstrap-datetimepicker/2.4.4/js/bootstrap-datetimepicker.min.js",
    "bower_components/cryptojslib/components/core-min.js": "https://unpkg.com/crypto-js@3.1.9-1/core.js",
    "bower_components/cryptojslib/components/sha256-min.js": "https://unpkg.com/crypto-js@3.1.9-1/sha256.js",
    "bower_components/cryptojslib/components/md5-min.js": "https://unpkg.com/crypto-js@3.1.9-1/md5.js",
    "bower_components/ace-builds/src-min-noconflict/ace.js": "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js"
}

class CynoxProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    # ── OPTIONS (CORS preflight) ───────────────────────────────────────────────
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,X-Organisation')
        self.end_headers()

    # ── Proxy method to Docker Backend ───────────────────────────────────────
    def do_proxy(self):
        url = f"{BACKEND_URL}{self.path}"
        headers = {}
        for k, v in self.headers.items():
            if k.lower() not in ('host', 'content-length'):
                headers[k] = v

        # Read body if present
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # Translate incoming username domain if necessary (admin@cynox.local -> admin@thehive.local)
        if body and self.headers.get('Content-Type', '').startswith('application/json'):
            try:
                text = body.decode('utf-8', errors='ignore')
                text = text.replace("cynox.local", "thehive.local")
                text = text.replace("Cynox system user", "Cynox system user")
                body = text.encode('utf-8')
            except Exception:
                pass

        req = urllib.request.Request(url, data=body, headers=headers, method=self.command)
        
        try:
            with urllib.request.urlopen(req) as resp:
                self.send_response(resp.status)
                content_type = ""
                for k, v in resp.getheaders():
                    if k.lower() == 'content-type':
                        content_type = v
                    if k.lower() not in ('transfer-encoding', 'content-length'):
                        self.send_header(k, v)
                
                resp_body = resp.read()
                
                # Apply target translations for UI display
                # Replace 'Cynox system user' and domain names in JSON response
                if 'application/json' in content_type or 'text/' in content_type:
                    try:
                        text = resp_body.decode('utf-8', errors='ignore')
                        text = text.replace("Cynox system user", "Cynox system user")
                        text = text.replace("thehive.local", "cynox.local")
                        resp_body = text.encode('utf-8')
                    except Exception as e:
                        sys.stderr.write(f"[outgoing translation error] {e}\n")
                        
                self.send_header('Content-Length', str(len(resp_body)))
                self.end_headers()
                self.wfile.write(resp_body)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for k, v in e.headers.items():
                if k.lower() not in ('transfer-encoding', 'content-length'):
                    self.send_header(k, v)
            resp_body = e.read()
            self.send_header('Content-Length', str(len(resp_body)))
            self.end_headers()
            self.wfile.write(resp_body)
        except Exception as e:
            self.send_response(502)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<h2>Cynox Server Error</h2><p>Failed to connect to the Docker backend on port 9001: {e}</p><p>Please ensure that Docker containers are running.</p>".encode())

    # ── Intercept Requests ───────────────────────────────────────────────────
    def handle_request(self):
        raw_path = urllib.parse.unquote(self.path)
        url_path = raw_path.lstrip('/').split('?')[0]
        p = url_path.rstrip('/')

        # 1. Check if it's an API route -> Proxy to Docker
        if p.startswith('api'):
            self.do_proxy()
            return

        # 2. Intercept and patch angular-qr
        if "angular-qr/src/angular-qr.js" in url_path:
            try:
                url = "https://unpkg.com/angular-qr@0.2.2/src/angular-qr.js"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    content = response.read().decode('utf-8')
                content = content.replace("var qrcode = require('qrcode-genetator');", "var qrcode = window.qrcode || window.QRCode;")
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

        # 3. Intercept and patch angular-page-loader
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

        # 4. Redirect bower components to CDN
        for pattern, cdn_url in BOWER_MAPPINGS.items():
            if url_path.startswith(pattern):
                self.send_response(307)
                self.send_header('Location', cdn_url)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                return

        if url_path.startswith("bower_components/"):
            rest = url_path.replace("bower_components/", "", 1)
            target_url = f"https://unpkg.com/{rest}"
            self.send_response(307)
            self.send_header('Location', target_url)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            return

        # 5. Serve static files normally if the file exists on disk
        disk_path = os.path.join(FRONTEND_DIR, p)
        if os.path.isfile(disk_path):
            super().do_GET()
            return

        # 6. SPA fallback: Serve local index.html for all non-file requests
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

        # Fallback
        super().do_GET()

    def do_GET(self):
        self.handle_request()
    def do_POST(self):
        self.handle_request()
    def do_PUT(self):
        self.handle_request()
    def do_PATCH(self):
        self.handle_request()
    def do_DELETE(self):
        self.handle_request()

# ── Start Server ───────────────────────────────────────────────────────────
httpd = None
try:
    httpd = socketserver.TCPServer(("", PORT), CynoxProxyHandler)
except OSError as e:
    print(f"Error starting server on port {PORT}: {e}")
    sys.exit(1)

print(f"====================================================")
print(f"       CYNOX CUSTOM FRONTEND PROXY SERVER           ")
print(f"====================================================")
print(f" Serving UI from: {FRONTEND_DIR}")
print(f" Proxying API to: {BACKEND_URL}")
print(f" Local URL      : http://localhost:{PORT}/index.html")
print(f"====================================================")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
