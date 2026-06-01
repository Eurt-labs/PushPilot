#!/usr/bin/env python3
from __future__ import annotations

import threading
import time
import tkinter as tk
from dataclasses import replace
from pathlib import Path
from tkinter import filedialog, ttk
from typing import Callable

from autocommitter.core import (
    CONFIG_FILE,
    Config,
    GitCommandError,
    commit_cycle,
    create_initial_commit,
    ensure_branch,
    ensure_remote,
    ensure_repo,
    get_git_identity,
    has_commits,
    is_inside_repo,
    load_config,
    run_git,
    save_config,
    set_user,
)


class AutoCommitApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Auto GitHub Committer - Dhruv")
        self.root.resizable(False, False)

        self.folder_var = tk.StringVar()
        self.remote_var = tk.StringVar()
        self.branch_var = tk.StringVar(value="main")
        self.interval_var = tk.StringVar(value="60")
        self.prefix_var = tk.StringVar(value="Auto commit")
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.allow_empty_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value="Select a folder to begin.")

        self._stop_event = threading.Event()
        self._watch_thread: threading.Thread | None = None

        self._build_ui()
        self._set_default_folder()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0)

        ttk.Label(frame, text="Folder").grid(row=0, column=0, sticky="w")
        folder_entry = ttk.Entry(frame, textvariable=self.folder_var, width=52)
        folder_entry.grid(row=0, column=1, padx=6)
        ttk.Button(frame, text="Browse", command=self._browse).grid(
            row=0, column=2
        )

        ttk.Label(frame, text="Remote URL").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.remote_var, width=52).grid(
            row=1, column=1, padx=6, columnspan=2, sticky="w"
        )

        ttk.Label(frame, text="Branch").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.branch_var, width=16).grid(
            row=2, column=1, sticky="w"
        )

        ttk.Label(frame, text="Interval (sec)").grid(row=3, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.interval_var, width=16).grid(
            row=3, column=1, sticky="w"
        )

        ttk.Label(frame, text="Message prefix").grid(
            row=4, column=0, sticky="w"
        )
        ttk.Entry(frame, textvariable=self.prefix_var, width=40).grid(
            row=4, column=1, sticky="w"
        )

        ttk.Label(frame, text="Git user.name").grid(row=5, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.name_var, width=40).grid(
            row=5, column=1, sticky="w"
        )

        ttk.Label(frame, text="Git user.email").grid(row=6, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.email_var, width=40).grid(
            row=6, column=1, sticky="w"
        )

        ttk.Checkbutton(
            frame,
            text="Allow empty initial commit",
            variable=self.allow_empty_var,
        ).grid(row=7, column=1, sticky="w", pady=(4, 0))

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=(10, 4))
        self.setup_button = ttk.Button(
            button_frame, text="Setup Repo", command=self._setup_repo
        )
        self.setup_button.grid(row=0, column=0, padx=4)
        self.start_button = ttk.Button(
            button_frame, text="Start Watching", command=self._start_watching
        )
        self.start_button.grid(row=0, column=1, padx=4)
        self.push_button = ttk.Button(
            button_frame, text="Push Now", command=self._push_now
        )
        self.push_button.grid(row=0, column=2, padx=4)
        self.stop_button = ttk.Button(
            button_frame, text="Stop", command=self._stop_watching, state="disabled"
        )
        self.stop_button.grid(row=0, column=3, padx=4)

        ttk.Label(
            frame, textvariable=self.status_var, foreground="#444"
        ).grid(row=9, column=0, columnspan=3, sticky="w", pady=(8, 0))

    def _browse(self) -> None:
        folder = filedialog.askdirectory()
        if not folder:
            return
        self.folder_var.set(folder)
        repo_path = Path(folder)
        self._load_config(repo_path)
        self._populate_identity(repo_path)

    def _load_config(self, repo_path: Path) -> None:
        config_path = repo_path / CONFIG_FILE
        if not config_path.exists():
            self._set_status("No config found. Fill details and run Setup.")
            return
        try:
            config = load_config(config_path)
        except (ValueError, OSError, GitCommandError, SystemExit) as exc:
            self._set_status(f"Failed to load config: {exc}")
            return
        self.remote_var.set(config.remote)
        self.branch_var.set(config.branch)
        self.interval_var.set(str(config.interval))
        self.prefix_var.set(config.message_prefix)
        self._set_status(f"Loaded config from {config_path}.")

    def _populate_identity(self, repo_path: Path) -> None:
        name, email = get_git_identity(cwd=repo_path)
        if name and not self.name_var.get().strip():
            self.name_var.set(name)
        if email and not self.email_var.get().strip():
            self.email_var.set(email)

    def _set_default_folder(self) -> None:
        default_path = Path.cwd()
        self.folder_var.set(str(default_path))
        self._populate_identity(default_path)
        if is_inside_repo(cwd=default_path):
            self._load_config(default_path)
            self._set_status(f"Using current folder: {default_path}")
        else:
            self._set_status("Select a folder to begin.")

    def _parse_interval(self) -> int:
        raw = self.interval_var.get().strip() or "60"
        interval = int(raw)
        if interval <= 0:
            raise ValueError("Interval must be a positive number.")
        return interval

    def _setup_repo(self) -> None:
        repo_path = self._repo_path()
        if repo_path is None:
            return
        remote = self.remote_var.get().strip()
        if not remote:
            self._set_status("Remote URL is required for setup.")
            return
        branch = self.branch_var.get().strip() or "main"
        try:
            interval = self._parse_interval()
        except ValueError as exc:
            self._set_status(str(exc))
            return
        prefix = self.prefix_var.get().strip() or "Auto commit"
        name = self.name_var.get().strip() or None
        email = self.email_var.get().strip() or None
        allow_empty = self.allow_empty_var.get()

        def work() -> None:
            ensure_repo(cwd=repo_path)
            ensure_remote(remote, cwd=repo_path)
            ensure_branch(branch, cwd=repo_path)
            set_user(name, email, cwd=repo_path)
            if not has_commits(cwd=repo_path):
                create_initial_commit(allow_empty, cwd=repo_path)
            run_git(["push", "-u", "origin", branch], cwd=repo_path)
            config = Config(
                remote=remote,
                branch=branch,
                interval=interval,
                message_prefix=prefix,
            )
            save_config(repo_path / CONFIG_FILE, config)
            self._set_status("Setup complete. You can start watching.")

        self._run_async(work)

    def _start_watching(self) -> None:
        if self._watch_thread and self._watch_thread.is_alive():
            return
        repo_path = self._repo_path()
        if repo_path is None:
            return
        if not is_inside_repo(cwd=repo_path):
            self._set_status("Not a git repo. Run Setup first.")
            return

        config = self._resolve_config(repo_path)
        if config is None:
            return

        self._stop_event.clear()
        self._watch_thread = threading.Thread(
            target=self._watch_loop,
            args=(repo_path, config),
            daemon=True,
        )
        self._watch_thread.start()
        self._set_buttons(running=True)
        self._set_status("Watching for changes...")

    def _push_now(self) -> None:
        repo_path = self._repo_path()
        if repo_path is None:
            return
        if not is_inside_repo(cwd=repo_path):
            self._set_status("Not a git repo. Run Setup first.")
            return
        config = self._resolve_config(repo_path)
        if config is None:
            return

        def work() -> None:
            committed = commit_cycle(config, cwd=repo_path)
            if committed:
                self._set_status("Committed and pushed.")
            else:
                self._set_status("No changes to commit.")

        self._run_async(work)

    def _resolve_config(self, repo_path: Path) -> Config | None:
        config_path = repo_path / CONFIG_FILE
        config: Config | None = None
        if config_path.exists():
            try:
                config = load_config(config_path)
            except (ValueError, OSError, SystemExit, GitCommandError) as exc:
                self._set_status(f"Failed to load config: {exc}")
                return None
        remote = self.remote_var.get().strip() or (config.remote if config else "")
        if not remote:
            self._set_status("Remote URL is required. Run Setup first.")
            return None
        branch = self.branch_var.get().strip() or (config.branch if config else "main")
        prefix = (
            self.prefix_var.get().strip()
            or (config.message_prefix if config else "Auto commit")
        )
        try:
            interval = self._parse_interval()
        except ValueError as exc:
            self._set_status(str(exc))
            return None
        if config is None:
            config = Config(
                remote=remote,
                branch=branch,
                interval=interval,
                message_prefix=prefix,
            )
        else:
            config = replace(
                config,
                remote=remote,
                branch=branch,
                interval=interval,
                message_prefix=prefix,
            )
        return config

    def _watch_loop(self, repo_path: Path, config: Config) -> None:
        interval = config.interval
        while not self._stop_event.is_set():
            try:
                committed = commit_cycle(config, cwd=repo_path)
            except (GitCommandError, OSError, SystemExit) as exc:
                self._set_status(f"Git error: {exc}")
                break
            if committed:
                self._set_status(f"Committed and pushed at {time.strftime('%H:%M:%S')}.")
            else:
                self._set_status(f"No changes at {time.strftime('%H:%M:%S')}.")
            self._stop_event.wait(interval)

        self.root.after(0, lambda: self._set_buttons(running=False))

    def _stop_watching(self) -> None:
        if not self._watch_thread:
            return
        self._stop_event.set()
        self._set_status("Stopping watcher...")

    def _repo_path(self) -> Path | None:
        raw = self.folder_var.get().strip()
        if not raw:
            self._set_status("Choose a folder first.")
            return None
        return Path(raw)

    def _run_async(self, func: Callable[[], None]) -> None:
        def wrapped() -> None:
            try:
                func()
            except (GitCommandError, OSError, ValueError, SystemExit) as exc:
                self._set_status(str(exc))

        threading.Thread(target=wrapped, daemon=True).start()

    def _set_buttons(self, running: bool) -> None:
        if running:
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
        else:
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def _set_status(self, message: str) -> None:
        self.root.after(0, lambda: self.status_var.set(message))

    def _on_close(self) -> None:
        self._stop_event.set()
        self.root.destroy()


def gui_main() -> None:
    root = tk.Tk()
    ttk.Style(root).theme_use("clam")
    AutoCommitApp(root)
    root.mainloop()


if __name__ == "__main__":
    gui_main()
