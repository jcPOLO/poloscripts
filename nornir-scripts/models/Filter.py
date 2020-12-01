from typing import Any, Dict, Optional, List
from nornir.core.filter import F
import os, sys


class Filter(object):

    platforms = ['ios', 'huawei']

    def __init__(self, nr, filter_parameters={}) -> None:

        self.choices = {
            "1": self.by_platform,
            "2": self.by_hostname,
            "3": self.by_ip,
            "4": self.by_host,
            "5": self.by_site_code,
            "s": self.show,
            "z": self.clear,
            "e": self.exit,

        }
        self.initial_nr = nr
        self.nr = nr
        filter_parameters = filter_parameters or {}
        self.filter_parameters = filter_parameters
        self.run()

    @staticmethod
    def display_menu() -> None:
        os.system('clear')
        print("""
           Filter by:

           1. Platform
           2. IP
           3. New IP
           4. Hostname
           5. Site code

           -------------------------------------------------------------------------------

           s. Show selection       z. Clear selections

           e. Exit

           """)

    def run(self, msg='') -> None:

        self.display_menu()
        if msg:
            print(msg)

        while True:
            choice = input("Enter an option: ")
            if choice.strip() in self.choices.keys():
                field = self.choices.get(choice.strip())
                return field()
            else:
                return self.nr

    def show(self) -> None:
        msg = self.nr.inventory.hosts
        self.run(msg)

    def clear(self) -> None:
        self.nr = self.initial_nr
        self.run()
        print(f'All filters cleared.\n')

    def exit(self) -> None:
        print(f'Bye!\n')
        sys.exit()

    def by_platform(self):
        nr = self.nr

        platforms = set()

        for host in nr.inventory.hosts.values():
            platforms.add(host.platform)

        platform = input(f"Platform to filter by: - {', '.join(platforms)}:").lower()

        if platform in platforms:
            devices = nr.filter(F(platform=platform))
            self.nr = devices
            msg = f'Filtered by platform: {platform}'
            self.run(msg)
        else:
            msg = f'All platforms selected.'
            self.run(msg)

    def by_hostname(self):
        nr = self.nr

        hostnames = set()

        for host in nr.inventory.hosts.values():
            hostnames.add(host.hostname)

        hostname = input(f"IP to filter by: - {', '.join(hostnames)}:").lower()

        if hostname in hostnames:
            devices = nr.filter(F(hostname=hostname))
            self.nr = devices
            msg = f'Filtered by current device IP: {hostname}'
            self.run(msg)

        else:
            msg = f'All devices selected.'
            self.run(msg)

    def by_ip(self):
        pass

    def by_host(self):
        pass

    def by_site_code(self):
        nr = self.nr

        sites = set()

        for host in nr.inventory.hosts.values():
            sites.add(host['site_code'])

        site = input(f"Platform to filter by: - {', '.join(sites)}:").lower()

        if site in nr.inventory.groups:
            devices = nr.filter(F(site=site))
            self.nr = devices
            msg = f'Filtered by site: {site}'
            self.run(msg)

        else:
            msg = f'All sites selected.'
            self.run(msg)

    def by_field(self, field):
        pass

    def show_filtering_options(self, nr, fields={}):
            if fields:
                devices = nr.filter(F(groups__contains=fields))
            else:
                devices = nr.filter(F(groups__contains="ios"))
            print(devices.inventory.hosts.keys())
            pass