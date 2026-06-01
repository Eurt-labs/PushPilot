# Automate Your Github Commits and Push Automatically to Github
 **No More Commands Just Ctrl+S and This Python application**\
Automatically watches a folder, commits changes, and pushes to GitHub. You can use it as a **Python GUI**, **Python CLI**, or a **Windows EXE** (built by the user if you want).

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

## How to Setup Git and Github for the first time 
**You can watch this video for you refernce**: https://youtu.be/wDRoduig_98?si=MxIWlZQn9vYYDedS

### **You can Also follow this Steps**\

####    Step 1: Install Git\
            First, you need the Git version control system installed locally on your machine.\
                Download the installer from git-scm.com and run it. The default settings are generally fine for most users if you are not good with the default settings then go and watch youtube videos.\
####    Step 2: Configure Your Git Identity\
           Git needs to know who you are so it can properly label your commits. Open your terminal (or Git Bash on Windows) and run these commands, replacing the placeholder text with your actual information:\
            ```bash
            git config --global user.name "Your First and Last Name"
            git config --global user.email "your_github_email@example.com"
            ```\
            Pro-tip: It is highly recommended to set your default branch name to main (instead of the older default master), as this matches GitHub's default settings:
            ```bash\
            git config --global init.defaultBranch main
            ```\
####    Step 3: Now you have to download the application or GUI/CLI:\
            You have to follow the steps below of your version , then after entrying the neccessary details the Application will except you to **sign in** to you **github account** 
              do not worry it just to verify Git to you Github account.\
            After this setup you will not be asked again and again to sign in to you github account.\

## Version 1: Python GUI Application (Source)
### Step‑by‑step setup
1. Clone this repository to your PC 
2. Open a terminal in this project folder.
3. Run:
   ```bash
   python autocommit_gui.py
   ```
4. In the GUI-app:
   1. Click **Browse** and choose the folder you want to watch.
   2. Enter **Remote URL**.
   3. Setup your time **interval** (Default=60)
   4. Click **Setup Repo** once.
   5. Click **Start Watching** to auto‑commit and push changes automaticcaly when the script detects any file changes.

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
1. Open a terminal in the folder you want to Commit automatically on Any Changes made in File.
2. Run:
    **Important** (this is to setup your Repository link)
    **Replace this link with your Repository link** 
     ```
     https://github.com/<user>/<repo>.git
      ```
   ```bash
   python autocommit.py setup --remote https://github.com/<user>/<repo>.git
   ```
3. Start watching( This Will automatically Commit Changes when the Files chanages and changes are saved in file):
   ```bash
   python autocommit.py run
   ```

### Useful CLI commands
```bash
python autocommit.py run --once 
python autocommit.py commit
python autocommit.py --path "C:\path\to\repo" run\
 (If you want to Commit Changes from a different Foleder or you want to Setup a Folder other than the Opend Folder)
```

## Version 3: Desktop Application (If You Don't Trust my Application you can Build the application your Self)
For Users build the EXE themselves from this source.


**Important** You Have to Delete all Files inside Desktop application folder ( if they exists)
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
   ```bash
   Desktop application\AutoCommitter.exe
   ```
   or the dist path you entered in the previous Command

### Step‑by‑step run
1. GUI: double‑click `Desktop application\AutoCommitter.exe`
2. CLI example:
   ```bash
   Desktop application\AutoCommitter.exe setup --remote https://github.com/<user>/<repo>.git
   ```
