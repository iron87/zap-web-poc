# ZAP Web Playground

Playground OWASP ZAP con due scenari separati:
- test `form-login`
- test `sso-local` (Keycloak + oauth2-proxy)

## Prerequisiti

- Docker
- Docker Compose

## Struttura

- `app/`: applicazione Flask target
- `tests/form-login/automation.yaml`: piano ZAP per login classico via form
- `tests/sso-local/automation.yaml`: piano ZAP per SSO locale funzionante
- `tests/sso-local/automation-external-idp-template.yaml`: template per IdP esterno (es. Office365/Entra)
- `keycloak/realm-playground.json`: realm importato con client e utente demo
- `scripts/form-login/`: script scenario form-login
- `scripts/sso-local/`: script scenario sso-local
- `reports/`: report generati

## Script per scenario

Form-login:
```sh
./scripts/form-login/01-up.sh
./scripts/form-login/02-scan.sh
./scripts/form-login/03-down.sh
```

Run completo form-login:
```sh
./scripts/form-login/00-all.sh
```

SSO locale:
```sh
./scripts/sso-local/02-scan.sh
./scripts/sso-local/03-down.sh
```

Run completo SSO locale:
```sh
./scripts/sso-local/00-all.sh
```

Nota compatibilita:
- i vecchi wrapper in `scripts/*.sh` restano disponibili e richiamano gli script nelle nuove cartelle.

## Credenziali demo

Form-login app:
- username: `testuser`
- password: `testpass`

SSO locale:
- Keycloak admin: `admin` / `admin` (`http://localhost:8090`)
- utente SSO: `demo-user` / `demo-pass`

## URL utili

- App: `http://localhost:8080`
- SSO browser entrypoint: `http://localhost:4180/private`
- Keycloak: `http://localhost:8090`

## Architettura SSO (Keycloak)

```text
Browser
  |
  | 1) GET /private
  v
sso-public (oauth2-proxy, localhost:4180)
  |
  | 2) redirect OIDC auth
  v
Keycloak (localhost:8090)
  |
  | 3) login utente + callback code
  v
sso-public (oauth2 callback)
  |
  | 4) exchange code -> token (verso keycloak interno)
  v
Keycloak (service DNS: keycloak:8080)
  |
  | 5) sessione valida, proxy verso upstream
  v
App Flask (app:8080)
```

Percorso ZAP (interno Docker):
```text
ZAP browser auth -> sso (service interno) -> Keycloak -> sso -> App
```

## File ZAP usati

Test form-login:
- `tests/form-login/automation.yaml`

Test SSO locale:
- `tests/sso-local/automation.yaml`
- richiamato da `scripts/sso-local/02-scan.sh`

Come fa login ZAP nel test SSO:
1. Usa `authentication.method: browser`.
2. Apre `loginPageUrl: http://sso:4180/private`.
3. Inserisce credenziali `demo-user` / `demo-pass`.
4. Segue redirect OIDC su Keycloak e callback.
5. Prosegue spider + active scan in sessione autenticata.

## A cosa serve `automation-external-idp-template`

`tests/sso-local/automation-external-idp-template.yaml` non e' un refuso:
- e' un esempio da copiare/adattare quando vuoi usare un IdP reale esterno (non il Keycloak locale).
- non viene usato dagli script di default.
- richiede sostituzione di URL, username/password e regole di verifica.

## Troubleshooting

Se dopo login vedi `500` su `localhost:4180`:
- causa tipica: mismatch issuer OIDC (`keycloak:8080` vs `localhost:8090`).
- in questo repo e' stato corretto su `sso-public` impostando:
  - `OAUTH2_PROXY_OIDC_ISSUER_URL=http://localhost:8090/realms/playground`

## Report output

- `reports/zap-report.html`
- `reports/zap-report.json`
- `reports/zap-sso-local-report.html`
- `reports/zap-sso-local-report.json`
