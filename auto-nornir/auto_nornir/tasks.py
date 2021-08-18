from typing import Dict, List
from nornir.core import Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_netmiko.tasks import netmiko_send_config
from helpers import check_directory
from auto_nornir.models.platforms.platform_factory import PlatformFactory
import configparser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = dir_path+'/templates/'


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


def basic_configuration(
        task: Task,
        template: str,
        ini_vars: configparser = None
) -> None:
    # convert ini_vars configparser object to dict for templates
    if ini_vars:
        path = ini_vars.get('CONFIG', 'templates_path')
        ini_vars = dict(ini_vars['GLOBAL'])
    else:
        path = TEMPLATES_DIR
        ini_vars = None
    # Transform inventory data to configuration via a template file
    r = task.run(task=template_file,
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
    task.run(task=netmiko_send_config,
             name=f"APLICAR PLANTILLA PARA {task.host.platform}",
             config_commands=task.host["config"].splitlines(),
             #severity_level=logging.DEBUG,
             )

def software_upgrade(task: Task):
    device = PlatformFactory().software_upgrade(task)
    return device.software_upgrade()
