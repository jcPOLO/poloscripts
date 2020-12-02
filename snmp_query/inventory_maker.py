import datetime
import getopt
import re
import socket
import sys
import os
from multiprocessing import Process
from pysnmp.hlapi import *
import configparser


class SnmpQuery(object):

    def __init__(self, ip, timeout=1, ini_file='../.global.ini'):

        self.ip = ip
        self.community = ''
        self.timeout = timeout
        self.hostname = ''
        self.connectivity = ''
        self.platform = ''
        self.default_route = ''
        self.mask = ''
        self.ini_file = ini_file

    def get_oid(self, oid):
        error_indication, error_status, error_index, var_binds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community, mpModel=1),  # SNMPv2c
                   UdpTransportTarget((self.ip, 161), timeout=self.timeout),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid)))
        )
        if error_indication:
            return 'SNMP_error'
        elif error_status:
            print('%s at %s' % (error_status.prettyPrint(),
                                error_index and var_binds[int(error_index) - 1][0] or '?'))
        else:
            for var_bind in var_binds:
                t = ' '.join([x.prettyPrint() for x in var_bind])
                if 'OID' in t:
                    t = 'SNMP_error'
                return t

    def snmpwalk_oid(self, oid):
        t = []
        g = nextCmd(SnmpEngine(),
                    CommunityData(self.community, mpModel=1),
                    UdpTransportTarget((self.ip, 161), timeout=self.timeout),
                    ContextData(),
                    ObjectType(ObjectIdentity(oid)),
                    lexicographicMode=False)
        queries = list(g)
        counter = 0
        while counter < len(queries):
            query = queries[counter]
            var_bind = query[3]
            _snmp_query = str(var_bind[0])
            _snmp_query = _snmp_query.split(" = ")
            _index = _snmp_query[0].split(".")
            _index = _index[len(_index) - 1]
            _value = str(_snmp_query[1])

            snmp = {"index": _index, "value": _value}
            if 'OID' in _value:
                snmp = {"index": _index, "value": "SNMP_error"}
                t.append(snmp)
            elif _value != '':
                t.append(snmp)
            counter += 1
        return t

    def get_ini_vars(self) -> dict:
        try:
            config = configparser.RawConfigParser()
            config.read(self.ini_file)
            return dict(config['SNMP'])
        except Exception as e:
            raise e

    def get_hostname(self):
        communities = self.get_ini_vars()
        communities = communities['communities'].split(',')

        self.community = communities[0]
        temp = self.get_oid('1.3.6.1.2.1.1.5.0')
        if temp == "SNMP_error":
            self.hostname = ""
        else:
            temp = re.search(r"(.*) (.*)", temp).group(2)
            temp = re.split('[,.]', temp)
            if len(temp) >= 1:
                self.hostname = temp[0]
        i = 1
        while self.hostname == '' and i < len(communities):
            self.community = communities[i]
            temp = self.get_oid('1.3.6.1.2.1.1.5.0')
            if temp == "SNMP_error":
                self.hostname = ""
            else:
                temp = re.search(r"(.*) (.*)", temp).group(2)
                temp = re.split('[,.]', temp)
                if len(temp) >= 1:
                    self.hostname = temp[0]
            i += 1
        if self.hostname == "SNMP_error":
            self.community = '-'
            self.hostname = '-'
            self.connectivity = '-'
            self.platform = '-'
        self.hostname = self.strfilter(self.hostname)
        return self.hostname

    def get_connection(self):
        if self.connectivity == '':
            ports = {"t": 23, "s": 22, "w": 80, "+": 443}
            for key, port_number in ports.items():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.0)
                result = s.connect_ex((self.ip, port_number))
                if result == 0:
                    self.connectivity = self.connectivity + str(key)
                s.close()
        return self.connectivity

    def get_platform(self):
        if self.platform == '':
            temp = self.get_oid('1.3.6.1.2.1.1.1.0')
            temp = temp.replace("\r\n", " ")
            patterns = {
                "Huawei": "huawei",
                "BIG-IP": "f5",
                "Pulse Secure": "junos",
                "Adaptive Security Appliance": "asa",
                "Cisco Integrated Management Controller": "ucs",
                "Content Switch SW": "ios",
                "VMware": "vmware",
                "ESX": "ucs",
                "NX-OS": "nxos",
                "isco": "ios",
                "Managed Switch": "ios",
                "Smart Switch": "ios",
                "Teldat": "teldat",
                "Windows": "windows",
                "Service Release": "alcatel",
                "OAW-4604": "alcatel",
                "Alcatel": "alcatel",
                "Omni": "alcatel",
                "Palo Alto": "panos",
                "Linux": "linux",
                "ProCurve": "hp"
            }
            for pattern, vendor in patterns.items():
                if pattern in temp:
                    if self.platform == '':
                        self.platform = self.strfilter(vendor)
        return self.platform

    def get_default_route(self):
        if self.default_route == '':
            if "huawei" in self.platform:
                temp = self.get_oid('iso.3.6.1.2.1.4.21.1.7.0.0.0.0')
            if "ios" in self.platform:
                temp = self.get_oid('iso.3.6.1.2.1.16.19.12.0')
            result = temp.replace("\r\n", " ").split()[-1]
            self.default_route = result
            return self.default_route

    def get_mask(self):
        if self.mask == '':
            temp = self.get_oid(f'iso.3.6.1.2.1.4.20.1.3.{self.ip}')
            result = temp.replace("\r\n", " ").split()[-1]
            self.mask = result
            return self.mask

    @staticmethod
    def strfilter(string=''):
        string = string.strip()
        string = string.replace(",", "_")
        return string


