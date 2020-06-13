#!/usr/bin/env bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$( dirname "${BASH_SOURCE[0]}" )"
pwd
ls
echo 'DIR:'
echo ${DIR}
#bash init.sh
#python3 start_ngrok.py