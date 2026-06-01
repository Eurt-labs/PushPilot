# Auto GitHub Committer

Automatically watches a folder, commits changes, and pushes to GitHub — triggered by file saves. No manual `git add`, `git commit`, or `git push` needed.

Available as a **Python GUI** (tkinter), **CLI**, or **standalone EXE**.

---

## Requirements

- Git installed and on PATH ([download](https://git-scm.com/downloads))
- Python 3.9+ ([download](https://www.python.org/downloads/))
- GitHub authentication configured (HTTPS + PAT or [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager))
- A GitHub repository created (use its HTTPS URL)

---

## Quick Start

### CLI (run from the folder you want to watch)

```bash
# Install the package (optional but recommended)
pip install -e .

# Setup your repo URL once
autocommitter-cli setup --remote https://github.com/<user>/<repo>.git

# Start watching for changes
autocommitter-cli run
```

### GUI

```bash
python autocommit_gui.py
# Or: autocommitter-gui
# Or: autocommitter  (launches GUI when no CLI args given)
```

1. Click **Browse** to select your target folder.
2. Enter the **Remote URL** of your GitHub repo.
3. Set the polling **Interval** in seconds (default 60).
4. Click **Setup Repo** to initialize git and configure the remote.
5. Click **Start Watching** to begin auto-committing on every detected change.
6. Click **Push Now** for an immediate commit + push.

---

## Installation

### Run from source (no install)

```bash
git clone https://github.com/<user>/<repo>.git
cd <repo>
python autocommit.py setup --remote <url>
python autocommit.py run
```

### Editable install

```bash
pip install -e .
# Then use the registered commands:
autocommitter            # GUI (no args) or CLI (with args)
autocommitter-cli        # CLI only
autocommitter-gui        # GUI only
```

### Standalone EXE

```bash
pip install pyinstaller
pyinstaller --onefile autocommit_app.py --name AutoCommitter --distpath "Desktop application" --workpath build --specpath build
```

The EXE will be at `Desktop application\AutoCommitter.exe`.

---

## CLI Reference

```bash
# Usage
python autocommit.py <command> [options]
autocommitter-cli <command> [options]

# Global options (place before the subcommand)
--config FILE    Config file path (default: .autocommit.json)
--path DIR       Repo folder to use (default: current directory)
```

### `setup`

Initialize a repo, configure the remote, and save the config file.

| Flag | Description |
| --- | --- |
| `--remote URL` | GitHub repository URL **(required)** |
| `--branch NAME` | Branch to push to (default: `main`) |
| `--interval SEC` | Polling interval in seconds (default: 60) |
| `--message-prefix STR` | Prefix for auto-commit messages (default: `Auto commit`) |
| `--name STR` | Git `user.name` for this repo |
| `--email STR` | Git `user.email` for this repo |
| `--allow-empty-initial` | Allow an empty first commit if the folder has no files |

### `run`

Continuously poll for changes, commit, and push.

| Flag | Description |
| --- | --- |
| `--interval SEC` | Override the polling interval |
| `--message STR` | Override the commit message |
| `--once` | Run a single cycle, then exit |

### `commit`

Run a single commit + push cycle and exit.

| Flag | Description |
| --- | --- |
| `--message STR` | Override the commit message |

---

## GUI Reference

| Control | Description |
| --- | --- |
| **Folder** | Local directory to watch |
| **Browse** | Folder picker; auto-loads `.autocommit.json` if present |
| **Remote URL** | GitHub repository HTTPS URL |
| **Branch** | Branch to push to (default: `main`) |
| **Interval (sec)** | How often the watcher polls for changes |
| **Message prefix** | Prefix for auto-generated commit messages |
| **Git user.name** | Optional repo-local git user name |
| **Git user.email** | Optional repo-local git user email |
| **Allow empty initial commit** | Create an empty first commit if no files exist |
| **Setup Repo** | Initialize git, set remote/branch/user, create initial commit, push, and save config |
| **Start Watching** | Begin the background poll-and-push loop |
| **Push Now** | Commit and push immediately |
| **Stop** | Stop the background watcher |
| **Status line** | Shows the latest action, error, or confirmation |

---

## How Auto-Commit Messages Work

When changes are detected, the tool generates a message like:

```
Auto commit 2026-06-01 14:30:00+0530 | M src/index.py (+10 -2); A docs/readme.md (+45 -0)
```

The format is:

```
<prefix> <timestamp> | <status> <path> (+<added> -<deleted>); ...
```

Status characters follow git conventions: `M` (modified), `A` (added), `D` (deleted), `R` (renamed).

---

## Project Structure

```
autocommitter/
├── __init__.py
├── app.py          # Combined CLI + GUI entry point
├── core.py         # Git operations, config, CLI parser
└── gui.py          # tkinter GUI (AutoCommitApp class)
autocommit.py       # CLI script
autocommit_gui.py   # GUI script
autocommit_app.py   # Combined script (no args = GUI, args = CLI)
pyproject.toml      # Package metadata and entry points
```

---

## First-Time Git Setup

If Git isn't configured yet:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_github_email@example.com"
git config --global init.defaultBranch main
```

Then authenticate with GitHub using a [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) or the [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager).

---

## License

MIT
