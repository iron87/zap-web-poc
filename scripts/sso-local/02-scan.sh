#!/usr/bin/env sh
set -eu

docker compose up -d app keycloak sso sso-public

echo "Waiting for Keycloak..."
until curl -fsS http://localhost:8090/realms/playground/.well-known/openid-configuration >/dev/null 2>&1; do
  sleep 2
done

echo "Waiting for SSO gateway..."
until curl -fsS http://localhost:4180/oauth2/sign_in >/dev/null 2>&1; do
  sleep 2
done

mkdir -p reports

docker compose run --rm --no-deps zap \
  zap.sh -cmd -autorun /zap/wrk/tests/sso-local/automation.yaml

echo "Local SSO scan completed. Reports in ./reports"
