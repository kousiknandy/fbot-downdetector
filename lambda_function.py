import os
from os import environ
from subprocess import Popen
import time
import urllib.request
from urllib3.contrib.socks import SOCKSProxyManager
import socket
import socks
from random import randrange
import json
from contextlib import contextmanager
import logging


@contextmanager
def tor_proxy(port):
    from tempfile import mkstemp

    fd, tmp = mkstemp(".torrc")
    fd_datadir, data_dir = mkstemp(".data")
    os.unlink(data_dir)
    os.makedirs(data_dir)

    with open(tmp, "w") as f:
        f.write("SOCKSPort {}\n".format(port))
        f.write("DataDirectory {}\n".format(data_dir))
    tor_path = os.path.join(environ["LAMBDA_TASK_ROOT"], "tor")
    process = Popen([tor_path, "-f", tmp], cwd=os.path.dirname(data_dir))
    yield
    process.terminate()


def check_onion(url, port, count=3, timeout=30):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    circuit_wait = 10
    while count > 0:
        try:
            time.sleep(circuit_wait)
            proxy = SOCKSProxyManager(f"socks5h://localhost:{port}/")
            logger.info(f"Connecting to {url}")
            s = proxy.request("GET", url, timeout=timeout)
            res = {
                k: v
                for k, v in s.headers.items()
                if k in ["X-FB-Connection-Quality", "X-FB-Debug", "Set-Cookie"]
            }
            res["status"] = s.status
            logger.debug(res)
            return res
        except Exception as e:
            count -= 1
            circuit_wait = 0
            logger.error(f"{e} !! {count} attempts left")
    return {}


def lambda_handler(event, context):
    port = 9050

    with tor_proxy(port):
        res = check_onion(
            "https://www.facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion/",
            port=port,
        )

    return res
