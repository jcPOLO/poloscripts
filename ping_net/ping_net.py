import getopt
import sys
import os
import ipaddress
import subprocess
from typing import List, Dict, Set


MAX_PROCESS = 10000


def args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hn:f:', ['help', 'net=', 'file='])
    except getopt.GetoptError:
        print(f'Usa -[n] [net]')
        sys.exit(2)

    if len(opts) != 0:
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print(f'Usa -[f|n] [filename|network] ')
                sys.exit()
            elif opt in ('-n', "--net"):
                r = [str(arg)]
                return r
            elif opt in ('-f', '--file'):
                return get_nets_from_file(str(arg))
            else:
                print(f'Usa -[f] [filename]')
                sys.exit(2)
    else:
        print(f'Usa -[f] [filename]')


def get_nets_from_file(file: str) -> List[str]:
    path =  os.getcwd()
    filename = f'{path}/{file}'
    with open(filename) as f:
        nets = f.read()
    r = nets.split()
    return r


def process_childs(pings: Dict, result: List, pings_buffered: int) -> None:
    while pings:
        for host, ping in pings.items():
            # check if the child process has ended
            if ping.poll() is not None:
                del pings[host]
                pings_buffered -= 1
                if ping.returncode == 0:
                    result.append(host)
                break


def main():

    nets = args()

    try:
        for net in nets:
            result = []
            pings = {}
            i = 0

            network = ipaddress.ip_network(net)
            print(f'Working with {network}')

            for host in network.hosts():
                host = str(host)

                pings[host] = subprocess.Popen(
                    ['ping', '-c2', '-n', '-i0.5', '-W1', host],
                    shell=False,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                i += 1
                if i > MAX_PROCESS:
                    process_childs(pings, result, i)
                    
            process_childs(pings, result, i)

            file = net.replace('/', '_') + '.txt'
            with open(file, 'w+') as f:
                for host_ip in result:
                    f.write(host_ip + '\n')

    except TypeError:
        print("error")
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

