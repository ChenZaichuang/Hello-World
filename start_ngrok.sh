#!/usr/bin/env bash
set -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
./init.sh
python3 start_ngrok.py