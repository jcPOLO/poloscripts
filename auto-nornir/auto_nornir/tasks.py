from typing import Dict, List

from nornir.core import Task

from helpers import check_directory
from models import ios


def get_interfaces_status(task: Task) -> List[Dict[str, str]]:
    r = ''
    if task.host.platform == 'ios' or task.host.platform == 'nxos':
        r = ios.get_interfaces_trunk(task)

    return r


def get_version(task: Task):
    r = ''
    if task.host.platform == 'ios' or task.host.platform == 'nxos':
        r = ios.get_version(task)


def backup_config(task: Task, path: str = 'backups/') -> None:
    r = ''
    file = f'{task.host}.cfg'
    filename = f'{path}{file}'
    if task.host.platform == 'ios' or task.host.platform == 'nxos':
        r = ios.get_config(task)
    if r:
        check_directory(filename)
        with open(filename, 'w') as f:
            f.write(r)


def save_config(task: Task) -> None:
    if task.host.platform == 'ios' or task.host.platform == 'nxos':
        ios.save_config(task)


