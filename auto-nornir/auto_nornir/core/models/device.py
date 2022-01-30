from auto_nornir.core.exceptions import ValidationException
from auto_nornir.core.helpers import is_ip


# supported platforms at the moment
PLATFORMS = ['ios', 'nxos']


class Device(object):
    """
    Class to validate every devices field loaded from CSV to YAML SimpleInventory

    Args:
        hostname (str): Device management IP address
        platform (str): Device nornir device_type
        port (int): Connecting port for management IP

    Attributes:
        groups (list): Associated group belonged
        data (dict): Extra data associated to the device
        devices (list): Device object generator counter
        platforms (list): Total device platforms registered in inventory.

    """
    devices = []
    platforms = []

    # TODO: not the best way to create groups.
    def __init__(
            self,
            hostname,
            platform='ios',
            port='22',
            **kwargs
    ):
        self.hostname = self.validate_hostname(hostname)
        self.platform = self.validate_platform(platform)
        self.port = self.validate_port(port)
        self.groups = [self.platform]
        self.data = kwargs
        # for k, v in kwargs.items():
        #     setattr(self, k, v)

        self.devices = self.devices.append(self)

        # TODO: this should not appear in host.yaml file as an attribute.
        self.platforms = self.platforms.append(self.platform)

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
        try:
            a = a.strip()
            if not a:
                message = "hostname '{}' hostname cannot be empty".format(a)
                raise ValidationException("fail-config", message)
            if is_ip(a):
                return a
        except AttributeError:
            pass
        message = "hostname '{}' must be a valid IPv4 address".format(a)
        raise ValidationException("fail-config", message)

    @staticmethod
    def validate_port(a):
        try:
            a = a.strip()
            if 65535 > int(a) > 0:
                return int(a)
        except AttributeError:
            pass
        except ValueError:
            pass
        message = "port '{}' is not a valid port number".format(a)
        raise ValidationException("fail-config", message)

    @classmethod
    def get_devices(cls):
        return cls.devices

    @classmethod
    def get_devices_data_keys(cls):
        return cls.devices[0].data.keys()

    @classmethod
    def get_devices_platform(cls):
        return cls.platforms

    def _device_dict(self):
        return {
            'hostname': self.hostname,
            'platform': self.platform,
            'port': self.port,
            'groups': [
                self.platform
            ],
            'data': self.data
        }

    def __iter__(self):
        for k, v in self._device_dict().items():
            yield k, v
