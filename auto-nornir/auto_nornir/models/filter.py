from nornir.core.filter import F
import os
import sys


class Filter(object):

    platforms = ['ios']
    keys = ['']

    def __init__(self, nr, filter_parameters=dict) -> None:

        self.choices = {
            "1": self.by_platform,
            "2": self.by_hostname,
            "3": self.by_field,
            "z": self.clear,
            "s": self.show,
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
           3. Other fields...

           --------------------------------------------------------------------

           ENTER to continue      s. Show selection       z. Clear selections

           e. Exit

           """)

    @staticmethod
    def devices_filtered(self, text='All devices selected:') -> str:
        msg = text + '\n'
        i = 0
        for device in self.nr.inventory.hosts:
            i += 1
            msg += f' \
                {i} \
                {self.nr.inventory.hosts[device].platform} \
                {self.nr.inventory.hosts[device].name} \
                {self.nr.inventory.hosts[device].hostname}\n'
        return msg

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
        msg = self.devices_filtered(self)
        self.run(msg)

    def clear(self) -> None:
        self.nr = self.initial_nr
        self.run()
        print(f'All filters cleared.\n')

    @staticmethod
    def exit() -> None:
        print(f'Bye!\n')
        sys.exit()

    def by_platform(self):
        nr = self.nr

        platforms = set()

        for host in nr.inventory.hosts.values():
            platforms.add(host.platform)

        platform = input(
            f"Platform to filter by: - {', '.join(platforms)}:"
        ).lower()

        if platform in platforms:
            devices = nr.filter(F(platform=platform))
            self.nr = devices
            msg = self.devices_filtered(self, 'Filtered by {platform}:')
            self.run(msg)
        else:
            msg = self.devices_filtered(self)
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
            msg = self.devices_filtered(self, 'Filtered by IP:')
            self.run(msg)

        else:
            msg = self.devices_filtered(self)
            self.run(msg)

    def by_field(self):
        field = input(f"Field to filter by: - {', '.join(self.keys)}:").lower()

        if field in self.keys:
            nr = self.nr

            values = set()

            for host in nr.inventory.hosts.values():
                values.add(host[field])

            value = input(
                f"{field} to filter by: - {', '.join(values)}:"
            ).lower()

            if value in values:
                devices = nr.filter(F(**{field: str(value)}))
                self.nr = devices
                msg = self.devices_filtered(self, 'Filtered by {field}')
                self.run(msg)

        else:
            msg = self.devices_filtered(self)
            self.run(msg)

    @staticmethod
    def show_filtering_options(nr, fields=dict):
        if fields:
            devices = nr.filter(F(groups__contains=fields))
        else:
            devices = nr.filter(F(groups__contains="ios"))
        print(devices.inventory.hosts.keys())
        pass
