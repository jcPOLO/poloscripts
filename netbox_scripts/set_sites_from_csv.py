import csv
import os
import getopt
import sys
from typing import List, Dict
from slugify import slugify
import pynetbox
import json


def load_api():
    return pynetbox.api(
        'http://netbox.aragon.es',
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
    nb = load_api()

    # albalatillo,Albalatillo,Provincia Zaragoza
    #region = nb.dcim.regions.create(region)

    with open(arg, encoding="utf8") as f:
        #data = csv.DictReader(f, quotechar="'", delimiter=';')
        data = csv.DictReader(f)
        print(data.fieldnames)

        for row in data:
            # poblacion = row["POBLACION"].title()
            # provincia = row["PROVINCIA"].capitalize()
            region = {
                "name": '',
                "slug": '',
                "parent": {
                    "name": '' 
                }
            }

            name = row['name']
            slug = row['slug']
            parent = row['parent']
            # print(f'Processing {name},{slug},{parent}...')
            try:
                r = nb.dcim.regions.create(name=name, slug=slug, parent={'name':parent})
                print("EXITO",r)
            except Exception:
                print(f'Error {name},{slug},{parent}...')
                pass


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
