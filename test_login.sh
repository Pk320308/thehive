#!/bin/sh
# Test login with default credentials
RESULT=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"user":"admin@thehive.local","password":"secret"}' \
  http://localhost:9000/api/login)
echo "Login test result: $RESULT"
