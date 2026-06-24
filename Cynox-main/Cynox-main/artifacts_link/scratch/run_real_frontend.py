import http.server
import socketserver
import os
import sys
import json
import urllib.parse

PORT = 8085
# Resolve absolute path to the original frontend app folder
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

# In-memory mock database for API requests
MOCK_CASES = [
    {
        "id": "1",
        "title": "Anomalous PowerShell Execution Detected",
        "description": "An unusual PowerShell process was launched by web server user.",
        "severity": "High",
        "tlp": "Amber",
        "status": "Open",
        "assignee": "admin@cynox.local",
        "startDate": 1779875402000
    },
    {
        "id": "2",
        "title": "SSH Brute Force from Internal IP",
        "description": "High frequency authentication failures detected from subnet 10.0.4.0/24.",
        "severity": "Medium",
        "tlp": "Green",
        "status": "Open",
        "assignee": "analyst@cynox.local",
        "startDate": 1779875102000
    }
]

MOCK_ALERTS = [
    {
        "id": "101",
        "title": "Ransomware Ransom Note File Created",
        "description": "EDR flagged decrypt_instructions.txt generation.",
        "severity": "High",
        "tlp": "Red",
        "source": "EDR-Sentinel",
        "date": 1779875302000
    }
]

class PreprocessorHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_GET(self):
        # Decode URL path
        url_path = urllib.parse.unquote(self.path).lstrip('/')
        
        # 1. Intercept Bower requests and redirect them to UNPKG/CDN
        for pattern, cdn_url in BOWER_MAPPINGS.items():
            if url_path.startswith(pattern):
                self.send_response(307)
                self.send_header('Location', cdn_url)
                self.end_headers()
                return

        # Fallback for dynamic bower component redirects
        if url_path.startswith("bower_components/"):
            rest = url_path.replace("bower_components/", "", 1)
            target_url = f"https://unpkg.com/{rest}"
            self.send_response(307)
            self.send_header('Location', target_url)
            self.end_headers()
            return

        # 2. Intercept API Endpoints to return Mock JSON and satisfy routing
        if url_path.startswith("api/") or url_path.startswith("./api/") or "api/user/current" in url_path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Match specific API calls
            if "api/user/current" in url_path or "api/user" in url_path:
                user_data = {
                    "login": "admin@cynox.local",
                    "name": "Administrator",
                    "organisation": "admin",
                    "profile": "admin",
                    "roles": ["admin", "read", "write"],
                    "permissions": ["managePlatform", "manageProfile", "manageTaxonomy", "manageOrganisation", "manageUser", "manageCaseTemplate", "manageCustomField", "manageObservableTemplate"]
                }
                self.wfile.write(json.dumps(user_data).encode())
            elif "api/config" in url_path:
                config_data = {
                    "version": "4.1.24",
                    "cortex": False,
                    "misp": False
                }
                self.wfile.write(json.dumps(config_data).encode())
            elif "api/ui" in url_path:
                self.wfile.write(json.dumps({}).encode())
            elif "api/taxonomy" in url_path:
                self.wfile.write(json.dumps([]).encode())
            elif "api/case" in url_path:
                self.wfile.write(json.dumps(MOCK_CASES).encode())
            elif "api/alert" in url_path:
                self.wfile.write(json.dumps(MOCK_ALERTS).encode())
            elif "api/dashboard/metadata" in url_path:
                self.wfile.write(json.dumps({}).encode())
            elif "api/dashboard" in url_path:
                self.wfile.write(json.dumps({"data": []}).encode())
            else:
                # Default empty JSON fallback
                self.wfile.write(json.dumps({}).encode())
            return

        # 3. Serve standard files from the frontend/app directory
        super().do_GET()

    def do_POST(self):
        url_path = urllib.parse.unquote(self.path).lstrip('/')
        
        # Intercept POST API calls like login or case updates
        if url_path.startswith("api/"):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
            return
            
        self.send_error(404, "File Not Found")

    def log_message(self, format, *args):
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

# Port selection scan
httpd = None
for p in range(PORT, PORT + 50):
    try:
        httpd = socketserver.TCPServer(("", p), PreprocessorHttpRequestHandler)
        PORT = p
        break
    except OSError:
        continue

if httpd is None:
    print("Could not find an open port.")
    sys.exit(1)

print(f"====================================================")
print(f"   CYNOX 4 - ORIGINAL FRONTEND LIVE PREVIEW       ")
print(f"====================================================")
print(f" Base Directory: {FRONTEND_DIR}")
print(f" Port Allocated: {PORT}")
print(f" Open in Browser: http://localhost:{PORT}/index.html")
print(f" No modifications made to any files under project folder.")
print(f"====================================================")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nStopping preview server. Goodbye!")
except Exception as e:
    print(f"Error: {e}")
