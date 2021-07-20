from nornir_netmiko.tasks import netmiko_send_command, netmiko_save_config
from nornir.core.task import Result, Task
from typing import List, Dict
from auto_nornir.models.platform import PlatformBase
import logging


GET_VERSION_MSG = "SHOW VERSION PARA EL HOST: {}"
GET_NEIGHBORS_MSG = "MUESTRA LOS VECINOS DEL INTERFACE {}"
GET_INTERFACE_DESCRIPTION_MSG = "SHOW INTERFACE {} PARA EL HOST: {}"
GET_CONFIG_MSG = "SHOW RUN PARA EL HOST: {} {}"
GET_INTERFACE_STATUS_MSG = "SHOW INTERFACE STATUS PARA EL HOST: {}"
GET_INTERFACES_TRUNK_MSG = "SHOW INTERFACE TRUNK PARA EL HOST: {}"

GET_VERSION_CMD = 'show version'
GET_CONFIG_CMD = 'show run'
GET_INTERFACES_STATUS_CMD = 'show interfaces status'
GET_INTERFACES_TRUNK_CMD = 'show interfaces trunk'
GET_INTERFACES_DESCRIPTION_CMD = 'show interface {}'
GET_NEIGHBORS_CMD = 'show cdp nei {} det'


class Ios(PlatformBase):
    def __init__(self, task: Task):
        super().__init__(task)

    # TODO: napalm version to base?
    def get_version(self) -> str:
        r = self.task.run(
            task=netmiko_send_command,
            name=GET_VERSION_MSG.format(self.task.host),
            command_string=GET_VERSION_CMD,
            use_textfsm=True,
            severity_level=logging.DEBUG,
            ).result
        return r

    def get_config(self) -> str:
        r = self.task.run(
            task=netmiko_send_command,
            name=GET_CONFIG_MSG.format(self.task.host, self.task.host.hostname),
            command_string=GET_CONFIG_CMD,
            severity_level=logging.DEBUG,
            ).result
        return r

    def get_interfaces_status(self) -> List[Dict[str, str]]:
        r = self.task.run(
            task=netmiko_send_command,
            name=GET_INTERFACE_STATUS_MSG.format(self.task.host),
            command_string=GET_INTERFACES_STATUS_CMD,
            use_textfsm=True,
            severity_level=logging.DEBUG,
            ).result
        return r

    def get_interfaces_trunk(self) -> List[Dict[str, str]]:
        r = self.task.run(
            task=netmiko_send_command,
            name=GET_INTERFACES_TRUNK_MSG.format(self.task.host),
            command_string=GET_INTERFACES_TRUNK_CMD,
            use_textfsm=True,
            severity_level=logging.DEBUG,
            ).result
        return r

    def get_interface_description(self, interface: str) -> List[Dict[str, str]]:
        r = self.task.run(
            task=netmiko_send_command,
            name=GET_INTERFACE_DESCRIPTION_MSG.format(interface, self.task.host),
            command_string=GET_INTERFACES_DESCRIPTION_CMD.format(interface),
            use_textfsm=True,
            severity_level=logging.DEBUG,
            ).result
        return r

    # TODO: this and this return type
    def get_neighbor(self, interface: str) -> Dict:
        r = self.task.run(
            task=netmiko_send_command,
            name=GET_NEIGHBORS_MSG.format(interface),
            command_string=GET_NEIGHBORS_CMD.format(interface),
            use_textfsm=True
            ).result
        return r

    def save_config(self) -> Result:
        r = self.task.run(task=netmiko_save_config).result
        return r

    def get_config_section(self) ->  str:
        r = self.task.run(
            task=netmiko_send_command,
            name=GET_CONFIG_MSG.format(self.task.host, self.task.host.hostname),
            command_string=f'{GET_CONFIG_CMD} | i 213.229.183',
            severity_level=logging.DEBUG,
            ).result
        return r