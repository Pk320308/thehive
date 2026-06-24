#!/bin/sh
echo '{"password":"Cynox@123"}' | curl -s -X POST \
  -u "admin@thehive.local:secret" \
  -H "Content-Type: application/json" \
  -d @- \
  http://localhost:9000/api/user/admin@thehive.local/password/set
echo ""
echo "Done."
