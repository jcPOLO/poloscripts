import pytest
from auto_nornir.models.Device import Device
from auto_nornir.exceptions import ValidationException


def test_ensure_device_instance_is_valid():
    serial_number = "123456"
    platform = "ios"
    hostname = "1.1.1.1"

    device_kwargs = {
        "hostname": hostname,
        "platform": platform,
        "serial_number": serial_number,
    }

    device = Device(**device_kwargs)

    assert device.platform == platform
    assert device.hostname == hostname


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


def test_ensure_device_instance_has_extra_data():

    device_kwargs = {
        "hostname": '1.1.1.1',
        "platform": 'ios',
        "serial_number": '12345',
    }

    device = Device(**device_kwargs)

    assert device.serial_number == '12345'
