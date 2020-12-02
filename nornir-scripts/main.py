from nornir import InitNornir
from nornir.plugins.functions.text import print_result
import getpass
from main_functions import make_magic
from models.Menu import Menu, Template
from models.Bootstrap import Bootstrap
from models.Filter import Filter


CFG_FILE = 'config.yaml'
EXCLUDED_VLANS = [1, 1002, 1003, 1004, 1005]


def main() -> None:


    # creates hosts.yaml from csv file, ini file could be passed as arg, by default .global.ini
    bootstrap = Bootstrap()

    # configparser object, similar to dict object
    ini_vars = bootstrap.get_ini_vars()

    # initialize Nornir object
    nr = InitNornir(config_file=CFG_FILE)

    filter_obj = Filter(nr)
    devices = filter_obj.nr

    # show the main menu
    menu_obj = Menu()
    menu = menu_obj.run()

    if isinstance(menu, Template):
        templates = menu.templates
    else:
        templates = 'save_config'

    username = input("\nUsername:")
    password = getpass.getpass()

    nr.inventory.defaults.password = password
    nr.inventory.defaults.username = username

    # Python program to show time by perf_counter()
    from time import perf_counter
    # Start the stopwatch / counter
    t1_start = perf_counter()

    print('----------- LOADING -----------')

    result = devices.run(task=make_magic,
                         name=f'CONTAINER TASK',
                         templates=templates,
                         ini_vars=ini_vars
                         )

    print_result(result)

    if result.failed_hosts:
        print(
            """
        Failed HOSTS:
            --------------------------------------
        """
        )
        for host in result.failed_hosts:
            print(f'Host: {host}')
            print(f'|__{result.failed_hosts[host].exception.__class__.__name__}')

        print(
            """
        --------------------------------------
        """
        )

    t1_stop = perf_counter()

    elapsed_time = t1_stop - t1_start
    print("Elapsed time during the whole program in seconds:",
          '{0:.2f}'.format(elapsed_time))


if __name__ == '__main__':
    main()

