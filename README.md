# EnableAI

A small terminal chatbot that uses OpenRouter to generate AI responses. The app provides local user login/registration, saves per-user conversation history, and supports pluggable CLI "tools" via a tools registry.

## Features
- CLI chatbot powered by OpenRouter
- Local user registration and password hashing
- Per-user conversation history stored on disk
- Extensible commands via a tools registry (tools/registry.py -> TOOLS)

## Quickstart (minimum)
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Provide your OpenRouter API key (recommended: use environment variable):

   Option A — Environment variable (recommended):
   ```bash
   export OPENROUTER_API_KEY="sk-..."
   ```
   Then update `chatbot.py` to read the key from the environment (example shown below).

   Option B — .env file (local development only):
   - Create a file named `.env` and add:
     ```env
     OPENROUTER_API_KEY=sk-...
     ```
   - Do NOT commit `.env` to source control. Add `.env` to `.gitignore`.

   Example change in `chatbot.py` to load the key from the environment:
   ```python
   import os
   API_KEY = os.environ.get("OPENROUTER_API_KEY")
   if not API_KEY:
       raise RuntimeError("Set OPENROUTER_API_KEY in environment before running.")
   client = OpenRouter(API_KEY)
   ```

3. Run the chatbot:
   ```bash
   python chatbot.py
   ```

## Prerequisites
- Python 3.10+ (or latest stable supported interpreter)
- An OpenRouter API key (sign up at OpenRouter if you don't have one)

## Configuration & environment
The app expects an OpenRouter API key. Recommended approaches:
- Preferred: set `OPENROUTER_API_KEY` in your shell environment as shown above.
- Alternative: keep a local `.env` for development and load it with a library like `python-dotenv`, but never commit the file.

## Repository layout (relevant files)
- `chatbot.py` — CLI entrypoint, login flow, message loop, OpenRouter client usage
- `auth.py` — user registration/login, password hashing, save/load users
- `memory.py` — save/load per-user conversation history under `data/users/<username>/`
- `help.py` — prints available tool commands
- `tools/registry.py` — (not present yet) should export `TOOLS` dict mapping command strings to handler functions

## Data storage
- Users are stored under `data/users/` (e.g., `data/users/<username>/users.json` or `data/users/<username>/history.json`)
- Do not commit `data/` to version control. Add a `.gitignore` entry (example below).

Example `.gitignore` entries:
```
/data/
/.venv/
/.env
```

## Troubleshooting
- "KEY not defined" at startup: set `OPENROUTER_API_KEY` and ensure `chatbot.py` reads it.
- ImportError for `tools.registry`: add `tools/registry.py` or remove/change the import.
- Permission/IO errors saving files: ensure `data/` directory exists and is writable.
