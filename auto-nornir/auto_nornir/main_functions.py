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
    templates: str,
    ini_vars: configparser,
    make_magic_bar: 'tqdm',
    get_config_bar: 'tqdm',
    backup_config_bar: 'tqdm',
    on_retry: bool = False
) -> None:
    config_vars = dict(ini_vars['CONFIG'])
    # makes a log file output for every device accessed
    session_log(task, config_vars.get('outputs_path', None)) 
    # backup running config
    backup_config(task, config_vars.get('backups_path', None))
    if on_retry is True:
        backup_config_bar.clear()
        get_config_bar.clear()
        make_magic_bar.clear()
        on_retry = False

    backup_config_bar.update()
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


# def change_to_telnet(task: Task) -> None:
#     import ipdb; ipdb.set_trace()
#     task.host.port = 23
#     task.host.connection_options['netmiko'] = ConnectionOptions(
#         extras={"device_type": 'cisco_ios_telnet',
#                 "fast_cli": False,
#                 "session_log": session_log(task)}
#     )
#     import ipdb; ipdb.set_trace()
#     print(task.host.connection_options['netmiko'])


def process_data_trunk(data: List) -> List[str]:
    result = []
    for interface in data:

        try:
            if interface['link'] == 'trunk':  # huawei: display port vlan
                result.append(interface['port'])
        except KeyError:
            if interface['status'] == 'trunking':  # ios: show interfaces trunk
                result.append(interface['port'])

    return result


def trunk_description(task: Task) -> None:
    data = get_interfaces_status(task)
    interfaces = process_data_trunk(data)
    task.host['interfaces']: Dict[str, str] = get_interface_description(
        interfaces, task)
