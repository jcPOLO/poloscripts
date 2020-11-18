import datetime
import getopt
import re
import socket
import sys
import os
from multiprocessing import Process

from pysnmp.hlapi import *

class SnmpQuery(object):

    def __init__(self, ip, timeout=1):
    
        self.ip = ip
        self.community = ''
        self.timeout = timeout
        self.hostname = ''
        self.connectivity = ''
        self.location = ''
        self.platform = ''
        self.devices = []

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

    def get_hostname(self, _community):
        communities = [
            'C0mun1c4c10n3s',
            'salud145_RO',
            'toip145ro',
            'OY42E7l57NZF.QW9',
            'NRjud1c1al',
            'toip145ro',
            'srnumrpal',
            'sunrmbpana',
            'publics'
        ]

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
            if _community:
                self.community = _community
            else:
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
            self.location = '-'
            self.community = '-'
            self.hostname = '-'
            self.connectivity = '-'
            self.platform = '-'
            self.devices = [{'entity': '-', 'model': '-', 'serial': '-'}]
        self.hostname = self.strfilter(self.hostname)

    def get_location(self):
        if self.location == '':
            temp = self.get_oid('1.3.6.1.2.1.1.6.0')
            if temp == "SNMP_error":
                self.location = ""
            else:
                self.location = re.search(r"0 (.*)", temp).group(1)
        self.location = self.strfilter(self.location)

    def get_connection(self, _connection):
        self.connectivity = _connection
        if self.connectivity == '':
            ports = {"t": 23, "s": 22, "w": 80, "+": 443}
            # ports = {"t": 23, "s": 22}
            for port, value in ports.items():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.0)
                result = s.connect_ex((self.ip, int(value)))
                if result == 0:
                    self.connectivity = self.connectivity + str(port)
                s.close()

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

    def get_devices(self):
        if not self.devices:
            serial = ''
            model = ''
            mpls = False
            default_pattern = ['ios', 'asa', 'nxos', 'alcatel', 'hp', 'huawei']
            if self.platform == "panos":
                model = self.get_oid('1.3.6.1.4.1.25461.2.1.2.2.1.0')
                model = model.split(".0")[1]
                serial = self.get_oid('1.3.6.1.4.1.25461.2.1.2.1.3.0')
                serial = serial.split(".0")[1]
                entity = "device"
                model = self.strfilter(model)
                serial = self.strfilter(serial)
                device = {"entity": entity, "model": model, "serial": serial}
                self.devices.append(device)
            if self.platform == "junos":
                model = self.get_oid('1.3.6.1.2.1.1.1.0')
                model = model.split(".0")[1]
                model = model.split(",")[3]
                serial = "-"
                entity = "device"
                model = self.strfilter(model)
                serial = self.strfilter(serial)
                device = {"entity": entity, "model": model, "serial": serial}
                self.devices.append(device)
            if self.platform == "ucs":
                raw_model = self.get_oid('1.3.6.1.4.1.9.9.719.1.9.6.1.6.1')
                model = raw_model.split(".719.1.9.6.1.6.1")[1]
                raw_serial = self.get_oid('1.3.6.1.4.1.9.9.719.1.9.6.1.14.1')
                serial = raw_serial.split(".719.1.9.6.1.14.1")[1]
                entity = "device"
                model = self.strfilter(model)
                serial = self.strfilter(serial)
                device = {"entity": entity, "model": model, "serial": serial}
                self.devices.append(device)
            if self.platform == "vmware":
                raw_model = self.get_oid('1.3.6.1.2.1.47.1.1.1.1.13.1')
                model = raw_model.split(".47.1.1.1.1.13.1")[1]
                raw_serial = self.get_oid('1.3.6.1.2.1.47.1.1.1.1.11.1')
                serial = raw_serial.split(".47.1.1.1.1.11.1")[1]
                entity = "device"
                model = self.strfilter(model)
                serial = self.strfilter(serial)
                device = {"entity": entity, "model": model, "serial": serial}
                self.devices.append(device)
            if self.platform == "f5":
                raw_model = self.get_oid('1.3.6.1.2.1.1.1.0')
                parse_model = raw_model.replace("\r\n", " ")
                parse_model = parse_model.split(".0")[1]
                model = parse_model.split(": Linux")[0]
                raw_serial = self.get_oid('1.3.6.1.4.1.3375.2.1.3.3.3.0')
                serial = raw_serial.split(".0")[1]
                entity = "device"
                model = self.strfilter(model)
                serial = self.strfilter(serial)
                device = {"entity": entity, "model": model, "serial": serial}
                self.devices.append(device)
            if self.platform == 'huawei':
                raw_model = self.get_oid('1.3.6.1.2.1.1.1.0')
                parse_model = raw_model.replace("\r\n", " ")
                parse_model = parse_model.split(".0")[1]
                model = parse_model.split("Huawei Versatile")[0]
                model = model.replace(" ", "")
                if model == '':
                    model = parse_model.split("HUAWEI ")[1]
                    mpls = True
                temp = self.snmpwalk_oid('1.3.6.1.2.1.47.1.1.1.1.2')
                k = 0
                for i in temp:
                    if not mpls and i['value'] == 'MPU Board':
                        _serial = self.get_oid('1.3.6.1.2.1.47.1.1.1.1.11.' + i['index'])
                        if _serial == "SNMP_error":
                            serial = ""
                        else:
                            serial = _serial.split(" ", 1)[1]
                    elif mpls:
                        if k == 0:
                            _serial = self.get_oid('1.3.6.1.2.1.47.1.1.1.1.11.' + i['index'])
                            if _serial == "SNMP_error":
                                serial = ""
                            else:
                                serial = _serial.split(" ", 1)[1]
                    k += 1
                entity = "device"
                model = self.strfilter(model)
                serial = self.strfilter(serial)
                device = {"entity": entity, "model": model, "serial": serial}
                self.devices.append(device)
            if self.platform == 'teldat':
                _model = ''
                raw_model = self.get_oid('1.3.6.1.2.1.1.1.0')
                _device = raw_model.split("model ")[1]
                model = _device.split(" S/N: ")[0]
                _serial = _device.split(" S/N: ")[1]
                serial = _serial.split('Teldat')[0]
                entity = 'device'
                model = self.strfilter(model)
                serial = self.strfilter(serial)
                device = {"entity": entity, "model": model, "serial": serial}
                self.devices.append(device)
            if self.platform in default_pattern:
                temp = self.snmpwalk_oid('1.3.6.1.2.1.47.1.1.1.1.2')
                for i in temp:  # iteramos cada oid de la lista de oids
                    _serial = self.get_oid('1.3.6.1.2.1.47.1.1.1.1.11.' + i['index'])
                    serial = _serial.split(" ", 1)[1]
                    serial = self.strfilter(serial)
                    if serial:
                        entity = i['value']
                        _model = self.get_oid('1.3.6.1.2.1.47.1.1.1.1.13.' + i['index'])
                        model = _model.split(" ", 1)[1]
                        entity = self.strfilter(entity)
                        model = self.strfilter(model)
                        if len(self.devices) == 0:
                            device = {"entity": entity, "model": model, "serial": serial}
                            self.devices.append(device)
                        else:
                            new_serial = 1
                            for device in self.devices:
                                if serial in device['serial']:
                                    new_serial = new_serial * 0
                            if new_serial == 1:
                                device = {"entity": entity, "model": model, "serial": serial}
                                self.devices.append(device)
        if len(self.devices) == 0:
            entity = 'unknown'
            serial = 'unknown'
            model = 'unknown'
            device = {"entity": entity, "model": model, "serial": serial}
            self.devices.append(device)

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


