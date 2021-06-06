from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
import getpass
from main_functions import auto_nornir
# from models.Menu import Menu
from models.Bootstrap import Bootstrap
# from models.Filter import Filter
# from tqdm import tqdm
from typing import Dict, List
from helpers import configure_logging

import logging


CFG_FILE = 'config.yaml'
EXCLUDED_VLANS = [1, 1002, 1003, 1004, 1005]

logger = logging.getLogger(__name__)


def main_task(
    devices: 'Nornir',
    selections: List,
    **kwargs
) -> 'AggregatedResult':

    result = devices.run(
        task=auto_nornir,
        selections=selections,
        name=f'CONTAINER TASK',
        **kwargs
    )
    return result


def on_failed_host(devices: 'Nornir', result: 'AggregatedResult'):
    print(
        """
        Failed HOSTS:
        --------------------------------------
        """
    )
    for host in result.failed_hosts:
        logger.error(f'Host: \x1b[1;31;40m{host} \
            {devices.inventory.hosts[host].hostname}\x1b[0m')
        logger.error(f'|_Error: \x1b[0;31;40m{result[host][1].exception}\x1b[0m')
        logger.error(f'|_Task: {result.failed_hosts[host]}')

    print(
        """
        --------------------------------------
        """
    )


def main() -> None:
    # configure logger
    configure_logging(logger)

    # creates hosts.yaml from csv file, ini file could be passed as arg,
    # by default .global.ini
    bootstrap = Bootstrap()
    bootstrap.load_inventory()

    # initialize Nornir object
    nr = InitNornir(config_file=CFG_FILE)
    devices = nr

    # show filter options menu and return device inventory filtered
    # filter_obj = Filter(nr)
    # devices = filter_obj.nr

    # show the main menu
    # menu_obj = Menu()
    # selections = menu_obj.run()
    selections = ['get_facts']

    username = input("\nUsername:")
    password = getpass.getpass()

    devices.inventory.defaults.password = password
    devices.inventory.defaults.username = username

    # Python program to show time by perf_counter()
    from time import perf_counter
    # Start the stopwatch / counter
    t1_start = perf_counter()

    logger.info('----------- LOADING -----------\n')

    result = main_task(devices, selections)
    print_result(result)

    t1_stop = perf_counter()
    while result.failed_hosts:
        on_failed_host(devices, result)
        retry = input("Do you want to retry tasks on failed hosts?[y/n]")
        if retry == 'y':
            params = {
                'on_good': False,
                'on_failed': True,
                'on_retry': True
            }

            result = main_task(devices, selections, **params)
            print_result(result)
        else:
            break

    elapsed_time = t1_stop - t1_start
    print(
        "Elapsed time during the whole program in seconds:",
        '{0:.2f}'.format(elapsed_time))


if __name__ == '__main__':
    main()
