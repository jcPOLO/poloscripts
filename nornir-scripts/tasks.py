from nornir.core import Task
from nornir.plugins.tasks import networking, text
from models import huawei, ios
from helpers import check_directory
from typing import List, Dict
import logging
import configparser


def get_interfaces_status(task: Task) -> List[Dict[str, str]]:
    r = ''
    if task.host.platform == 'huawei':
        r = huawei.get_interfaces_status(task)
    if task.host.platform == 'ios' or task.host.platform == 'nxos':
        r = ios.get_interfaces_trunk(task)

    return r


def basic_configuration(task: Task, template: str, ini_vars: configparser) -> None:
    # convert ini_vars configparser object to dict for templates
    path = ini_vars.get('CONFIG', 'templates_path')
    ini_vars = dict(ini_vars['GLOBAL'])

    # Transform inventory data to configuration via a template file
    r = task.run(task=text.template_file,
                 name=f"PLANTILLA A APLICAR PARA {task.host.platform}",
                 template=template,
                 path=f"{path}{task.host.platform}",
                 ini_vars=ini_vars,
                 nr=task,
                 #severity_level=logging.DEBUG,
                 )
    # Save the compiled configuration into a host variable
    task.host["config"] = r.result
    # Send final configuration template using netmiko
    task.run(task=networking.netmiko_send_config,
             name=f"APLICAR PLANTILLA PARA {task.host.platform}",
             config_commands=task.host["config"].splitlines(),
             #severity_level=logging.DEBUG,
             )


def backup_config(task: Task, path: str = 'backups/') -> None:
    if path is None:
        path = 'backups/'
    r = ''
    file = f'{task.host}-{task.host.hostname}.cfg'
    filename = f'{path}{file}'

    if task.host.platform == 'huawei':
        r = huawei.get_config(task)
    if task.host.platform == 'ios' or task.host.platform == 'nxos':
        r = ios.get_config(task)

    check_directory(filename)
    with open(filename, 'w') as f:
        f.write(r)


def save_config(task: Task) -> None:
    if task.host.platform == 'huawei':
        huawei.save_config(task)
    if task.host.platform == 'ios' or task.host.platform == 'nxos':
        ios.save_config(task)


def get_interface_description(interfaces: List, task: Task) -> List[Dict[str, str]]:
    r = ''
    result = []
    for interface in interfaces:
        if task.host.platform == 'huawei':
            r = huawei.get_interface_description(interface, task)
        if task.host.platform == 'ios' or task.host.platform == 'nxos':
            r = ios.get_interface_description(interface, task)

        if 'description' in r[0]:
            # do not duplicate interface name in description if it already exists
            if interface in r[0]['description']:
                r[0]['description'] = r[0]['description'].replace(interface, '').strip()
            port_dict = {
                'interface': interface,
                'description': r[0]['description'],
            }
        else:
            port_dict = {
                'interface': interface,
                'description': '',
            }
        result.append(port_dict)

    return result
