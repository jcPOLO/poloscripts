from helpers import check_directory
from nornir.core import Task
from tasks import backup_config, save_config
from models.ios import get_version, get_facts
import configparser
from typing import List

import logging

logger = logging.getLogger(__name__)


def auto_nornir(
    task: Task,
    ini_vars: configparser,
    selections: List
) -> None:
    config_vars = dict(ini_vars['CONFIG'])
    # makes a log file output for every device accessed
    session_log(task, config_vars.get('outputs_path', None)) 
    # backup running config
    backup_config(task, config_vars.get('backups_path', None))

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

