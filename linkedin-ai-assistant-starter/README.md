# LinkedIn AI Assistant (Local, Compliant)

A step‑by‑step starter you can run **entirely on your laptop**. It helps you draft high‑quality replies for LinkedIn messages
without auto‑sending anything (to stay within platform rules). You can use the **Streamlit app** (copy‑paste workflow) or an optional **Chrome extension** that inserts drafts for you to review and send manually.

> ⚠️ **Policy note**: This project **does not** auto‑message other users. It only drafts responses that **you** send. Any automated messaging or scraping may violate LinkedIn’s Terms. Use the Chrome extension here only to **insert text you approve**.

---

## What you’ll build

- **FastAPI backend** running locally, powered by an LLM (OpenAI by default; you can swap providers).
- **Streamlit UI** for a copy‑paste workflow: paste conversation → choose tone → get a polished draft → click to copy.
- **Chrome extension (optional)** that adds a “Draft with AI” button on LinkedIn’s message page. It collects the on‑screen conversation, asks your local backend for a suggested reply, and **inserts** the draft in the compose area. **You still click Send.**

---

## Prerequisites

- Windows/macOS/Linux with **Python 3.9+**
- A text editor (VS Code recommended)
- **OpenAI API key** (or another LLM; see `.env.example`)

---

## 1) Backend Setup (FastAPI)

1. Open a terminal in the project folder and run:

   ```bash
   cd backend
   python -m venv .venv
   # On Windows: .venv\\Scripts\\activate
   # On macOS/Linux:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and set your API key and model:

   ```env
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o-mini
   PORT=8000
   ```

3. Start the server:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. Test in your browser: open `http://localhost:8000/docs` to try endpoints.

---

## 2) Streamlit App (Copy‑Paste Workflow)

In a **separate terminal**:

```bash
cd frontend_streamlit
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

- Paste a LinkedIn conversation (or any text).
- Choose tone (friendly, formal, concise, etc.).
- Click **Generate Reply** → review → **Copy to clipboard** → paste back into LinkedIn and send.

---

## 3) Chrome Extension (Optional, Manual‑send Only)

This adds a small floating button on LinkedIn messages to draft a reply and insert it into the compose box.

1. Ensure your backend is running on `http://localhost:8000`.
2. Open **Chrome** → go to `chrome://extensions` → **Developer mode** → **Load unpacked**.
3. Select the folder: `chrome_extension/`.
4. Go to LinkedIn messages (`https://www.linkedin.com/messaging/`). You’ll see a small **Draft with AI** button at the bottom right.
5. Click it → it reads the visible messages, asks your local backend for a draft, and inserts it in the compose area. **You must still click Send**.

> 🔧 **If the button doesn’t appear**: LinkedIn’s HTML can change. Use the extension’s popup (click the extension icon → “Draft with AI”) to trigger drafting for the current tab.

---

## 4) Customization

- **Prompt style**: Edit `backend/prompts.py`.
- **Max length** / tone options: Edit `backend/main.py` and `frontend_streamlit/app.py`.
- **LLM provider**: Replace OpenAI client in `backend/llm_client.py` with your preferred API.

---

## 5) Safety & Compliance (Important)

- Keep human‑in‑the‑loop: **only you send** messages.
- Avoid scraping or auto‑sending. Respect platform rules and recipients’ preferences.
- Log errors locally; don’t log private message content in production settings.

---

## 6) Troubleshooting

- **CORS/Network**: If the extension can’t reach the backend, confirm `http://localhost:8000` is reachable and CORS is enabled in `backend/main.py`.
- **Selectors**: If insertion fails, LinkedIn changed the DOM. Adjust `querySelectors` in `chrome_extension/content.js`.
- **API Errors**: Check your `.env` values and rate limits.

---

## 7) File Map

```
backend/
  main.py
  llm_client.py
  prompts.py
  requirements.txt
  .env.example
frontend_streamlit/
  app.py
  requirements.txt
chrome_extension/
  manifest.json
  content.js
  popup.html
  popup.js
  styles.css
```

---

Made for local development and learning.