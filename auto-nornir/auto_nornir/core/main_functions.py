from nornir.core import Task
from auto_nornir.core.helpers import check_directory
from auto_nornir.core.tasks import backup_config, save_config, get_version, get_facts, basic_configuration, get_config_section, software_upgrade, set_rsa, get_dir
from typing import List
# import configparser
import logging

logger = logging.getLogger(__name__)
FINAL_TEMPLATE = 'final.j2'


def container_task(
    task: Task,
    selections: List
) -> None:
    # makes a log file output for every device accessed by netmiko config
    session_log(task)
    # backup running config
    backup_config(task)

    # tasks
    if 'get_version' in selections:
        logger.info("get_version selected")
        get_version(task)
    if 'get_config_section' in selections:
        get_config_section(task)
    if 'get_facts' in selections:
        logger.info("get_facts selected")
        get_facts(task)
    if 'get_dir' in selections:
        logger.info("get_dir selected")
        get_dir(task)
    if 'save_config' in selections:
        logger.info("save_config selected")
        save_config(task)
    if any('.j2' in s for s in selections):
        logger.info("applying jinja2 template")
        basic_configuration(task, FINAL_TEMPLATE)
    if 'software_upgrade' in selections:
        logger.info("software_upgrade selected")
        software_upgrade(task)
    if 'set_rsa' in selections:
        logger.info("set rsa_rsa selected")
        set_rsa(task)


def session_log(task: Task, path: str = 'outputs/') -> str:
    if path is None:
        path = 'outputs/'
    file = f'{task.host}-output.txt'
    filename = f'{path}{file}'
    check_directory(path)
    group_object = task.host.groups[0]
    group_object.connection_options["netmiko"].extras["session_log"] = filename
    return filename
