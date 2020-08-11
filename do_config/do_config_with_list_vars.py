from jinja2 import Template
import os
from typing import Set, Dict
import argparse


def load_template(file: str, d: Dict) -> str:
    path =  os.getcwd() or '/home/jcpolo/mis_codigos/'
    filename = f'{path}/{file}'

    with open(filename) as f:
        template = Template(f.read())
    r = template.render(d)
    return r


def get_args():
    parser = argparse.ArgumentParser(description='Process template...')
    parser.add_argument('jinja2_template')
    return parser.parse_args()


def main():

    vlan = {
        'tag': '',
        'description': '',
        'nameif': '',
        'ip_mask': '',
        'ip_stby': '',
    }
    vlans = []

    n_vlans = input('Cuantas vlans nuevas se van a crear?:')


    for vlan in range(int(n_vlans)):
        tag = input('Nueva vlan:')
        nameif = input('Nombre de la nueva interfaz del firewall:')
        description = input('Nombre o descripcion de la vlan, sin espacios ni cosas raras:')
        ip_mask = input('IP y mascara de la interfaz del firewall (ejemplo, 192.168.150.193 255.255.255.224):')
        ip_stby = input('IP de la standby (ejemplo, 192.168.150.194):')

        vlan = {
            'tag': tag,
            'description': description,
            'nameif': nameif,
            'ip_mask': ip_mask,
            'ip_stby': ip_stby,
        }
        vlans.append(vlan)

    context = input('Nombre del nuevo contexto:')
    failover_group = input('Numero del failover group (1 - pigna, 2 - Walqa):')
    password_comunicaciones = input('Password COMS:')

    dict_var = {
        'VLANS': vlans,
        'context': context,
        'failover_group': failover_group,
        'password_comunicaciones': password_comunicaciones
    }

    args = get_args()
    cfg = load_template(args.jinja2_template, dict_var)
    print(cfg)


if __name__ == '__main__':
    main()

