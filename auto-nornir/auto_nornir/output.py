# TODO: This is not optimal.
def facts_for_customer_csv(result):
    for h in result.keys():
        #facts = result[h][2]
        for task_result in result[h]:
            if 'FACT' in task_result.name:
                r = task_result.result
                facts = r['facts']
                hostname = facts['hostname']
                os_version = facts['os_version']
                serial_number = facts['serial_number']
                model = facts['model']
                print("{};{};{};{};{}".format(h, hostname, os_version, serial_number, model))
