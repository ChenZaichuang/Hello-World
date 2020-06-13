#!/usr/bin/env bash
set -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
bash init.sh
python3 start_ngrok.py