import getopt
import sys
import os
import ipaddress
import subprocess
import time


def args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hn:', ['help', 'net='])
    except getopt.GetoptError:
        print(f'Usa -[n] [net]')
        sys.exit(2)

    if len(opts) != 0:
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print(f'Usa -[f] [filename]')
                sys.exit()
            elif opt in ('-n', "--net"):
                return str(arg)
            else:
                print(f'Usa -[f] [filename]')
                sys.exit(2)
    else:
        print(f'Usa -[f] [filename]')

def main():
    net = ''
    result = []
    p = {}
    i = 0

    net = args()

    try:
        network = ipaddress.ip_network(net)
        print(f'Working with {network}')

        # 1.52 sec
        for host in network.hosts():
            host = str(host)

            p[host] = subprocess.Popen(
                ['ping', '-c2', '-n', '-i0.5', '-W1', host],
                shell=False,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
            i += 1
            print(i,end='_')
            if i > 10000:
                while p:
                    for host, proc in p.items():
                        print('.', end='')
                        if proc.poll() is not None:
                            del p[host]
                            i -= 1
                            if proc.returncode == 0:
                                result.append(host)
                            break

        while p:
            for host, proc in p.items():
                print('.', end='')
                if proc.poll() is not None:
                    del p[host]
                    if proc.returncode == 0:
                        result.append(host)
                    break

    except TypeError:
        print("error")
        pass

    file = net.replace('/', '_') + '.txt'
    with open(file, 'w+') as f:
        for host_ip in result:
            f.write(host_ip + '\n')


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

