# ZAP Web Playground

OWASP ZAP playground with two separate scenarios:
- `form-login` test
- `sso-local` test (Keycloak + oauth2-proxy)

## Prerequisites

- Docker
- Docker Compose

## Structure

- `app/`: target Flask application
- `tests/form-login/automation.yaml`: ZAP plan for classic form login
- `tests/sso-local/automation.yaml`: ZAP plan for working local SSO
- `tests/sso-local/automation-external-idp-template.yaml`: template for external IdP (e.g. Office365/Entra)
- `keycloak/realm-playground.json`: imported realm with demo client and user
- `scripts/form-login/`: scripts for the form-login scenario
- `scripts/sso-local/`: scripts for the sso-local scenario
- `reports/`: generated reports

## Scripts by scenario

Form-login:
```sh
./scripts/form-login/01-up.sh
./scripts/form-login/02-scan.sh
./scripts/form-login/03-down.sh
```

Full form-login run:
```sh
./scripts/form-login/00-all.sh
```

Local SSO:
```sh
./scripts/sso-local/02-scan.sh
./scripts/sso-local/03-down.sh
```

Full local SSO run:
```sh
./scripts/sso-local/00-all.sh
```

Compatibility note:
- old wrappers in `scripts/*.sh` are still available and call scripts in the new folders.

## Demo credentials

Form-login app:
- username: `testuser`
- password: `testpass`

Local SSO:
- Keycloak admin: `admin` / `admin` (`http://localhost:8090`)
- SSO user: `demo-user` / `demo-pass`

## Useful URLs

- App: `http://localhost:8080`
- SSO browser entrypoint: `http://localhost:4180/private`
- Keycloak: `http://localhost:8090`

## SSO Architecture (Keycloak)

```text
Browser
  |
  | 1) GET /private
  v
sso-public (oauth2-proxy, localhost:4180)
  |
  | 2) OIDC auth redirect
  v
Keycloak (localhost:8090)
  |
  | 3) user login + callback code
  v
sso-public (oauth2 callback)
  |
  | 4) code -> token exchange (against internal keycloak)
  v
Keycloak (service DNS: keycloak:8080)
  |
  | 5) valid session, proxy to upstream
  v
App Flask (app:8080)
```

ZAP path (inside Docker):
```text
ZAP browser auth -> sso (internal service) -> Keycloak -> sso -> App
```

## ZAP files used

Form-login test:
- `tests/form-login/automation.yaml`

Local SSO test:
- `tests/sso-local/automation.yaml`
- called by `scripts/sso-local/02-scan.sh`

How ZAP logs in during the SSO test:
1. It uses `authentication.method: browser`.
2. It opens `loginPageUrl: http://sso:4180/private`.
3. It submits credentials `demo-user` / `demo-pass`.
4. It follows OIDC redirects to Keycloak and callback.
5. It runs passive scan first (`passiveScan-wait`) on collected responses.
6. It continues with active scan as an authenticated session.

Job order used in tests:
- `spider -> passiveScan-wait -> activeScan -> report`

## What `automation-external-idp-template` is for

`tests/sso-local/automation-external-idp-template.yaml` is not a typo:
- it is an example to copy/adapt when using a real external IdP (not local Keycloak)
- it is not used by default scripts
- it requires replacing URLs, username/password, and verification rules

## Report output

- `reports/zap-report.html`
- `reports/zap-report.json`
- `reports/zap-sso-local-report.html`
- `reports/zap-sso-local-report.json`
