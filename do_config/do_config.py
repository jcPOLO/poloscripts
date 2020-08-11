from jinja2 import Template, Environment, meta
import os
from typing import Set
import argparse



def get_variables(file: str) -> Set:
    path =  os.getcwd()
    filename = f'{path}/{file}'
    with open(filename) as f:
        template = f.read()
    env = Environment()
    ast = env.parse(template)
    r = meta.find_undeclared_variables(ast)
    return r


def load_template(file: str, d) -> str:
    path =  os.getcwd()
    filename = f'{path}/{file}'

    with open(filename) as f:
        template = Template(f.read())
    r = template.render(d)
    return r


def main() -> None:
    parser = argparse.ArgumentParser(description='Process template...')
    parser.add_argument('jinja2_template')
    args = parser.parse_args()
    var_d = get_variables(args.jinja2_template)
    r = {}
    for n in var_d:
        r[n] = input(f'{n}: ')

    cfg = load_template(args.jinja2_template, r)
    with open('config.txt', 'w') as f:
        f.write(cfg)
    print(cfg)


if __name__ == '__main__':
    main()

