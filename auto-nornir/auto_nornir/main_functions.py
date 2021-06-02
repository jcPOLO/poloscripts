from helpers import check_directory
from nornir.core import Task
from tasks import backup_config, basic_configuration, \
    get_interface_description, get_interfaces_status, \
    save_config
from typing import Dict, List
import configparser

PLATFORM = ['ios', 'huawei', 'nxos']
FINAL_TEMPLATE = 'final.j2'


def make_magic(
    task: Task,
    config_vars
    on_retry: bool = False
) -> None:
    # makes a log file output for every device accessed
    session_log(task, config_vars.get('outputs_path', None)) 
    # backup running config
    backup_config(task, config_vars.get('backups_path', None))

    # if option 2 or 3 is selected
    if 'trunk_description.j2' in templates or 'management.j2' in templates:
        trunk_description(task)
    if 'save_config' in templates:
        save_config(task)
        get_config_bar.update()
        # tqdm.write(f"{task.host}: saved config")
    else:
        # apply final template
        basic_configuration(task, FINAL_TEMPLATE, ini_vars)
        make_magic_bar.update()
        # tqdm.write(f"{task.host}: applied new config")


def session_log(task: Task, path: str = 'outputs/') -> str:
    if path is None:
        path = 'outputs/'
    file = f'{task.host}-{task.host.hostname}-output.txt'
    filename = f'{path}{file}'

    check_directory(path)
    group_object = task.host.groups[0]
    group_object.connection_options["netmiko"].extras["session_log"] = filename
    return filename

