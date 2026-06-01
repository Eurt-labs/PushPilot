#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

CONFIG_FILE = ".autocommit.json"


class GitCommandError(RuntimeError):
    def __init__(self, message: str, returncode: int) -> None:
        super().__init__(message)
        self.returncode = returncode


@dataclass(frozen=True)
class Config:
    remote: str
    branch: str = "main"
    interval: int = 60
    message_prefix: str = "Auto commit"


def run_git(
    args: list[str],
    check: bool = True,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        text=True,
        capture_output=True,
        cwd=str(cwd) if cwd else None,
    )
    if check and result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        if not message:
            message = f"Git command failed: git {' '.join(args)}"
        raise GitCommandError(message, result.returncode)
    return result


def is_inside_repo(cwd: Path | None = None) -> bool:
    result = run_git(
        ["rev-parse", "--is-inside-work-tree"],
        check=False,
        cwd=cwd,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def ensure_repo(cwd: Path | None = None) -> None:
    if not is_inside_repo(cwd=cwd):
        run_git(["init"], cwd=cwd)


def ensure_remote(remote: str, cwd: Path | None = None) -> None:
    current = run_git(
        ["remote", "get-url", "origin"],
        check=False,
        cwd=cwd,
    )
    if current.returncode != 0:
        run_git(["remote", "add", "origin", remote], cwd=cwd)
        return
    existing = current.stdout.strip()
    if existing != remote:
        run_git(["remote", "set-url", "origin", remote], cwd=cwd)


def ensure_branch(branch: str, cwd: Path | None = None) -> None:
    if branch:
        run_git(["branch", "-M", branch], cwd=cwd)


def set_user(
    name: str | None,
    email: str | None,
    cwd: Path | None = None,
) -> None:
    if name:
        run_git(["config", "user.name", name], cwd=cwd)
    if email:
        run_git(["config", "user.email", email], cwd=cwd)


def has_commits(cwd: Path | None = None) -> bool:
    result = run_git(
        ["rev-parse", "--verify", "HEAD"],
        check=False,
        cwd=cwd,
    )
    return result.returncode == 0


def has_changes(cwd: Path | None = None) -> bool:
    result = run_git(["status", "--porcelain"], check=False, cwd=cwd)
    return result.stdout.strip() != ""


def create_initial_commit(allow_empty: bool, cwd: Path | None = None) -> None:
    if has_changes(cwd=cwd):
        run_git(["add", "-A"], cwd=cwd)
        run_git(["commit", "-m", "Initial commit"], cwd=cwd)
        return
    if allow_empty:
        run_git(["commit", "--allow-empty", "-m", "Initial commit"], cwd=cwd)
        return
    raise SystemExit(
        "No files to commit. Add files first or pass --allow-empty-initial."
    )


def current_timestamp() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S%z")


def commit_cycle(
    config: Config,
    message: str | None = None,
    cwd: Path | None = None,
) -> bool:
    if not has_changes(cwd=cwd):
        return False
    run_git(["add", "-A"], cwd=cwd)
    commit_message = message or f"{config.message_prefix} {current_timestamp()}"
    run_git(["commit", "-m", commit_message], cwd=cwd)
    run_git(["push", "origin", config.branch], cwd=cwd)
    return True


def save_config(config_path: Path, config: Config) -> None:
    config_path.write_text(
        json.dumps(
            {
                "remote": config.remote,
                "branch": config.branch,
                "interval": config.interval,
                "message_prefix": config.message_prefix,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def load_config(config_path: Path) -> Config:
    if not config_path.exists():
        raise SystemExit(
            f"Config file not found: {config_path}. Run 'setup' first."
        )
    raw: dict[str, Any] = json.loads(config_path.read_text(encoding="utf-8"))
    return Config(
        remote=str(raw["remote"]),
        branch=str(raw.get("branch", "main")),
        interval=int(raw.get("interval", 60)),
        message_prefix=str(raw.get("message_prefix", "Auto commit")),
    )


def setup_command(args: argparse.Namespace) -> None:
    config_path = Path(args.config)
    ensure_repo()
    ensure_remote(args.remote)
    ensure_branch(args.branch)
    set_user(args.name, args.email)

    if not has_commits():
        create_initial_commit(allow_empty=args.allow_empty_initial)

    run_git(["push", "-u", "origin", args.branch])

    config = Config(
        remote=args.remote,
        branch=args.branch,
        interval=args.interval,
        message_prefix=args.message_prefix,
    )
    save_config(config_path, config)
    print(f"Configured. Auto-commit config saved to {config_path}.")


def run_command(args: argparse.Namespace) -> None:
    config = load_config(Path(args.config))
    if not is_inside_repo():
        raise SystemExit("Not inside a git repository. Run 'setup' first.")
    interval = args.interval if args.interval is not None else config.interval
    while True:
        commit_cycle(config, message=args.message)
        if args.once:
            break
        time.sleep(interval)


def commit_command(args: argparse.Namespace) -> None:
    config = load_config(Path(args.config))
    if not is_inside_repo():
        raise SystemExit("Not inside a git repository. Run 'setup' first.")
    committed = commit_cycle(config, message=args.message)
    if not committed:
        print("No changes to commit.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Automatic git commit + push CLI."
    )
    parser.add_argument(
        "--config",
        default=CONFIG_FILE,
        help=f"Config file path (default: {CONFIG_FILE})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    setup = subparsers.add_parser(
        "setup", help="Initialize repo, set remote, and save config."
    )
    setup.add_argument("--remote", required=True, help="GitHub repo URL.")
    setup.add_argument("--branch", default="main", help="Branch name.")
    setup.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Seconds between auto-commit checks.",
    )
    setup.add_argument(
        "--message-prefix",
        default="Auto commit",
        help="Commit message prefix.",
    )
    setup.add_argument("--name", help="Git user.name for this repo.")
    setup.add_argument("--email", help="Git user.email for this repo.")
    setup.add_argument(
        "--allow-empty-initial",
        action="store_true",
        help="Allow an empty initial commit if no files exist.",
    )
    setup.set_defaults(func=setup_command)

    run = subparsers.add_parser(
        "run", help="Continuously auto-commit and push."
    )
    run.add_argument(
        "--interval", type=int, help="Override interval in seconds."
    )
    run.add_argument("--message", help="Override commit message.")
    run.add_argument(
        "--once", action="store_true", help="Run one cycle then exit."
    )
    run.set_defaults(func=run_command)

    commit = subparsers.add_parser(
        "commit", help="Run a single commit + push cycle."
    )
    commit.add_argument("--message", help="Override commit message.")
    commit.set_defaults(func=commit_command)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except GitCommandError as exc:
        if str(exc):
            sys.stderr.write(f"{exc}\n")
        raise SystemExit(exc.returncode)


if __name__ == "__main__":
    main()
