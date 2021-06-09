from helpers import check_directory
from nornir.core import Task
from tasks import backup_config, save_config, get_version, get_facts
from typing import List
# import configparser
import logging

logger = logging.getLogger(__name__)


def auto_nornir(
    task: Task,
    selections: List
) -> None:
    # makes a log file output for every device accessed
    session_log(task)
    # backup running config
    backup_config(task)

    # tasks
    if 'get_version' in selections:
        logger.info("get_version selected")
        get_version(task)
    if 'get_facts' in selections:
        logger.info("get_facts selected")
        get_facts(task)
    if 'save_config' in selections:
        logger.info("save_config selected")
        save_config(task)
    else:
        logger.warning("nothing selected")


def session_log(task: Task, path: str = 'outputs/') -> str:
    if path is None:
        path = 'outputs/'
    file = f'{task.host}-output.txt'
    filename = f'{path}{file}'

    check_directory(path)
    group_object = task.host.groups[0]
    group_object.connection_options["netmiko"].extras["session_log"] = filename
    return filename