def get_role(_entity_, _model_):
    role = ''
    role_found = False
    if _model_ == "":
        _model_ = _entity_
    if _entity_ == "device":
        role = 'parent'
    elif _model_+'\n' in PARENTS:
        role = 'parent'
    else:
        if not role_found:
            entity_role = _entity_ + _model_
            for model in MODELS:
                model = model.split(';')
                if entity_role.find(model[0]) != -1 and not role_found:
                    role = model[1]
                    role_found = True
        if not role_found:
            role = 'role not choosen'
        role = role.replace('\n', '')
    return role


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
    community, connection = recover_saved_facts(_ip_address_)
    s.get_connection(connection)
    if s.get_hostname(community) != '-':
        #s.get_location()
        s.get_platform()
        #s.get_devices()
        facts = []
        for device in s.devices:
            fact = str(s.ip) + ',' \
                    + str(s.connectivity) + ',' \
                    + str(s.platform) + ',' \
                    + str(s.community) + ',' \
                    + str(s.hostname) + ',' \
                    + str(s.location)
            entity = str(device.get('entity'))
            model = str(device.get('model'))
            serial = str(device.get('serial'))
            role = get_role(entity, model)
            fact = fact + ',' + entity + ',' + model + ',' + serial + ',' + role
            fact = fact.replace('\n', '')
            facts.append(fact)
        save_to_file(s.ip, facts)
        return facts


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
    if ip_address:
        facts = get_facts(ip_address.strip())
        print(facts)
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
    # Python program to show time by perf_counter()
    from time import perf_counter

    # Start the stopwatch / counter
    t1_start = perf_counter()

    dirname = os.path.dirname(__file__)

    with open(os.path.join(dirname, 'entities.csv')) as file:
        ENTITIES = file.readlines()

    with open(os.path.join(dirname, 'models.csv')) as file:
        MODELS = file.readlines()

    with open(os.path.join(dirname, 'parents.txt')) as file:
        PARENTS = file.readlines()

    main()

    t1_stop = perf_counter()
    elapsed_time = t1_stop - t1_start
    print()
    print("Elapsed time during the whole program in seconds:",
          '{0:.2f}'.format(elapsed_time))
    print()
