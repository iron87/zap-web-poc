# ZAP Web Playground

Minimal playground for OWASP ZAP analysis with authentication.

It includes:
- Flask web app with form login and a protected area (`/private`).
- ZAP Automation Framework configuration with automatic login.
- Containerized setup with Docker Compose.
- Shell scripts to run the operational steps.

## Prerequisites

- Docker
- Docker Compose

## Demo credentials

- Username: `testuser`
- Password: `testpass`

## Structure

- `/app`: web application
- `/zap/automation.yaml`: ZAP plan (context, auth, spider, active scan, report)
- `/scripts`: execution scripts
- `/reports`: generated reports (created at runtime)

## Usage

1. Start the app:
```sh
./scripts/01-up.sh
```

2. Run the ZAP scan (with login):
```sh
./scripts/02-scan.sh
```

3. Stop the environment:
```sh
./scripts/03-down.sh
```

Full sequential run:
```sh
./scripts/00-all.sh
```

## Output

At the end of the scan, reports are available in:
- `reports/zap-report.html`
- `reports/zap-report.json`
