def facts_for_customer_csv(result):
    for h in result.keys():
        facts = result[h][2]
        d_facts = facts.__dict__
        facts = d_facts['result']['facts']
        hostname = facts['hostname']
        os_version = facts['os_version']
        serial_number = facts['serial_number']
        model = facts['model']
        print("{};{};{};{};{}".format(h, hostname, os_version, serial_number, model))
