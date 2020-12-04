from napalm import get_network_driver
import getpass  

username = input("Username: ")
password = getpass.getpass()
driver = get_network_driver("vrp")

device = driver(
  hostname='192.168.206.163', 
  username=username, 
  password=password, 
  optional_args = {'port': 22}
  )

device.open()
facts = device.get_facts()
print(facts)
device.close()

