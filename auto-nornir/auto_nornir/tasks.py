from typing import Dict, List
from nornir.core import Task
from helpers import check_directory
from auto_nornir.models.platform_factory import PlatformFactory


def get_interfaces_status(task: Task) -> List[Dict[str, str]]:
    device = PlatformFactory().get_platform(task)
    return device.get_interfaces_trunk()


def get_version(task: Task):
    device = PlatformFactory().get_platform(task)
    return device.get_version()


def backup_config(task: Task, path: str = 'backups/') -> None:
    r = ''
    file = f'{task.host}.cfg'
    filename = f'{path}{file}'
    device = PlatformFactory().get_platform(task)
    r = device.get_config()
    if r:
        check_directory(filename)
        with open(filename, 'w') as f:
            f.write(r)


def save_config(task: Task) -> None:
    device = PlatformFactory().get_platform(task)
    device.save_config()


def get_facts(task: Task):
    device = PlatformFactory().get_platform(task)
    return device.get_facts()
