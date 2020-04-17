from ngrok_ssh_client.ip_evaluate import get_accessible_ssh_tunnels
from python_utils.logger import CustomLogger
import logging
import re
import subprocess
import time
import traceback
from datetime import datetime
import requests
from gevent import sleep

logger = CustomLogger(console_logger_config={'level': logging.INFO}, file_logger_config={'filename': 'start_ngrok.log'})


def kill_ngrok():
    # res = "533 ?        00:09:48 ngrok"
    ngrok_process_str = subprocess.run(f"ps -e | grep ngrok", shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).stdout.decode('utf-8')
    logger.info(f'ngrok_process_str: {ngrok_process_str}')
    match_res = re.match('^\s*(\d+).+ngrok\s*$', ngrok_process_str)
    if match_res is not None:
        pid_number = match_res.groups()[0]
        kill_result = subprocess.run(f"kill -9 {pid_number}", shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        logger.info(f'kill result: {kill_result.stdout} | {kill_result.stdout}')
    else:
        logger.info(f'No ngrok process found...')
    time.sleep(2)


def start_ngrok():
    kill_ngrok()
    res = subprocess.Popen('nohup ngrok tcp 22 --region au &', shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    if res.returncode == 0:
        logger.info(f"Successfully start ngrok: {res.stdout} | {res.stdout}")
    else:
        logger.info(f"Fail to start ngrok: {res.stdout} | {res.stderr}")


def commit_config(public_url):
    logger.info(f"public_url: {public_url}")
    with open(f'configuration/firefly_ssh.txt', 'w') as f:
        f.write(public_url)
    logger.info('finish write ngrok info to file')
    res = subprocess.run(f"cd configuration && git checkout master && git branch --unset-upstream || git add . && git status && git commit -m '{datetime.now()}' && git push origin master --force", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0:
        logger.info(f"Successfully push commit: {res.stdout} | {res.stderr}")
        return True
    else:
        logger.info(f"Fail to push commit: {res.stdout} | {res.stderr}")
        return False

def get_public_url():
    try:
        res = requests.get(url='http://127.0.0.1:4040/api/tunnels')
    except ConnectionRefusedError:
        return 'ngrok not up'
    else:
        info = res.json()
        logger.info(f'Get info: {info}')
        if 'tunnels' in info and len(info['tunnels']) > 0 and 'public_url' in info['tunnels'][0]:
            return info['tunnels'][0]['public_url'][6:]
        else:
            return 'ngrok in init'

def is_network_accessibility():
    try:
        public_url = get_public_url()
        if public_url in ('ngrok not up', 'ngrok in init'):
            return False
        else:
            host, port = public_url.split(':')
            best_ssh_tunnel = get_accessible_ssh_tunnels(host, port, only_best=True)
            return best_ssh_tunnel is not None
    except:
        logger.info(f"Error happen when check_network_accessibility: {traceback.format_exc()}")
        return False


if __name__ == '__main__':

    status = 'need_start_ngrok'

    while True:
        if status == 'need_start_ngrok':
            logger.info(f'status = {status}')
            start_ngrok()
            status = 'check_and_restart_ngrok_until_success'
            sleep(10)

        elif status == 'check_and_restart_ngrok_until_success':
            logger.info(f'status = {status}')
            public_url = get_public_url()
            if public_url == 'ngrok not up':
                status = 'need_start_ngrok'
            elif public_url == 'ngrok in init':
                sleep(2)
            else:
                if commit_config(public_url):
                    status = 'check_network_accessibility'
                else:
                    sleep(2)

        elif status == 'check_network_accessibility':
            logger.info(f'status = {status}')
            if not is_network_accessibility():
                status = 'need_start_ngrok'
            else:
                sleep(60 * 60)
        else:
            raise RuntimeError(f'Unknown status: {status}')