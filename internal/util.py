__author__ = 'Gareth Coles'

import logging
import sys

logging.basicConfig(
    format="%(asctime)s | %(levelname)8s | %(message)s",
    datefmt="%d %b %Y - %H:%M:%S")

logger = logging.getLogger("Web")
logger.setLevel(logging.DEBUG if "--debug" in sys.argv else logging.INFO)


def log(message, level=logging.INFO):
    logger.log(level, message)


def log_request(request, message, level=logging.INFO):
    ip = request.remote_addr
    log("[{ip}] {message}".format(ip=ip, message=message), level)
