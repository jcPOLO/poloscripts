import ipaddress
from ..exceptions import ValidationException
from ..helpers import is_ip


class Device(object):

    def __init__(
            self,
            hostname,
            platform='ios',
            port='22',
            **kwargs
    ):
        """
        Args:
            hostname (str): Device management IP address
            platform (str): Device nornir device_type
            port (int): Connecting port for management IP
            name (str): Device hostname
        """

        self.hostname = hostname
        self.platform = platform
        self.port = port
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def hostname(self):
        return self._hostname

    @property
    def platform(self):
        return self._platform

    @hostname.setter
    def hostname(self, a):
        if not a:
            raise ValidationException("hostname cannot be empty")
        if not is_ip(a):
            raise ValidationException(
                "fail-config",
                "hostname '{}' must be a valid IPv4 address".format(a)
            )
        self._hostname = a

    @platform.setter
    def platform(self, a):
        platforms = ['ios', 'nxos']
        if a not in platforms:
            raise ValidationException(
                "fail-config",
                "platform '{}' is not in a supported. Supported: {}".format(
                    a,
                    ', '.join(platforms)
                )
            )
        self._platform = a

    def run(self):
        return self.__dict__