def get_saved_facts(_ip_address_):
    filename = './output/' + _ip_address_ + '.txt'
    saved_facts = []
    saved_timestamps = []
    if os.path.isfile(filename):
        with open(filename) as file:
            lines = file.readlines()
        for line in lines:
            if '~' in line:
                saved_fact = line.split("~,")[1]
                saved_fact = saved_fact.replace("\n", "")
                saved_facts.append(saved_fact)
                saved_timestamp = line.split("~,")[0]
                saved_timestamps.append(saved_timestamp)
    return saved_facts, saved_timestamps


def recover_saved_facts(_ip_address_):
    filename = './output/' + _ip_address_ + '.txt'
    community = ''
    connection = ''
    if os.path.isfile(filename):
        with open(filename) as file:
            line = file.readline()
        if '~' in line:
            community = line.split(',')[4]
            connection = line.split(',')[2]
    return community, connection


def save_to_file(_ip_address_, _facts_):
    filename = './output/' + _ip_address_ + '.txt'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
    saved_facts, saved_timestamps = get_saved_facts(_ip_address_)
    i = 0

    with open(filename, 'w') as f:
        i = 0
        for saved_fact in saved_facts:
            if saved_fact in _facts_:
                fact_to_write = ">" + saved_timestamps[i].replace(">", "") + "~," + saved_fact
                fact_to_write = fact_to_write.replace("\n", "") + "\n"
                f.write(fact_to_write)
            else:
                fact_to_write = saved_timestamps[i].replace(">", "") + "~," + saved_fact
                fact_to_write = fact_to_write.replace("\n", "") + "\n"
                f.write(fact_to_write)
            i += 1
        for fact in _facts_:
            if fact not in saved_facts:
                fact_to_write = ">" + timestamp + "~," + fact
                fact_to_write = fact_to_write.replace("\n", "") + "\n"
                f.write(fact_to_write)


def get_facts(_ip_address_):
    s = SnmpQuery(_ip_address_)
    s.get_connection()
    if s.get_hostname() != '-' and s.get_platform():
        s.get_mask()
        if not s.get_default_route():
            print('cannot get default route for ', _ip_address_)
            exit()
        fact = str(s.ip) + ',' \
            + str(s.connectivity) + ',' \
            + str(s.platform) + ',' \
            + str(s.hostname) + ',' \
            + str(s.default_route) + ','
        print(fact)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:f:', ['help', 'ip_address=', 'filename='])
    except getopt.GetoptError:
        print(f'-[i|f] [ip_address|filename]')
        sys.exit(2)
    ip_address = filename = None
    if len(opts) != 0:
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print(f'Usa -[i|f] [ip_address|filename]')
                sys.exit()
            elif opt in ('-i', "--ip_address"):
                ip_address = str(arg)
            elif opt in ('-f', "--filename"):
                filename = str(arg)
            else:
                print(f'Usa -[i|f] [ip_address|filename]')
                sys.exit(2)
    else:
        print(f'-[i|f] [ip_address|filename]')
    print('hostname,is_telnet,platform,host,current_dg,ip,new_dg,mask,site_code')
    if ip_address:
        get_facts(ip_address.strip())

    elif filename:
        f = open(filename)
        i = 0
        inventory = []
        processes = []

        for line in f:
            line = line.replace("\n", "")
            inventory.append(line)
            i += 1
        for host in inventory:
            proc = Process(target=get_facts, args=(host,))
            processes.append(proc)
            proc.start()
        for p in processes:
            p.join()
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
