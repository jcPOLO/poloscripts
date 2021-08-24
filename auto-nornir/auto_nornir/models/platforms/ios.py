from nornir_netmiko.tasks import netmiko_send_command, netmiko_save_config, netmiko_file_transfer
from nornir.core.task import Result, Task
from typing import List, Dict
from auto_nornir.models.platform import PlatformBase
from helpers import HumanBytes
from auto_nornir.exceptions import RuntimeErrorException
import os
import logging


GET_VERSION_MSG = "SHOW VERSION PARA EL HOST: {}"
GET_NEIGHBORS_MSG = "MUESTRA LOS VECINOS DEL INTERFACE {}"
GET_INTERFACE_DESCRIPTION_MSG = "SHOW INTERFACE {} PARA EL HOST: {}"
GET_CONFIG_MSG = "SHOW RUN PARA EL HOST: {} {}"
GET_INTERFACE_STATUS_MSG = "SHOW INTERFACE STATUS PARA EL HOST: {}"
GET_INTERFACES_TRUNK_MSG = "SHOW INTERFACE TRUNK PARA EL HOST: {}"
GET_DIR_MSG = "DIR FLASH:/ PARA EL HOST: {}"

GET_VERSION_CMD = 'show version'
GET_CONFIG_CMD = 'show run'
GET_INTERFACES_STATUS_CMD = 'show interfaces status'
GET_INTERFACES_TRUNK_CMD = 'show interfaces trunk'
GET_INTERFACES_DESCRIPTION_CMD = 'show interface {}'
GET_NEIGHBORS_CMD = 'show cdp nei {} det'
GET_DIR_CMD = 'dir'


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
            # severity_level=logging.DEBUG,
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
            # severity_level=logging.DEBUG,
            ).result
        return r

    def get_interfaces_trunk(self) -> List[Dict[str, str]]:
        r = self.task.run(
            task=netmiko_send_command,
            name=GET_INTERFACES_TRUNK_MSG.format(self.task.host),
            command_string=GET_INTERFACES_TRUNK_CMD,
            use_textfsm=True,
            # severity_level=logging.DEBUG,
            ).result
        return r

    def get_interface_description(self, interface: str) -> List[Dict[str, str]]:
        r = self.task.run(
            task=netmiko_send_command,
            name=GET_INTERFACE_DESCRIPTION_MSG.format(interface, self.task.host),
            command_string=GET_INTERFACES_DESCRIPTION_CMD.format(interface),
            use_textfsm=True,
            # severity_level=logging.DEBUG,
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
        r = self.task.run(
            task=netmiko_save_config,
            # severity_level=logging.DEBUG
            ).result
        return r

    def get_config_section(self) ->  str:
        r = self.task.run(
            task=netmiko_send_command,
            name=GET_CONFIG_MSG.format(self.task.host, self.task.host.hostname),
            command_string=f'{GET_CONFIG_CMD} | i 213.229.183',
            # severity_level=logging.DEBUG,
            ).result
        return r

    def set_rsa(self) -> Result:
        def netmiko_send_task(task):
            # log all netmiko communication with the device in test.log
            # import logging
            # logging.basicConfig(filename='test.log', level=logging.DEBUG)
            # logger = logging.getLogger("netmiko")

            # Manually create Netmiko connection. Needs fast_cli to False in nornir groups.yaml - ios netmiko extra option
            net_connect = self.task.host.get_connection("netmiko", self.task.nornir.config)
            output = net_connect.config_mode()
            output += net_connect.send_command("crypto key zeroize rsa", expect_string=r"you really want to remove")
            output += net_connect.send_command("y", expect_string=r"#")
            output += net_connect.send_command("crypto key generate rsa modulus 2048", expect_string=r"OK")
            output += net_connect.exit_config_mode()
            return output
        r = self.task.run(
            task=netmiko_send_task,
            # severity_level=logging.DEBUG,
            ).result
        return r

    # @staticmethod
    # def polo(task):
    #     return Result(
    #             host=task.host,
    #             result=f"Ejecutando transferencia de archivos..."
    #         )

    # netmiko checks the md5 signature after upload with a different ssh control session than the scp one.
    def software_upgrade(self) -> Result:
        source_file = self.task.host.get('image')
        dest_file = self.task.host.get('image')
        r = self.task.run(
            name=f"CHECKING SPACE AVAILABLE IN {self.task.host.name} FOR {self.task.host.get('image')}",
            task=self.has_free_space,
            # severity_level=logging.DEBUG,
            )
        # r = self.task.run(
        #     name=f"IMAGE UPLOAD TO HOST: {self.task.host.name}",
        #     task=self.polo,
        #     # severity_level=logging.DEBUG,
        #     )
        # return r
        r = self.task.run(
            name=f"IMAGE UPLOAD TO HOST: {self.task.host.name}",
            task=netmiko_file_transfer,
            source_file=source_file,
            dest_file=dest_file,
            direction='put'
            ).result
        return r

    # TODO: remove exec timeout before making long tasks as it can get you out of the device before ending. Maybe it is handled already by nornir... need to check it.
    def remove_exec_timeout(self) -> Result:
        pass

    def get_dir(self) -> Result:
        r = self.task.run(
            task=netmiko_send_command,
            name=GET_DIR_MSG.format(self.task.host, self.task.host.hostname),
            command_string=GET_DIR_CMD,
            use_textfsm=True,
            severity_level=logging.DEBUG,
            ).result
        return r
        
    def has_free_space(self, task) -> str:
        r = self.get_dir()
        space_available = float(r[0]['total_free'] if 'flash' in r[0].get('file_system') else "error")
        total_size = float(r[0]['total_size'] if 'flash' in r[0].get('file_system') else "error")
        source_file = task.host.get('image')
        file_size = float(os.stat(source_file).st_size)
        if space_available > file_size * 2:
            return Result(
                host=task.host,
                result=f"Space needed: {HumanBytes.format(file_size)}\nFree space: {HumanBytes.format(space_available)}"
            )
        else:
            message = f"ERROR:\n \
                    Space needed: {HumanBytes.format(file_size)}\n \
                    Free space: {HumanBytes.format(space_available)}\n \
                    Total size: {HumanBytes.format(total_size)}"
            raise RuntimeErrorException("fail-config", message)
