from helpers import check_directory
from nornir.core import Nornir, Task
from nornir.core.filter import F
from nornir.core.inventory import ConnectionOptions
from tasks import backup_config, basic_configuration, \
    get_interface_description, get_interfaces_status, \
    save_config
from typing import Dict, List
import configparser

PLATFORM = ['ios', 'huawei', 'nxos']


def make_magic(task: Task, templates: str, ini_vars: configparser) -> None:
    config_vars = dict(ini_vars['CONFIG'])
    # makes a log file output for every device accessed
    session_log(task, config_vars.get('outputs_path', None))
    # backup config
    backup_config(task, config_vars.get('backups_path', None))
    # if option 2 or 3 is selected
    if 'trunk_description.j2' in templates or 'management.j2' in templates:
        trunk_description(task)
    if 'save_config' in templates:
        save_config(task)
    else:
        # apply final template
        config(task, ini_vars)


def config(task: Task, ini_vars: configparser) -> None:
    # record configuration in the device
    template = 'final.j2'
    basic_configuration(task, template, ini_vars)


def session_log(task: Task, path: str = 'outputs/') -> str:
    if path is None:
        path = 'outputs/'
    file = f'{task.host}-{task.host.hostname}-output.txt'
    filename = f'{path}{file}'

    check_directory(path)
    group_object = task.host.groups[0]
    group_object.connection_options["netmiko"].extras["session_log"] = filename
    return filename


def change_to_telnet(task: Task) -> None:
    task.host.port = 23
    task.host.connection_options['netmiko'] = ConnectionOptions(
        extras={"device_type": 'cisco_ios_telnet',
                "session_log": session_log(task)}
    )


def process_data_trunk(data: List) -> List[str]:
    result = []
    for interface in data:

        try:
            if interface['link'] == 'trunk':  # huawei - display port vlan
                result.append(interface['port'])
        except KeyError:
            if interface['status'] == 'trunking':  # ios - show interfaces trunk
                result.append(interface['port'])

    return result


def trunk_description(task: Task) -> None:
    data = get_interfaces_status(task)
    interfaces = process_data_trunk(data)
    task.host['interfaces']: Dict[str, str] = get_interface_description(
        interfaces, task)
