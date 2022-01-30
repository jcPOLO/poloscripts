from nornir import InitNornir
from nornir.core import Nornir
from nornir.core.task import AggregatedResult
from nornir_utils.plugins.functions import print_result
from auto_nornir.main_functions import auto_nornir
from auto_nornir.models.menu import Menu
from auto_nornir.models.bootstrap import Bootstrap
from auto_nornir.models.filter import Filter
from auto_nornir.helpers import configure_logging
from auto_nornir.models.device import Device
# from tqdm import tqdm
import getpass
from typing import List
import logging
import output


logger = logging.getLogger(__name__)
CFG_FILE = 'config.yaml'


def main_task(devices: 'Nornir', selections: List, **kwargs) -> 'AggregatedResult':
    result = devices.run(
        task=auto_nornir,
        selections=selections,
        name=f'CONTAINER TASK',
        # severity_level=logging.DEBUG,
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

    # show filter options menu and return device inventory filtered
    filter_obj = Filter(nr)
    devices = filter_obj.nr

    # show the main menu
    menu_obj = Menu()
    selections = menu_obj.run()

    # before executing the tasks, ask for device credentials
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

    # ---------------------------------------------------
    output.facts_for_customer_csv(result)
    # ---------------------------------------------------

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
