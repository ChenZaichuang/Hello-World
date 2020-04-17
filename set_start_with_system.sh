#run with sudo
echo -e '[Unit]\nDescription=/etc/rc.local Compatibility\nConditionPathExists=/etc/rc.local\n \n[Service]\nType=forking\nExecStart=/etc/rc.local start\nTimeoutSec=0\nStandardOutput=tty\nRemainAfterExit=yes\nSysVStartPriority=99\n \n[Install]\nWantedBy=multi-user.target\n' > /etc/systemd/system/rc-local.service
echo -e '#!/bin/sh -e \n su firefly -c '"'python3 /home/firefly/Documents/Ngrok-SSH-Server/start_ngrok.py' \n exit 0" > /etc/rc.local
chmod +x /etc/rc.local
systemctl enable rc-local