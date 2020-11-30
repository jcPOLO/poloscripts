from nornir.plugins.tasks import networking
from nornir.core import Task
from typing import List, Dict
import logging


def get_config(task: Task) -> str:
    try:
        r = task.run(task=networking.netmiko_send_command,
                     name=f"SHOW RUN PARA EL HOST: {task.host}",
                     command_string='show run',
                     severity_level=logging.DEBUG,
                     ).result
    except Exception as e:
        raise e
    return r


def get_interfaces_status(task: Task) -> List[Dict[str, str]]:
    r = task.run(task=networking.netmiko_send_command,
                 name=f'SHOW INTERFACE STATUS PARA EL HOST: {task.host}',
                 command_string='show interfaces status',
                 use_textfsm=True,
                 severity_level=logging.DEBUG,
                 ).result
    return r


def get_interfaces_trunk(task: Task) -> List[Dict[str, str]]:
    r = task.run(task=networking.netmiko_send_command,
                 name=f'SHOW INTERFACE TRUNK PARA EL HOST: {task.host}',
                 command_string='show interfaces trunk',
                 use_textfsm=True,
                 severity_level=logging.DEBUG,
                 ).result
    return r


def get_interface_description(interface: str, task: Task) -> List[Dict[str, str]]:
    r = task.run(task=networking.netmiko_send_command,
                 name=f'SHOW INTERFACE {interface} PARA EL HOST: {task.host}',
                 command_string=f'show interface {interface}',
                 use_textfsm=True,
                 severity_level=logging.DEBUG,
                 ).result
    return r


# TODO: this and this return type
def get_neighbor(interface: str, task: Task):
    r = task.run(task=networking.netmiko_send_command,
                 name='MUESTRA LOS VECINOS LOS PUERTOS',
                 command_string=f'show cdp nei {interface} det',
                 use_textfsm=True
                 ).result


def save_config(task: Task):
    r = task.run(task=networking.netmiko_save_config).result
    return r
