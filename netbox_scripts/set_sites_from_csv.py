import csv
import os
import getopt
import sys
from typing import List, Dict
from slugify import slugify
import pynetbox


def load_api():
    return pynetbox.api(
        'http://aragon.netbox.com',
        token='65fa3de4a2de953dca49e88ffdb5a1daebfcc4c7'
    )


def get_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:', ['help', 'file='])
    except getopt.GetoptError:
        print(f'Usa -[f] [file]')
        sys.exit(2)

    if len(opts) != 0:
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print(f'Usa -[f|n] [filename|network] ')
                sys.exit()
            elif opt in ('-f', '--file'):
                return get_from_file(str(arg))
            else:
                print(f'Usa -[f] [filename]')
                sys.exit(2)
    else:
        print(f'Usa -[f] [filename]')


def get_from_file(file: str) -> str:
    path = os.getcwd()
    filename = f'{path}/{file}'
    return filename


def main():
    arg = get_args()
    i = 0
    nb = load_api()

    print(nb.dcim.devices.all())
    exit()

    with open(arg) as f:
        data = csv.DictReader(f, quotechar="'", delimiter=';')
        print(data.fieldnames)
        for row in data:
            i += 1
            poblacion = row["POBLACION"].title()
            provincia = row["PROVINCIA"].capitalize()
            if poblacion:
                print(f'{slugify(poblacion)},{poblacion},Provincia {provincia}')
                if i == -1:
                    break


if __name__ == "__main__":
    # Python program to show time by perf_counter()
    from time import perf_counter

    # Start the stopwatch / counter
    t1_start = perf_counter()

    main()

    t1_stop = perf_counter()
    elapsed_time = t1_stop - t1_start
    print("Elapsed time during the whole program in seconds:",
          '{0:.2f}'.format(elapsed_time))
