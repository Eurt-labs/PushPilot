#!/usr/bin/env python3
from __future__ import annotations

import sys

from autocommitter.core import cli_main
from autocommitter.gui import gui_main


def main() -> None:
    if len(sys.argv) > 1:
        cli_main(sys.argv[1:])
    else:
        gui_main()


if __name__ == "__main__":
    main()
