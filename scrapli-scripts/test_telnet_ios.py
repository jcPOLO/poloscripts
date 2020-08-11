from scrapli.driver.core import IOSXEDriver
import getpass

username = input("Username: ")
password = getpass.getpass()
my_device = {
    "host": "1.43.5.235",
    "port": 23,
    "auth_username": username,
    "auth_password": password,
    "transport": "telnet",
    "auth_strict_key": False,
}

conn = IOSXEDriver(**my_device)
conn.open()
response = conn.send_command("show ver")
print(response.result)
