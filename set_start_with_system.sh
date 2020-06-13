DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

command=$'echo -e \'[Unit]\nDescription=/etc/rc.local Compatibility\nConditionPathExists=/etc/rc.local\n \n[Service]\nType=forking\nExecStart=/etc/rc.local start\nTimeoutSec=0\nStandardOutput=tty\nRemainAfterExit=yes\nSysVStartPriority=99\n \n[Install]\nWantedBy=multi-user.target\n\'> /etc/systemd/system/rc-local.service && '
command+=$'echo -e \'#!/bin/sh -e \nsu firefly -c \'\"\'sh '${DIR}$'/start_ngrok.sh\' \nexit 0\" > /etc/rc.local && '
command+=$'chmod +x /etc/rc.local && '
command+=$'systemctl enable rc-local'

su -c "${command}" root