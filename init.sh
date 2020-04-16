SCRIPT_PATH=$(pwd)
${SCRIPT_PATH}/init_submodule.sh ngrok_ssh_client git@github.com:ChenZaichuang/Ngrok-SSH-Client.git
${SCRIPT_PATH}/init_submodule.sh configuration git@github.com:ChenZaichuang/Configuration.git
pip3 install -r ${SCRIPT_PATH}/requirements.txt
find ${SCRIPT_PATH} -type d -empty -delete
