from auto_nornir.exceptions import ValidationException
from auto_nornir.helpers import is_ip


PLATFORMS = ['ios', 'nxos']


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

        self.hostname = self.validate_hostname(hostname)
        self.platform = self.validate_platform(platform)
        self.port = self.validate_port(port)
        self.groups = [self.platform]
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def validate_platform(a):
        a = a.strip()
        platforms = PLATFORMS
        if a not in platforms:
            platforms_str = ', '.join(platforms)
            message = "platform '{}' is not in a supported. Supported: {}".format(a, platforms_str)
            raise ValidationException("fail-config", message)
        return a

    @staticmethod
    def validate_hostname(a):
        a = a.strip()
        if not a:
            raise ValidationException("hostname cannot be empty")
        if not is_ip(a):
            message = "hostname '{}' must be a valid IPv4 address".format(a)
            raise ValidationException("fail-config", message)
        return a

    @staticmethod
    def validate_port(a):
        a = a.strip()
        if 65535 > int(a) > 0:
            return int(a)
        if a is None:
            message = "port '{}' is not a valid port number".format(a)
            raise ValidationException("fail-config", message)
