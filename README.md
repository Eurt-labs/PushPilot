# Auto GitHub Committer

Automatically watches a folder, commits changes, and pushes to GitHub.

## Links
- Git: https://git-scm.com/downloads
- Python: https://www.python.org/downloads/
- Git Credential Manager: https://github.com/git-ecosystem/git-credential-manager
- PyInstaller: https://pyinstaller.org/

## Requirements
- Git installed and on PATH
- Python 3.9+
- GitHub authentication configured (HTTPS + PAT or Git Credential Manager)

## Python GUI Application (Source)
Run the GUI directly:
```bash
python autocommit_gui.py
```

### GUI quick start
1. Click **Browse** and select the folder to watch.
2. Enter **Remote URL** and click **Setup Repo** once.
3. Click **Start Watching** to auto‑commit and push on changes.
4. Click **Stop** to pause.

### GUI controls
| Control | What it does |
| --- | --- |
| Folder | The local folder to watch and commit from. |
| Browse | Opens a folder picker and loads `.autocommit.json` if it exists. |
| Remote URL | GitHub repository URL used for `origin`. |
| Branch | Branch name to push to (default `main`). |
| Interval (sec) | How often the app checks for changes. |
| Message prefix | Prefix used in auto‑commit messages. |
| Git user.name | Optional repo‑local git user name (auto‑filled from git config). |
| Git user.email | Optional repo‑local git user email (auto‑filled from git config). |
| Allow empty initial commit | Allows an empty first commit if the folder has no files. |
| Setup Repo | Initializes git, sets remote/branch/user, creates the first commit, pushes, and saves config. |
| Start Watching | Starts the background watcher that commits + pushes when changes are found. |
| Stop | Stops the watcher. |
| Status line | Shows the latest action or error from the app. |

## Python CLI (Optional)
### Setup
```bash
python autocommit.py setup --remote https://github.com/<user>/<repo>.git
```

### Run (continuous)
```bash
python autocommit.py run
```

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

## Desktop Application (EXE)
Users can build a Windows EXE from this source and run it without Python.

### Build the EXE
```bash
python -m pip install pyinstaller
pyinstaller --onefile autocommit_app.py --name AutoCommitter --distpath "Desktop application" --workpath build --specpath build
```
The EXE will be created at:
```
Desktop application\AutoCommitter.exe
```

### Run the EXE
1. GUI: double‑click `Desktop application\AutoCommitter.exe`
2. CLI: run from a terminal, for example  
   `Desktop application\AutoCommitter.exe setup --remote https://github.com/<user>/<repo>.git`

## Shared Behavior (GUI + CLI)
- Config file: `.autocommit.json` in the repo folder.
- Commit message format:  
  `Auto commit 2026-06-01 10:12:00+0530 | M app.py (+3 -1); A README.md`
- Both GUI and CLI use the same config and commit logic.
