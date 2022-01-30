import logging
import configparser
import yaml
import pathlib
from typing import Dict
from csv import DictReader
from auto_nornir.core.helpers import check_directory, configure_logging
from auto_nornir.core.models.device import Device
from auto_nornir.core.exceptions import ValidationException


logger = logging.getLogger(__name__)


class Bootstrap(object):
    """
    Class to create host.yaml Simple Inventory file and loading ini file with jinja2 config template vars

    Args:
        ini_file (str): Path to the ini file
        csv_file (str): Path to inventory file
        encoding (str): csv encoding type

    Attributes:
        groups (list): Associated group belonged
        data (dict): Extra data associated to the device
        devices (list): Device object generator counter
        platforms (list): Total device platforms registered in inventory.

    """
    configure_logging(logger)

    def __init__(
        self,
        ini_file: str = '../.global.ini',
        csv_file: str = 'inventory.csv',
        encoding: str = "utf-8"
    ):

        self.ini_file = pathlib.Path(ini_file).expanduser()
        self.csv_file = pathlib.Path(csv_file).expanduser()
        self.encoding = encoding
        # self.load_inventory()
        self.data_keys = set()

    def get_ini_vars(self) -> configparser:
        if self.ini_file.exists():
            config = configparser.RawConfigParser()
            config.read(self.ini_file)
            return config

    # Return a dictionary from imported csv file
    def import_inventory_file(self) -> dict:
        result = {}
        devices = {}

        with open(self.csv_file, 'r', encoding=self.encoding) as csv_file:
            csv_reader = DictReader(csv_file)
            fields = 'hostname'
            csv_fields = set(csv_reader.fieldnames)
            self.data_keys = csv_fields
            wrong_headers = False if fields in csv_fields else True
            if not wrong_headers:
                # create dict of Devices from CSV
                for row in csv_reader:
                    hostname = row['hostname'].strip()
                    if hostname not in devices.keys():
                        devices[hostname] = Device(**row)
            else:
                message = '{} not in csv header'.format(wrong_headers)
                logger.error(message)
                raise ValidationException("fail-config", message)
            for h, n in devices.items():
                result[h] = n.__dict__
            return result

    def load_inventory(self) -> None:
        self.create_hosts_yaml(self.import_inventory_file())

    @staticmethod
    def create_hosts_yaml(d: Dict) -> None:
        file = 'hosts.yaml'
        path = './inventory/'
        filename = f'{path}{file}'
        yml = yaml.dump(d)
        check_directory(path)
        with open(filename, 'w') as f:
            f.write(yml)
