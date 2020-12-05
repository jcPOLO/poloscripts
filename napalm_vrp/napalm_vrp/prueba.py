from napalm import get_network_driver
import getpass

# username = input("Username: ")
password = getpass.getpass()
driver = get_network_driver("vrp")

device = driver(
  hostname='192.168.63.152',
  username='jcpolo',
  password=password,
  optional_args = {'port': 22}
  )

device.open()
facts = device.get_facts()
print(facts)
print('y ahora lo otro')
ips = device.get_interfaces_ip()
print(ips)
device.close()

