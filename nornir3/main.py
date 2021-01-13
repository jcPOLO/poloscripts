from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
import getpass
from main_functions import make_magic
from models.Menu import Menu, Template
from models.Bootstrap import Bootstrap
from models.Filter import Filter
from tqdm import tqdm

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

    devices.inventory.defaults.password = password
    devices.inventory.defaults.username = username

    # Python program to show time by perf_counter()
    from time import perf_counter
    # Start the stopwatch / counter
    t1_start = perf_counter()

    print('----------- LOADING -----------')

    with tqdm(
        total=len(devices.inventory.hosts), desc='applying config',
    ) as make_magic_bar:
        with tqdm(
            total=len(devices.inventory.hosts), desc='writing config',
        ) as get_config_bar:
            with tqdm(
                total=len(devices.inventory.hosts), desc='making backup',
            ) as backup_config_bar:
                result = devices.run(task=make_magic,
                                    name=f'CONTAINER TASK',
                                    templates=templates,
                                    ini_vars=ini_vars,
                                    make_magic_bar=make_magic_bar,
                                    get_config_bar=get_config_bar,
                                    backup_config_bar=backup_config_bar
                                    )

        print_result(result)

    t1_stop = perf_counter()
    if result.failed_hosts:
        print(
            """
        Failed HOSTS:
            --------------------------------------
        """
        )
        for host in result.failed_hosts:
            print(f'Host: \x1b[1;31;40m{host} {devices.inventory.hosts[host].hostname}\x1b[0m')
            print(f'|_Error: \x1b[0;31;40m{result[host][1].exception}\x1b[0m')
            print(f'|_Task: {result.failed_hosts[host]}')

        print(
            """
        --------------------------------------
        """
        )
        retry = input("Do you want to retry tasks on failed hosts?[y/n]")
        if retry is 'y':
            print_result(result)


    elapsed_time = t1_stop - t1_start
    print("Elapsed time during the whole program in seconds:",
          '{0:.2f}'.format(elapsed_time))


if __name__ == '__main__':
    main()

