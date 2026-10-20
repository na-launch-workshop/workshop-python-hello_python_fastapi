# 🚀 **Module: FastAPI Hello World Translation Service**

**Technology Stack:**

- Python

---

## 🎯 **Scenario**

This project mirrors the Node.js translation service from `workshop-nodejs-hello_nodejs`, delivering the same behaviour using Python and FastAPI. It exposes a single endpoint that returns a localized greeting with an ISO-8601 timestamp appended.

---

## Prerequisites
- Python 3.10 or newer
- pip

---

## 🐾 **Guided Walkthrough**

1. Installation
Create a virtual environment and install the development dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

2. Running the Tests
```bash
python -m pytest
```

3. Starting the Service
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```
The server listens on port `8080` by default. Override with the `PORT` environment variable if needed.

4. HTTP Endpoint
- `GET /` – Responds with a greeting string such as `hello world @ 2024-06-01T12:34:56.000Z`.
- `GET /eggs` – 🥚 See below.

5. Configuration
Environment variables provide the same configurability as the Node.js version:
- `TRANSLATION_DEFAULT_LANGUAGE` (default: `EN`) – Two-letter code used to choose the greeting.
- `TRANSLATION_FILE` (default: `translations.json`) – File located in the `resources/` directory that contains the greeting map.
- `PORT` (default: `8080`) – Port for the HTTP server.

All translations are stored in `resources/translations.json`, copied verbatim from the Node.js project.

---

## 🥚 **Easter Egg!**

One egg is hidden in this service. Start the service, then ask it for the riddle at `/eggs`.

From a terminal in your workspace:

```bash
curl http://localhost:8080/eggs
```

In **OpenShift Dev Spaces**, open the `hello-by-lang` endpoint from the Endpoints view and add `/eggs` to the end of the URL.

- [ ] 🥚 Find the easter egg – *"The translation file holds 85 greetings, but the service knows a few it never wrote down. Pirates can read them."*

You will know you found it when the service hands you a trophy. 🏆

**House rules:** reading `app/easter_eggs.py` is cheating (and it is encoded anyway). The response headers, however, are fair game. 🐣
