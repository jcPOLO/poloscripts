from auto_nornir.models.ios import Ios
from auto_nornir.models.huawei import Huawei
from nornir.core.task import Task

IOS = 'ios'
HUAWEI = 'huawei'


class PlatformFactory:

    @staticmethod
    def get_platform(task: Task):
        if task.host.platform == IOS:
            return Ios(task)
        if task.host.platform == HUAWEI:
            return Huawei(task)
        return None
