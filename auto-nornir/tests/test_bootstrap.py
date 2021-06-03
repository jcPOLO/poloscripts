import pytest
from auto_nornir.models.Bootstrap import Bootstrap
from io import StringIO
import csv


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


def test_import_inventory_file():

    with pytest.raises(FileNotFoundError):
        Bootstrap(
            csv_file='not_found.csv'
        )
    bootstrap = Bootstrap(
        csv_file='auto_nornir/inventory.csv'
    )
    hosts_dict = bootstrap.import_inventory_file()
    assert isinstance(hosts_dict, dict)


def test_validate_devices():

    csv_file = mock_csv_good()

