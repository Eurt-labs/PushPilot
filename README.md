# Auto GitHub Committer

Automatically watches a folder, commits changes, and pushes to GitHub. You can use it as a **Python GUI**, **Python CLI**, or a **Windows EXE** (built by the user).

## Links
- Git: https://git-scm.com/downloads
- Python: https://www.python.org/downloads/
- Git Credential Manager: https://github.com/git-ecosystem/git-credential-manager
- PyInstaller: https://pyinstaller.org/
- PyPI: https://pypi.org/

## Requirements (all versions)
1. Git installed and on PATH.
2. Python 3.9+ installed.
3. GitHub authentication configured (HTTPS + PAT or Git Credential Manager).
4. A GitHub repository created (use its HTTPS URL for setup).

## Version 1: Python GUI Application (Source)
### Step‑by‑step setup
1. Open a terminal in this project folder.
2. Run:
   ```bash
   python autocommit_gui.py
   ```
3. In the app:
   1. Click **Browse** and choose the folder you want to watch.
   2. Enter **Remote URL**.
   3. Click **Setup Repo** once.
   4. Click **Start Watching** to auto‑commit and push changes.

### GUI controls (what each button/field does)
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

## Version 2: Python CLI
### Step‑by‑step setup
1. Open a terminal in the folder you want to watch.
2. Run:
   ```bash
   python autocommit.py setup --remote https://github.com/<user>/<repo>.git
   ```
3. Start watching:
   ```bash
   python autocommit.py run
   ```

### Useful CLI commands
```bash
python autocommit.py run --once
python autocommit.py commit
python autocommit.py --path "C:\path\to\repo" run
```

## Version 3: Desktop Application (Windows EXE)
Users build the EXE themselves from this source.

### Step‑by‑step build
1. Install PyInstaller:
   ```bash
   python -m pip install pyinstaller
   ```
2. Build:
   ```bash
   pyinstaller --onefile autocommit_app.py --name AutoCommitter --distpath "Desktop application" --workpath build --specpath build
   ```
3. The EXE will be at:
   ```
   Desktop application\AutoCommitter.exe
   ```

### Step‑by‑step run
1. GUI: double‑click `Desktop application\AutoCommitter.exe`
2. CLI example:
   ```bash
   Desktop application\AutoCommitter.exe setup --remote https://github.com/<user>/<repo>.git
   ```

## Version 4: Python Package (PyPI)
### Step‑by‑step publish (for the maintainer)
1. Build:
   ```bash
   python -m pip install build twine
   python -m build
   ```
2. Upload:
   ```bash
   setx TWINE_USERNAME __token__
   setx TWINE_PASSWORD <your-pypi-token>
   python -m twine upload dist\*
   ```

### Step‑by‑step install (for users)
```bash
pip install auto-github-committer
autocommitter
```

## Shared behavior (GUI + CLI)
- Config file: `.autocommit.json` in the repo folder.
- Commit message format: `Auto commit <date/time> | <change summary>`.
- Same logic and settings for GUI, CLI, and EXE.
