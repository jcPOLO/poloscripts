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
            message = "hostname '{}' must be a valid IPv4 address".format(a)
            raise ValidationException("fail-config", message)
        self._hostname = a

    @platform.setter
    def platform(self, a):
        platforms = ['ios', 'nxos']
        if a not in platforms:
            platforms_str = ', '.join(platforms)
            message = "platform '{}' is not in a supported. Supported: {}".format(a, platforms_str)
            raise ValidationException("fail-config", message)
        self._platform = a

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, a):
        if 65535 > int(a) > 0:
            self._port = int(a)
        else:
            message = "port '{}' is not a valid port number".format(a)
            raise ValidationException("fail-config", message)

    def run(self):
        return self.__dict__
