# setting up gmail oauth for ai‑daily‑brief‑service

this guide walks you through creating the necessary gmail oauth credentials and adding them as github repository secrets so the `emailer` module can send the daily brief.

## 1. create a google cloud project

1. go to the [google cloud console](https://console.cloud.google.com/).
2. create a new project (or use an existing one).
3. enable the **gmail api** for the project (search for "gmail api" in the API library and click enable).

## 2. configure oauth consent screen

1. navigate to **apis & services → oauth consent screen**.
2. choose "external" (unless you only need internal usage).
3. fill in the required fields (app name, user support email, developer contact email).
4. add the scopes `https://www.googleapis.com/auth/gmail.send`.
5. save.

## 3. create oauth client credentials

1. go to **apis & services → credentials**.
2. click **create credentials → oauth client id**.
3. select "web application".
4. set an authorized redirect URI – for a simple script you can use `urn:ietf:wg:oauth:2.0:oob` (out‑of‑band) or `http://localhost`.
5. click create – you will receive a **client id** and **client secret**.

## 4. obtain a refresh token

you can use the provided `get_gmail_service` helper in `src/emailer.py` to perform the oauth flow, or use the following quick script:

```bash
pip install --quiet google-auth-oauthlib google-auth-httplib2
python - <<'PY'
from google_auth_oauthlib.flow import InstalledAppFlow
import os, json
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
flow = InstalledAppFlow.from_client_config({
    "installed": {
        "client_id": os.getenv('GMAIL_CLIENT_ID'),
        "client_secret": os.getenv('GMAIL_CLIENT_SECRET'),
        "redirect_uris": ['urn:ietf:wg:oauth:2.0:oob'],
        "auth_uri": 'https://accounts.google.com/o/oauth2/auth',
        "token_uri": 'https://oauth2.googleapis.com/token'
    }
}, SCOPES)
creds = flow.run_console()
print('refresh token:', creds.refresh_token)
PY
```

run the script with the environment variables `GMAIL_CLIENT_ID` and `GMAIL_CLIENT_SECRET` set to the values from step 3. copy the printed **refresh token**.

## 5. add github secrets

in your repository on github, go to **settings → secrets and variables → actions → new repository secret** and add the following secrets:

- `GMAIL_CLIENT_ID` – the client id from step 3
- `GMAIL_CLIENT_SECRET` – the client secret from step 3
- `GMAIL_REFRESH_TOKEN` – the refresh token obtained in step 4
- `DAILY_BRIEF_RECIPIENTS` – a comma‑separated list of email addresses that should receive the brief (e.g., `alice@example.com,bob@example.com`)

## 6. test the pipeline

once the secrets are set, you can manually trigger the **daily** workflow from the github actions tab, or run the orchestrator locally:

```bash
source .venv/bin/activate
python src/orchestrator.py
```

if everything is configured correctly, you should receive an email with the daily AI research brief.

---

*the above steps assume you have an existing gmail account and are comfortable with creating google cloud projects. feel free to ask if any step is unclear.*