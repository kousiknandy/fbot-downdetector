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


def lambda_handler(event, context):
    port = 9050
    with tor_proxy(port):
        count = 10
        while count > 0:
            try:
                time.sleep(5)
                proxy = SOCKSProxyManager(f"socks5h://localhost:{port}/")
                s = proxy.request(
                    "GET",
                    "https://www.facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion/",
                    timeout=17.0,
                )
                res = {
                    k: v
                    for k, v in s.headers.items()
                    if k in ["X-FB-Connection-Quality", "X-FB-Debug", "Set-Cookie"]
                }
                res["status"] = s.status
                return res
            except Exception as e:
                time.sleep(3)
                count -= 1

    return "{}"
