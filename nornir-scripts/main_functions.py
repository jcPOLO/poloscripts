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
    group_object = task.host.groups.refs[0]
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


def filter_inventory(nr: Nornir) -> Nornir:
    devices = nr
    platforms, sites, models = (set() for i in range(3))

    for host in nr.inventory.hosts.values():
        platforms.add(host.platform)
        sites.add(host['site_code'])
        # models.add(host['model'])

    # platforms = {host.platform for host in nr.inventory.hosts.values()}
    # sites = {host['site_code'] for host in nr.inventory.hosts.values()}
    # models = {host['model'] for host in nr.inventory.hosts.values()}

    platform = input(f"Platform to filter - {', '.join(platforms)}:").lower()
    site = str(input(f"Cod Inm - {', '.join(sites)}:"))
    # model = str(input(f"Cod Inm - {', '.join(models)}:"))

    if platform in platforms:
        print(f'Filter by platform: { platform }')
        devices = nr.filter(F(platform=platform))
    else:
        print(f'All platforms selected.')
    if site in nr.inventory.groups:
        print(f'Filter by site: { site }')
        devices = nr.filter(F(site=site))
    else:
        print(f'All sites selected.')
    try:
        return devices
    except ValueError:
        print(f'Error: no filter applied')
