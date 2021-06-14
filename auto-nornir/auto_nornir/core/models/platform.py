from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.task import Task
import logging


class PlatformBase:
    def __init__(self, task: Task):
        self.task = task

    def get_facts(self) -> str:
        r = self.task.run(
            task=napalm_get,
            name=f'FACTs PARA: {self.task.host}',
            getters=['facts'],
            severity_level=logging.DEBUG,
        ).result
        return r

    def get_version(self):
        pass

    def get_config(self):
        pass

    def get_interfaces_status(self):
        pass

    def get_interfaces_trunk(self):
        pass

    def get_interface_description(self, interface: str):
        pass

    def get_neighbor(self, interface: str):
        pass

    def save_config(self):
        pass
