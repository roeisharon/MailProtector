# Local Setup Guide

[← Back to Main README](../README.md)

---

# Overview

This document describes how to run MailProtector locally with:

* FastAPI backend
* Gmail Add-on
* Google Apps Script
* ngrok HTTPS exposure

The setup flow is designed for local development and live Gmail testing.

---

# Prerequisites

Before starting, make sure the following tools are installed:

* Python 3.10+
* pip
* Google account with Gmail access

Optional but recommended:

* Python virtual environment support
* VS Code or another IDE

---

# Backend Setup

Clone the repository and enter the backend directory:

```bash id="tb4u9v"
git clone <repository-url>

cd MailProtector/backend
```

Create and activate a virtual environment:

## macOS / Linux

```bash id="p6e9j3"
python -m venv venv
source venv/bin/activate
```

## Windows

```bash id="l2w8nh"
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash id="x9m1rf"
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file inside the `backend/` directory.

Example:

```env id="f9m3qa"
OPENAI_API_KEY=your_openai_api_key
GOOGLE_SAFE_BROWSING_API_KEY=your_google_safe_browsing_key
```

The backend uses these credentials for:

* LLM explanation generation
* Google Safe Browsing checks

API keys can be generated from:

* [OpenAI Platform API Keys](https://platform.openai.com/api-keys?utm_source=chatgpt.com)
* [Google Safe Browsing API Setup](https://developers.google.com/safe-browsing/v4/get-started?utm_source=chatgpt.com)

Sensitive credentials should never be committed to the repository.

---

## Recommended `.gitignore`

The repository should exclude sensitive credentials and local development artifacts from version control.

Example entries:

```gitignore id="q3n7vz"
# Environment variables
.env
.env.*

# Python virtual environments
venv/
.venv/

# Python cache
__pycache__/
*.pyc

# IDE files
.vscode/
.idea/

# Logs
*.log
```

This helps prevent accidental exposure of secrets and keeps the repository clean from local development files.

---

# Running the Backend

Start the FastAPI backend:

```bash id="v1n6cw"
uvicorn main:app --reload
```

The backend should now be available locally at:

```text id="k8y2fd"
http://127.0.0.1:8000
```

Swagger documentation is available at:

```text id="f3r8pb"
http://127.0.0.1:8000/docs
```

The Swagger UI can be used to manually test the `/analyze` endpoint before connecting the Gmail Add-on.

You can send example phishing or safe email payloads directly through the API and inspect the generated verdicts and findings.

---

# Exposing the Backend with ngrok

The Gmail Add-on requires a publicly accessible HTTPS endpoint.

Since the backend runs locally, ngrok is used to expose the local FastAPI server to the internet.

## Installing ngrok

### macOS (Homebrew)

```bash id="m9q4vk"
brew install ngrok/ngrok/ngrok
```

Additional installation methods are available on:

[ngrok Official Website](https://ngrok.com/download?utm_source=chatgpt.com)

---

## Starting ngrok

Run:

```bash id="j6t4rh"
ngrok http 8000
```

Example output:

```text id="n2x5wu"
Forwarding https://example.ngrok-free.app -> http://localhost:8000
```

Copy the HTTPS forwarding URL.

This URL will later be configured inside the Gmail Add-on.

---

# Gmail Add-on Setup

Open:

[Google Apps Script](https://script.google.com?utm_source=chatgpt.com)

Create a new Apps Script project.

Inside the project, replace the default files with the contents of:

```text id="z4y9ec"
addon/
├── Code.gs
├── ui.gs
└── appsscript.json
```

---

# Updating the Backend URL

Replace the existing backend URL with your ngrok HTTPS forwarding URL.
Placeholders should be found in ```code.gs``` and ```appsscript.json```.

Example:

```javascript id="q7p2lx"
const BACKEND_URL = "https://example.ngrok-free.app/analyze";
```

The URL must use HTTPS in order for Gmail Add-ons to communicate with the backend service.

---

# Deploying the Gmail Add-on

Inside Google Apps Script:

1. Click **Deploy**
2. Select **Test deployments**
3. Choose **Gmail Add-on**
4. Authorize the requested Gmail permissions
5. Install the Add-on into your Gmail account

During the first installation attempt, Google may display a warning such as:

```text id="e8h3zs"
"Google hasn’t verified this app"
```

This is expected for local development and unpublished Apps Script projects.

To continue:

1. Click **Advanced**
2. Click **Go to project (unsafe)**
3. Approve the requested permissions

After deployment completes, reload Gmail.

The Add-on should now appear inside the Gmail sidebar.

---

# Testing the Add-on

To test the system:

1. Run the FastAPI backend
2. Start ngrok
3. Update the backend URL inside Apps Script
4. Deploy the Add-on
5. Open Gmail
6. Open an email
7. Launch the MailProtector Add-on
8. Run the analysis

The Add-on should display:

* Risk score
* Verdict
* Findings
* AI-generated explanation

Example test emails are available under:

```text id="r5k7mt"
examples/
```

---

# Troubleshooting

## ngrok URL Expired

Free ngrok URLs may change between sessions.

If the backend becomes unreachable:

1. Restart ngrok
2. Copy the new HTTPS URL
3. Update the Apps Script backend URL
4. Redeploy the Add-on

---

## Missing Environment Variables

If the backend fails during startup:

* Verify that the `.env` file exists
* Verify that API keys are valid
* Restart the backend after updating environment variables

---

## Gmail Add-on Not Updating

Sometimes Gmail caches previous deployments.

Try:

* Redeploying the Add-on
* Refreshing Gmail
* Removing and reinstalling the test deployment

---

## Backend Connection Errors

Verify:

* FastAPI backend is running
* ngrok tunnel is active
* The Apps Script backend URL matches the current ngrok URL
