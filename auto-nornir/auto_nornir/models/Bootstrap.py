import configparser
import yaml
from csv import DictReader
from ..helpers import is_ip, check_directory, configure_logging
from typing import Dict

import logging

logger = logging.getLogger(__name__)


class Bootstrap(object):

    configure_logging(logger)

    def __init__(
        self,
        ini_file: str = '../.global.ini',
        csv_file: str = 'inventory.csv'
    ):

        self.ini_file = ini_file
        self.csv_file = csv_file
        self.load_inventory()

    def get_ini_vars(self) -> configparser:
        try:
            config = configparser.RawConfigParser()
            config.read(self.ini_file)
            return config
        except Exception as e:
            raise e

    # Return a dictionary from imported csv file
    def import_inventory_file(self) -> dict:
        platform = 'ios'
        try:
            result = {}

            with open(self.csv_file, 'r') as csv_file:
                csv_reader = DictReader(csv_file)
                fields = 'hostname'
                fields_set = set(fields.split(','))
                csv_fields_set = set(csv_reader.fieldnames)
                wrong_header_fields = list(fields_set - csv_fields_set)
                if not wrong_header_fields:
                    for row in csv_reader:
                        hostname = row['hostname'] if is_ip(row['hostname']) else None

                        # remove duplicated hostname
                        if hostname not in result.keys():
                            result[hostname] = {
                                'hostname': hostname,
                                'platform': platform,
                                'groups': [
                                    platform
                                ]
                            }
                else:
                    logger.info('{} not in csv header'.format(wrong_header_fields))
                    exit()

            return result
        except Exception as e:
            logger.error('{} Error'.format(e))
            raise e

    def load_inventory(self) -> None:
        self.create_hosts_yaml(self.import_inventory_file())

    @staticmethod
    def create_hosts_yaml(d: Dict) -> None:
        try:
            file = 'hosts.yaml'
            path = './inventory/'
            filename = f'{path}{file}'
            yml = yaml.dump(d)

            check_directory(path)

            with open(filename, 'w') as f:
                f.write(yml)
        except Exception as e:
            raise e
