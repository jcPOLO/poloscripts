import pandas as pd
from typing import List, Dict, TextIO, Callable, Optional
from slugify import slugify
import pynetbox
from Region import Region
from Site import Site
import os


FILE = "C:\\Users\\Polo\\Documents\\CURRO\\repo\\INVENTARIOS\\GESTION.xlsx"
NETBOX_URL = 'http://netbox.aragon.es'


class NetboxAPITokenNotFound(Exception):
    pass


def load_api():
    token = os.getenv('NETBOX_API_TOKEN')
    if token is None:
        raise NetboxAPITokenNotFound('NETBOX_API_TOKEN was not found in enviromental variables')
    return pynetbox.api(NETBOX_URL, token=token)


def create_region(dataf):
    name = dataf['POBLACIÓN'].str.title()
    parent = 'Provincia ' + dataf['PROVINCIA'].astype(str).str.capitalize()

    regions = [
        Region(
            name=str(name),
            parent=str(parent)
        ) for name,parent in zip(name, parent)
    ]
    return regions


def create_site(dataf):
    '''
    ESTADO no 'BAJA'
    SEDE no '0'
    DIRECCIÓN SEDE no "0" ni "vacía"
    POBLACIÓN no "vacía"
    PROVINCIA "zaragoza" o "huesca" o "teruel"
    ACTIVIDAD no "vacía"
    CARPETA no "vacía"
    '''

    name = dataf['NOMBRE SEDE']
    slug = dataf['CODIGO INMUEBLE']
    # status = dataf['ESTADO']
    region = dataf['POBLACIÓN'].str.title()
    description = dataf['NOMBRE SEDE']
    # description = dataf['ACTIVIDAD']
    physical_address = dataf['DIRECCIÓN SEDE']
    facility = dataf['CODIGO HOSTNAME']
    # contact_name = dataf['']
    # contact_phone = dataf['TELÉFONO FIJO']
    # contact_email = dataf['']
    # comments = ', '.join([dataf['TELÉFONO MÓVIL'], dataf['TELÉFONO FIJO']])
    cf_criticidad_servicio = dataf['CRITICIDAD SERVICIO']
    cf_disponibilidad = dataf['DISP.']


    sites = [
        Site(
            name=str(name),
            slug=str(slug),
            region={'slug': str(region)},
            physical_address=str(physical_address),
            description=str(description),
            facility=str(facility)
        ) for name,slug,region,physical_address,description,facility in zip(
            name,slug,region,physical_address, description,facility)
    ]

    return sites


def create_entity(entity: str, dataf) -> Callable:
    if entity == 'region':
        return create_region(dataf)
    if entity == 'site':
        return create_site(dataf)


# Return a List of entity objects
def get_data(file: TextIO) -> List:
    df = pd.read_excel(file,'Sedes')
    searchfor = ['zaragoza', 'huesca', 'teruel']
    df = df[df.PROVINCIA.notnull()]
    df = df[df['PROVINCIA'].notna()]
    df = df[df.PROVINCIA.str.lower().str.contains('|'.join(searchfor))]
    df = df[df['CARPETA'].notna()]
    df = df[df['CARPETA'].notnull()]

    return df


def dump_entity(nb, entity: str):
    errors = []
    failed_entities = []
    data = get_data(FILE)

    entities = create_entity(entity, data)

    try:
        created = []
        for ent in entities:
            if ent.slug not in created:
                r = ent.get_or_create(nb)
                created.append(ent.slug)
                print(r)
            else:
                print(f'{ent.name} already created....')
    except pynetbox.core.query.RequestError as e:
        errors.append(e)
        failed_entities.append(ent.name)
        pass

    # r = ent.get_or_create(nb)
    # r = ent.delete(nb)
    # r = ent.update(nb, description='')

    print("errors: {}".format(errors))
    print("failed entities: {}".format(failed_entities))


def main():
    nb = load_api()
    dump_entity(nb, 'site')
    # dump_regions(nb)
    # dump_sites(nb)


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
