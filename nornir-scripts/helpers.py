import ipaddress
import os
import errno


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

