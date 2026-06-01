# Automated CLI GitHub Committer

This CLI handles git init, commits, and pushes so you never need to type git commands after setup.

## Prerequisites
- Git installed and on PATH
- Python 3.9+
- GitHub authentication configured (HTTPS + PAT or Git Credential Manager)

## Setup
1. Create a GitHub repository (empty is fine).
2. From this folder:

```bash
python autocommit.py setup --remote https://github.com/<user>/<repo>.git
```

This initializes the repo, creates an initial commit (if files exist), pushes to GitHub, and writes `.autocommit.json`.

## Run
Start the auto-committer (no git commands needed):

```bash
python autocommit.py run
```

Optional single pass:

```bash
python autocommit.py run --once
```

## Config
The config file is `.autocommit.json` and includes:
- `remote`
- `branch`
- `interval` (seconds between checks)
- `message_prefix`

Update the file or pass `--interval` / `--message` to override on a run.

## Desktop App (Tkinter)
Run the desktop app and use the buttons instead of typing git commands:

```bash
python autocommit_gui.py
```

1. Choose the folder you want to watch.
2. Enter the GitHub remote URL and click **Setup Repo** once.
3. Click **Start Watching** to auto-commit on changes.
