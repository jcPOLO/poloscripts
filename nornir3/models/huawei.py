from nornir_netmiko.tasks import netmiko_send_command, netmiko_save_config
from nornir.core import Task
import logging
from typing import List, Dict
from netmiko.ssh_exception import NetmikoAuthenticationException


def get_config(task: Task) -> str:
    try:
        r = task.run(task=netmiko_send_command,
                    name=f"DISPLAY CURRENT PARA EL HOST: {task.host} {task.host.hostname}",
                    command_string='display current',
                    severity_level=logging.DEBUG,
                    ).result
    except NetmikoAuthenticationException:
        print(f'Excepcion capturada: {e}, en get_config de huawei.py')
    return r


def get_interfaces_status(task: Task) -> List[Dict[str, str]]:
    r = task.run(task=netmiko_send_command,
                 name=f'DISPLAY PORT VLAN PARA EL HOST: {task.host}',
                 command_string='display port vlan',
                 use_textfsm=True,
                 severity_level=logging.DEBUG,
                 ).result
    return r


def get_interface_description(interface: str, task: Task) -> List[Dict[str, str]]:
    r = task.run(task=netmiko_send_command,
                 name=f'DISPLAY INTERFACE {interface} PARA EL HOST: {task.host}',
                 command_string=f'display interface {interface}',
                 use_textfsm=True,
                 severity_level=logging.DEBUG,
                 ).result
    return r


# TODO: this and this return type
def get_neighbor(interface: str, task: Task):
    r = task.run(task=netmiko_send_command,
                 name='MUESTRA LA DESCRIPTION DE LOS PUERTOS',
                 command_string=f'dis ldp nei {interface}',
                 use_textfsm=True
                 ).result


def save_config(task: Task):
    r = task.run(task=netmiko_save_config, confirm=True, confirm_response="y").result
    return r
