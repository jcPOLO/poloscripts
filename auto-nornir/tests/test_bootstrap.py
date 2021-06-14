import pytest
from auto_nornir.core.models.bootstrap import Bootstrap
from auto_nornir.core.exceptions import ValidationException
from io import StringIO
import csv
import os


dir_path = os.path.dirname(os.path.realpath(__file__))


def mock_csv_bad():
    csv_file = StringIO()
    fieldnames = ['hostname', 'platform', 'serial_number']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'hostname': '1.1.1.1', 'platform': 'ios', 'serial_number': '12345'})
    writer.writerow({'hostname': '2.2.2.2', 'platform': 'nxos', 'serial_number': '23456'})
    writer.writerow({'hostname': '3.3.3.3', 'platform': 'ios', 'serial_number': '34567'})
    csv_file.seek(0)
    return csv_file


def mock_csv_good():
    csv_file = StringIO()
    fieldnames = ['hostname', 'platform', 'serial_number']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'hostname': '1.1.1.1', 'platform': 'ios', 'serial_number': '12345'})
    writer.writerow({'hostname': '2.2.2.2', 'platform': 'nxos', 'serial_number': '23456'})
    writer.writerow({'hostname': '3.3.3.3', 'platform': 'ios', 'serial_number': '34567'})
    csv_file.seek(0)
    return csv_file


def test_import_inventory_file_good():
    with pytest.raises(FileNotFoundError):
        bootstrap = Bootstrap(
            csv_file='not_found.csv'
        )
        bootstrap.load_inventory()

    bootstrap = Bootstrap(
        csv_file=f'{dir_path}/inventory/inventory.csv'
    )
    hosts_dict = bootstrap.import_inventory_file()
    assert isinstance(hosts_dict, dict)
    for n, h in hosts_dict.items():
        assert 'hostname' in hosts_dict[n].keys()
        assert 'platform' in hosts_dict[n].keys()
        assert 'port' in hosts_dict[n].keys()


def test_import_inventory_file_bad():
    with pytest.raises(ValidationException):
        bootstrap = Bootstrap(
            csv_file=f'{dir_path}/inventory/inventory_bad.csv'
        )
        bootstrap.load_inventory()
