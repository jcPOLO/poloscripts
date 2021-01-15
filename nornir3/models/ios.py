from nornir_netmiko.tasks import netmiko_send_command, netmiko_save_config
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core import Task
from typing import List, Dict
import logging
from netmiko.ssh_exception import NetmikoAuthenticationException
from nornir.core.exceptions import NornirSubTaskError


def get_config(task: Task) -> str:
    r = task.run(task=netmiko_send_command,
                        name=f"SHOW RUN PARA EL HOST: {task.host} {task.host.hostname}",
                        command_string='show run',
                        severity_level=logging.DEBUG,
                        ).result
    return r


def get_interfaces_status(task: Task) -> List[Dict[str, str]]:
    r = task.run(task=netmiko_send_command,
                 name=f'SHOW INTERFACE STATUS PARA EL HOST: {task.host}',
                 command_string='show interfaces status',
                 use_textfsm=True,
                 severity_level=logging.DEBUG,
                 ).result
    return r


def get_interfaces_trunk(task: Task) -> List[Dict[str, str]]:
    r = task.run(task=netmiko_send_command,
                 name=f'SHOW INTERFACE TRUNK PARA EL HOST: {task.host}',
                 command_string='show interfaces trunk',
                 use_textfsm=True,
                 severity_level=logging.DEBUG,
                 ).result
    return r


def get_interface_description(interface: str, task: Task) -> List[Dict[str, str]]:
    r = task.run(task=netmiko_send_command,
                 name=f'SHOW INTERFACE {interface} PARA EL HOST: {task.host}',
                 command_string=f'show interface {interface}',
                 use_textfsm=True,
                 severity_level=logging.DEBUG,
                 ).result
    return r


# TODO: this and this return type
def get_neighbor(interface: str, task: Task):
    r = task.run(task=netmiko_send_command,
                 name='MUESTRA LOS VECINOS LOS PUERTOS',
                 command_string=f'show cdp nei {interface} det',
                 use_textfsm=True
                 ).result


def save_config(task: Task):
    r = task.run(task=netmiko_save_config).result
    return r
