import configparser
import csv
import yaml
from helpers import get_platforms, is_ip, check_directory
from typing import Dict


class Bootstrap(object):

    def __init__(self, ini_file='.global.ini', csv_file='inventory.csv', **kwargs):

        self.ini_file = ini_file
        self.csv_file = csv_file
        self.load_inventory()
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_ini_vars(self) -> configparser:
        try:
            config = configparser.RawConfigParser()
            config.read(self.ini_file)
            return config
        except Exception as e:
            raise e

    def get_config_vars(self) -> dict:
        try:
            config = configparser.RawConfigParser()
            config.read(self.ini_file)
            r = config
            return dict(r['GLOBAL'])
        except Exception as e:
            raise e

    # Return a dictionary from imported csv file
    def import_inventory_file(self) -> dict:
        """
        host: <name>
            hostname: <ip>
            platform: <ios|huawei>
            groups:
                - <ios_telnet|ios|huawei>
                - [site code|role type|...]
            [
            data:
                site: '<site code>'
                ip: <migration ip>
            ]

        """
        platforms = get_platforms()
        try:
            result = {}

            with open(self.csv_file, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)

                fields = 'site_code,host,hostname,is_telnet,platform,ip,mask,new_dg,current_dg'

                wrong_header_fields = list(set(fields.split(',')) - set(csv_reader.fieldnames))
                if not wrong_header_fields:
                    for row in csv_reader:
                        site_code = row['site_code']
                        ip = row['ip']
                        mask = row['mask']
                        current_dg = row['current_dg']
                        new_dg = row['new_dg']

                        hostname = row['hostname'] if is_ip(row['hostname']) else None
                        host = row['host'].replace(" ", "_") or None
                        platform = row['platform'].lower().replace(" ", "_") if row['platform'].lower().replace(" ", "_") in platforms else None
                        is_telnet = 't' in row['is_telnet'].lower() and 's' not in row['is_telnet'].lower()
                        # device_type = row[9].replace(" ", "_") or None
                        # serial = row[10].replace(" ", "_") or None

                        # remove duplicated hostname
                        if None not in (hostname, host, platform) and host not in result.keys():
                            result[host] = {
                                'hostname': hostname,
                                'platform': platform,
                                'groups': [
                                    'ios_telnet' if is_telnet and platform == 'ios' else platform
                                ],
                                'data': {
                                    'site_code': site_code,
                                    'ip': ip,
                                    'mask': mask,
                                    'current_dg': current_dg,
                                    'new_dg': new_dg,
                                    'role': {},
                                    # 'device_type': platform,
                                    # 'serial': serial,
                                }

                            }
                            if is_telnet and platform == 'ios':
                                result[host]['port'] = 23
                else:
                    print('{} not in csv header'.format(wrong_header_fields))
                    exit()

            return result
        except Exception as e:
            print(platforms)
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
