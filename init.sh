SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
${SCRIPT_PATH}/init_submodule.sh ngrok_ssh_client git@github.com:ChenZaichuang/Ngrok-SSH-Client.git
pip3 install -r ${SCRIPT_PATH}/requirements.txt
find ${SCRIPT_PATH} -type d -empty -delete
