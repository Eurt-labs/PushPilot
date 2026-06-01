# Automated GitHub Committer (CLI + Desktop App)

Automatically detects changes in a folder, commits them, and pushes to GitHub. Use the **desktop application** (GUI), the **Python CLI**, or a **single EXE** that supports both.

## Links
- Git: https://git-scm.com/downloads
- Python: https://www.python.org/downloads/
- Git Credential Manager (recommended): https://github.com/git-ecosystem/git-credential-manager
- PyPI: https://pypi.org/
- PyInstaller: https://pyinstaller.org/

## Prerequisites
- Git installed and on PATH
- Python 3.9+
- GitHub authentication configured (HTTPS + PAT or Git Credential Manager)

## Desktop Application (GUI)
Run the GUI directly:
```bash
python autocommit_gui.py
```

### GUI quick start
1. Click **Browse** and select the folder to watch.
2. Enter **Remote URL** and click **Setup Repo** once.
3. Click **Start Watching** to auto‑commit and push on changes.
4. Click **Stop** to pause.

### GUI controls (every field and button)
| Control | What it does |
| --- | --- |
| Folder | The local folder to watch and commit from. |
| Browse | Opens a folder picker and loads `.autocommit.json` if it exists. |
| Remote URL | GitHub repository URL used for `origin`. |
| Branch | Branch name to push to (default `main`). |
| Interval (sec) | How often the app checks for changes. |
| Message prefix | Prefix used in auto‑commit messages. |
| Git user.name | Optional repo‑local git user name (auto‑filled from git config when available). |
| Git user.email | Optional repo‑local git user email (auto‑filled from git config when available). |
| Allow empty initial commit | Allows an empty first commit if the folder has no files. |
| Setup Repo | Initializes git, sets remote/branch/user, creates the first commit, pushes, and saves config. |
| Start Watching | Starts the background watcher that commits + pushes when changes are found. |
| Stop | Stops the watcher. |
| Status line | Shows the latest action or error from the app. |

## Python CLI
### Setup
```bash
python autocommit.py setup --remote https://github.com/<user>/<repo>.git
```
Initializes a repo if needed, sets the remote/branch, creates an initial commit (if files exist or `--allow-empty-initial` is used), pushes to GitHub, and writes `.autocommit.json`.

### Run (continuous)
```bash
python autocommit.py run
```
Checks for changes every `interval` seconds and auto‑commits + pushes when changes are detected.

### Run once
```bash
python autocommit.py run --once
```

### Commit once
```bash
python autocommit.py commit
```

### Use a specific folder
```bash
python autocommit.py --path "C:\path\to\repo" run
```
By default, the CLI uses the current directory.

### Commit message format
Auto‑commit messages include the timestamp and a short change summary, for example:
`Auto commit 2026-06-01 10:12:00+0530 | M app.py (+3 -1); A README.md`

### CLI config
The `.autocommit.json` file lives in the repo folder and is shared by both CLI and GUI.
- `remote`: GitHub repo URL
- `branch`: branch to push to (default `main`)
- `interval`: seconds between checks
- `message_prefix`: prefix for auto‑commit messages

Override run‑time settings with `--interval` or `--message`.

## Single EXE (GUI + CLI in one file)
Build a single Windows EXE that runs the GUI when double‑clicked and the CLI when arguments are provided.

```bash
python -m pip install pyinstaller
pyinstaller --onefile autocommit_app.py --name AutoCommitter
```

Usage:
1. GUI: double‑click `dist\AutoCommitter.exe`
2. CLI: run from a terminal, for example  
   `dist\AutoCommitter.exe setup --remote https://github.com/<user>/<repo>.git`

## Python Package (PyPI)
Install after publishing:
```bash
pip install auto-github-committer
```

Commands:
1. `autocommitter` (GUI if no args, CLI if args are provided)
2. `autocommitter-cli` (CLI only)
3. `autocommitter-gui` (GUI only)

### Publish to PyPI
1. Build:
```bash
python -m pip install build twine
python -m build
```
2. Upload (use an environment variable for your token):
```bash
setx TWINE_USERNAME __token__
setx TWINE_PASSWORD <your-pypi-token>
python -m twine upload dist\*
```
