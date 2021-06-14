from nornir_netmiko.tasks import netmiko_send_command, netmiko_save_config
from nornir.core.task import Task, Result
from auto_nornir.core.models.platform import PlatformBase
from typing import List, Dict
import logging


class Huawei(PlatformBase):
    def __init__(self, task: Task):
        super().__init__(task)

    # TODO: pending definition
    def get_interfaces_trunk(self) -> List[Dict[str, str]]:
        pass

    # TODO: pending definition or napalm method to base
    def get_version(self) -> str:
        pass

    def get_config(self) -> str:
        r = self.task.run(
            task=netmiko_send_command,
            name=f"DISPLAY CURRENT PARA EL HOST: {self.task.host} {self.task.host.hostname}",
            command_string='display current',
            severity_level=logging.DEBUG,
            ).result
        return r

    def get_interfaces_status(self) -> List[Dict[str, str]]:
        r = self.task.run(
            task=netmiko_send_command,
            name=f'DISPLAY PORT VLAN PARA EL HOST: {self.task.host}',
            command_string='display port vlan',
            use_textfsm=True,
            severity_level=logging.DEBUG,
            ).result
        return r

    def get_interface_description(self, interface: str) -> List[Dict[str, str]]:
        r = self.task.run(
            task=netmiko_send_command,
            name=f'DISPLAY INTERFACE {interface} PARA EL HOST: {self.task.host}',
            command_string=f'display interface {interface}',
            use_textfsm=True,
            severity_level=logging.DEBUG,
            ).result
        return r

    # TODO: this and this return type
    def get_neighbor(self, interface: str):
        r = self.task.run(
            task=netmiko_send_command,
            name='MUESTRA LA DESCRIPTION DE LOS PUERTOS',
            command_string=f'dis ldp nei {interface}',
            use_textfsm=True
            ).result

    def save_config(self) -> Result:
        r = self.task.run(
            task=netmiko_save_config, confirm=True, confirm_response="y").result
        return r
