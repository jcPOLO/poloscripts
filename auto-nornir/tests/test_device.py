import pytest
from auto_nornir.models.Device import Device
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
    assert device.serial_number == serial_number
    assert device.port == int(port)


def test_ensure_device_instance_has_valid_ip():

    device_kwargs = {
        "hostname": '1.1.1.a',
        "platform": 'ios',
        "serial_number": '12345',
    }

    with pytest.raises(ValidationException):
        Device(**device_kwargs)


def test_ensure_device_instance_has_valid_platform():

    device_kwargs = {
        "hostname": '1.1.1.1',
        "platform": 'huawei',
        "serial_number": '12345',
    }

    with pytest.raises(ValidationException):
        Device(**device_kwargs)


def test_ensure_device_instance_has_valid_port():

    device_kwargs = {
        "hostname": '1.1.1.1',
        "platform": 'huawei',
        "serial_number": '12345',
        "port": '23'
    }

    with pytest.raises(ValidationException):
        Device(**device_kwargs)


def test_ensure_device_instance_has_extra_data():

    device_kwargs = {
        "hostname": '1.1.1.1',
        "platform": 'ios',
        "serial_number": '12345',
    }

    device = Device(**device_kwargs)

    assert device.serial_number == '12345'
