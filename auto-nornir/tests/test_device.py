import pytest
from auto_nornir.models.device import Device
from auto_nornir.exceptions import ValidationException


def test_ensure_device_instance_is_valid():
    serial_number = "123456"
    platform = "ios"
    hostname = "1.1.1.1"
    port = "23"

    device_kwargs = {
        "hostname": hostname,
        "platform": platform,
        "serial_number": serial_number,
        "port": port
    }

    device = Device(**device_kwargs)
    assert device.platform == platform
    assert device.hostname == hostname
    assert device.data['serial_number'] == serial_number
    assert device.port == int(port)


def test_ensure_device_instance_has_valid_ip():

    device_kwargs = {
        "hostname": '1.1.1.a',
        "platform": 'ios',
        "serial_number": '12345',
    }
    with pytest.raises(ValidationException):
        Device(**device_kwargs)

    device_kwargs["hostname"] = ''
    with pytest.raises(ValidationException):
        Device(**device_kwargs)

    device_kwargs["hostname"] = None
    with pytest.raises(ValidationException):
        Device(**device_kwargs)

    device_kwargs["hostname"] = '1.1.1.1'
    device = Device(**device_kwargs)
    assert device.hostname == '1.1.1.1'


def test_ensure_device_instance_has_valid_platform():

    device_kwargs = {
        "hostname": '1.1.1.1',
        "platform": 'anchoas',
        "serial_number": '12345',
    }

    with pytest.raises(ValidationException):
        Device(**device_kwargs)

    device_kwargs["platform"] = ''
    with pytest.raises(ValidationException):
        Device(**device_kwargs)

    device_kwargs["platform"] = 'ios'
    device = Device(**device_kwargs)
    assert device.platform == 'ios'


def test_ensure_device_instance_has_valid_port():

    device_kwargs = {
        "hostname": '1.1.1.1',
        "platform": 'ios',
        "serial_number": '12345',
        "port": '70000'
    }

    with pytest.raises(ValidationException):
        Device(**device_kwargs)

    device_kwargs["port"] = 'abc'

    with pytest.raises(ValidationException):
        Device(**device_kwargs)

    device_kwargs["port"] = '23'
    device = Device(**device_kwargs)
    assert device.port == 23


def test_ensure_device_instance_has_extra_data():

    device_kwargs = {
        "hostname": '1.1.1.1',
        "platform": 'ios',
        "serial_number": '12345',
    }

    device = Device(**device_kwargs)
    assert device.data['serial_number'] == '12345'


def test_get_devices():
    total = len(Device.get_devices())
    device_kwargs = {
        "hostname": '1.1.1.1',
        "platform": 'ios',
        "serial_number": '12345',
    }
    Device(**device_kwargs)
    assert len(Device.get_devices()) == total + 1


def test_get_devices_data_keys_and__dict__():
    device_kwargs = {
        "hostname": '1.1.1.1',
        "platform": 'ios',
        "serial_number": '12345',
        'site': 'zaragoza'
    }
    Device.devices = []
    device = Device(**device_kwargs)
    data_keys = Device.get_devices_data_keys()
    assert ', '.join(data_keys) == 'serial_number, site'
    assert dict(device) == {
        "hostname": '1.1.1.1',
        "platform": 'ios',
        "port": 22,
        "data": {
            "serial_number": '12345',
            'site': 'zaragoza'
        },
        "groups": ['ios']
    }
