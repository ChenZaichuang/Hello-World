import subprocess
import http.client
import json
import os
import time
from datetime import datetime

if __name__ == '__main__':
    home_path = os.environ['HOME']
    subprocess.run('pkill -f "ngrok"', shell=True)
    subprocess.Popen('ngrok tcp 22 --region ap', shell=True)
    while True:
        try:
            conn = http.client.HTTPConnection("127.0.0.1:4040")
            conn.request("GET", '/api/tunnels')
            res = conn.getresponse()
            break
        except ConnectionRefusedError:
            time.sleep(1)
    info = json.loads(res.read().decode("utf-8"))
    with open(f'{home_path}/Documents/Configuration/firefly_ssh.txt', 'w') as f:
        f.write(info['tunnels'][0]['public_url'])
    subprocess.run(f"cd {home_path}/Documents/Configuration && git branch --unset-upstream || git add . && git status && git commit -m '{datetime.now()}' && git pull -r origin master || git push origin master", shell=True)
    subprocess.run(f"cd {home_path}/Documents/Configuration && git push origin master", shell=True)
