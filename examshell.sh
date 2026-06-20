#!/usr/bin/env bash
# Launch the 42 examshell practice TUI.
# With no arguments it opens the interactive exam-selection menu.
# Any arguments are forwarded to the CLI (e.g. ./examshell.sh list).

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1
exec python3 -m examshell "$@"
