import urllib.request
import urllib.error

candidates = {
    "angular-markdown-editor-ghiscoding-js": [
        "https://unpkg.com/angular-markdown-editor@1.1.5/src/angular-markdown-editor.js",
        "https://unpkg.com/angular-markdown-editor@1.1.5/dist/angular-markdown-editor.min.js",
        "https://unpkg.com/angular-markdown-editor@1.1.5/angular-markdown-editor.js"
    ],
    "angular-markdown-editor-ghiscoding-css": [
        "https://unpkg.com/angular-markdown-editor@1.1.5/styles/angular-markdown-editor.css",
        "https://unpkg.com/angular-markdown-editor@1.1.5/dist/angular-markdown-editor.min.css",
        "https://unpkg.com/angular-markdown-editor@1.1.5/angular-markdown-editor.css"
    ],
    "angular-qr": [
        "https://unpkg.com/angular-qr@0.2.0/src/angular-qr.js",
        "https://unpkg.com/angular-qr@0.2.0/angular-qr.js",
        "https://unpkg.com/angular-qr@0.2.0/dist/angular-qr.min.js",
        "https://unpkg.com/angular-qr/angular-qr.js"
    ],
    "angular-page-loader-js": [
        "https://unpkg.com/angular-page-loader@0.2.2/dist/angular-page-loader.js",
        "https://unpkg.com/angular-page-loader/dist/angular-page-loader.js",
        "https://unpkg.com/angular-page-loader/angular-page-loader.js"
    ],
    "angular-page-loader-css": [
        "https://unpkg.com/angular-page-loader@0.2.2/dist/angular-page-loader.css",
        "https://unpkg.com/angular-page-loader/dist/angular-page-loader.css",
        "https://unpkg.com/angular-page-loader/angular-page-loader.css"
    ],
    "smalot-bootstrap-datetimepicker-js": [
        "https://unpkg.com/smalot-bootstrap-datetimepicker@2.4.4/js/bootstrap-datetimepicker.js",
        "https://unpkg.com/smalot-bootstrap-datetimepicker@2.4.4/js/bootstrap-datetimepicker.min.js",
        "https://unpkg.com/smalot-bootstrap-datetimepicker/js/bootstrap-datetimepicker.js",
        "https://unpkg.com/bootstrap-datetimepicker@2.4.4/js/bootstrap-datetimepicker.js"
    ],
    "smalot-bootstrap-datetimepicker-css": [
        "https://unpkg.com/smalot-bootstrap-datetimepicker@2.4.4/css/bootstrap-datetimepicker.css",
        "https://unpkg.com/smalot-bootstrap-datetimepicker/css/bootstrap-datetimepicker.css",
        "https://unpkg.com/bootstrap-datetimepicker/css/bootstrap-datetimepicker.css"
    ],
    "angular-images-resizer": [
        "https://unpkg.com/angular-images-resizer@2.0.3/src/angular-images-resizer.js",
        "https://unpkg.com/angular-images-resizer@2.0.3/dist/angular-images-resizer.js",
        "https://unpkg.com/angular-images-resizer/dist/angular-images-resizer.js"
    ],
    "ng-file-upload-js": [
        "https://unpkg.com/ng-file-upload@12.2.13/dist/ng-file-upload.js",
        "https://unpkg.com/ng-file-upload/dist/ng-file-upload.js"
    ],
    "ng-file-upload-shim-js": [
        "https://unpkg.com/ng-file-upload@12.2.13/dist/ng-file-upload-shim.js",
        "https://unpkg.com/ng-file-upload/dist/ng-file-upload-shim.js"
    ],
    "file-saver": [
        "https://unpkg.com/file-saver@1.3.4/FileSaver.js",
        "https://unpkg.com/file-saver@1.3.4/dist/FileSaver.js",
        "https://unpkg.com/file-saver/FileSaver.js",
        "https://unpkg.com/file-saver/dist/FileSaver.js"
    ],
    "js-url": [
        "https://unpkg.com/js-url@2.5.3/url.js",
        "https://unpkg.com/js-url/url.js",
        "https://unpkg.com/js-url@2.5.3/src/url.js",
        "https://unpkg.com/js-url@2.5.3/dist/url.js"
    ]
}

for name, urls in candidates.items():
    print(f"\nTesting candidates for {name}:")
    success = False
    for url in urls:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.getcode() == 200:
                    print(f"  [SUCCESS] {url}")
                    success = True
                    break
        except Exception:
            continue
    if not success:
        print("  [FAILED] No working candidate found!")
