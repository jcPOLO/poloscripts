import csv
import os
import getopt
import sys
from typing import List, Dict

def args():
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


def get_from_file(file: str) -> List[str]:
    path =  os.getcwd()
    filename = f'{path}/{file}'
    return filename


def main():
    arg = args()
    print(arg)

    with open(arg) as f:
        data = csv.DictReader(f)
        for row in data:
            print(row["'DIRECCION'"])
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
