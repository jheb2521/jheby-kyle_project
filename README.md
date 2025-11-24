# QUPAL-like Tkinter UI

This small Python example recreates the visual look of the provided QUPAL screenshot using Tkinter and includes a simple local chatbot.

Files:

- `main.py` — Tkinter GUI that approximates the screenshot UI (logo, header, chat bubbles, input bar). Now supports a scrollable message history, resizable layout, and a simple chatbot.
- `requirements.txt` — Notes (no external pip dependencies required; uses the standard library `tkinter`).

How to run (Windows PowerShell):

```powershell
cd "C:\Users\JHEB\Downloads\Grp5"
python .\main.py
```

What's new

- Message history stacking: messages you send and the assistant replies are added to a scrollable history.
- Resizable UI: the chat area and message stack resize with the window.
- Simple chatbot responder: a rule-based responder is built-in. If you provide the environment variable `OPENAI_API_KEY` and have the `openai` package installed, the app will attempt an OpenAI completion call; if that fails or is not configured it falls back to the local rule-based responder.

Notes

- Tkinter is included with most standard Python installs. If your Python doesn't include it, install the appropriate system package (e.g., `python3-tk` on some Linux distributions).
- The OpenAI integration is optional. If you want to use it, install the `openai` package and set `OPENAI_API_KEY` in your environment. Example (PowerShell):

```powershell
pip install openai
$env:OPENAI_API_KEY = 'sk-...'
python .\main.py
```

- The application is a visual mock and demo — it doesn't persist messages to disk or connect to an external message store.

If you'd like, I can:

- Add message persistence (save/load history to JSON).
- Wire a real backend or integrate a deployment-ready OpenAI usage pattern (with safety checks and streaming).
- Improve the visual polish (rounded-bubble images, avatars, animated typing indicator).

Enjoy! If you want one of the follow-ups, tell me which and I’ll implement it.

Front-end mock (static HTML/CSS)

I added a static front-end you can open directly in your browser to better match the screenshot UI.

Files added:

- `frontend/index.html` — a responsive HTML mock that reproduces the top header, message bubble, and input bar layout.
- `frontend/styles.css` — styling for the front-end to match spacing, colors, rounded bubbles, and the turquoise send button.

How to open the front-end (Windows):

```powershell
cd "C:\Users\JHEB\Downloads\Grp5\frontend"
start .\index.html
```

Behavior notes:

- The page includes a small JavaScript snippet that stacks messages (user and assistant) and simulates a quick rule-based reply.
- This is a client-side mock (no backend). If you'd like I can wire it to the Python backend (`main.py`) or a real API.

Admin runtime API key (optional)

If you prefer not to set `OPENAI_API_KEY` as an environment variable, you can set the key at runtime using a localhost-only admin endpoint. This stores the key in the running process only (not in files) and requires an admin token.

1. Choose an admin token and set it in PowerShell (only required once):

```powershell
[Environment]::SetEnvironmentVariable('ADMIN_TOKEN','my-secret-token','User')
```

2. Start the server (without pasting API keys into files or chat):

```powershell
cd "C:\Users\JHEB\Downloads\Grp5"
python server.py
```

3. From the same machine, set the OpenAI key at runtime (replace values):

```powershell
# send the key to the running server (localhost only)
curl -X POST http://127.0.0.1:5000/admin/set_key -H "Content-Type: application/json" -d '{"key":"sk-...","admin_token":"my-secret-token"}'
```

4. To clear the key from the running server process:

```powershell
curl -X POST http://127.0.0.1:5000/admin/clear_key -H "Content-Type: application/json" -d '{"admin_token":"my-secret-token"}'
```

Security notes:

- The admin endpoints only accept requests from localhost and require the `ADMIN_TOKEN` (set in your user environment). This avoids embedding keys in code or sharing them in chat.
- Never paste API keys in chat. Use the admin endpoint or environment variables on your machine.
