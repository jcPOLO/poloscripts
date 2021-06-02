import ipaddress
import os
import errno
import logging
import sys


def is_ip(string: str) -> bool:
    try:
        ipaddress.ip_address(string)
        return True
    except ValueError:
        return False


def check_directory(path: str):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def is_int(v: any) -> bool:
    v = str(v).strip()
    return v == '0' or (v if v.find('..') > -1 else v.lstrip('-+').rstrip('0').rstrip('.')).isdigit()


def get_platforms(path='templates') -> list:
    if not os.path.exists(os.path.dirname(path)):
        try:
            return os.listdir(path)
        except Exception as e:
            raise e


def configure_logging(logger, debug=''):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    fh = logging.FileHandler('auto-nornir.log')
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
