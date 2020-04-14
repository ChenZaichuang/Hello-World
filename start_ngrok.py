import logging
import subprocess
import http.client
import json
import os
import sys
import time
import traceback
from datetime import datetime

os.environ["MAIN_FILE_PATH"] = os.path.dirname(os.path.abspath(sys.argv[0]))
logging.root.handlers = []
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG, filemode='w',
                    filename=os.path.join(os.environ["MAIN_FILE_PATH"], './', 'ngrok.log'))

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
logging.getLogger("").addHandler(console)

if __name__ == '__main__':
    home_path = '/home/firefly'
    while True:
        try:
            conn = http.client.HTTPConnection("127.0.0.1:4040")
            conn.request("GET", '/api/tunnels')
            res = conn.getresponse()
            text = res.read().decode("utf-8")
            logging.info(f'Get text: {text}')
            info = json.loads(text)
            logging.info(f'Get info: {info}')
            with open(f'{home_path}/Documents/Configuration/firefly_ssh.txt', 'w') as f:
                public_url = info['tunnels'][0]['public_url']
                logging.info(f"public_url: {public_url}")
                f.write(public_url)
            logging.info('finish write ngrok info to file')
            break
        except ConnectionRefusedError:
            logging.info(traceback.format_exc())
            logging.info('try to start ngrok')
            res = subprocess.Popen('nohup ngrok tcp 22 --region ap &', shell=True)
            logging.info('finish start ngrok')
            time.sleep(20)
        except Exception:
            logging.info(traceback.format_exc())
            time.sleep(2)

    subprocess.run(f"cd {home_path}/Documents/Configuration && git checkout master && git branch --unset-upstream || git add . && git status && git commit -m '{datetime.now()}' && git push origin master --force", shell=True)
    logging.info('finish push commit')