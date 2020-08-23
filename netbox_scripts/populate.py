import pandas as pd
from typing import List, Dict, TextIO, Callable, Optional
from slugify import slugify
import pynetbox
from Region import Region
from Site import Site
import os


FILE = 'GESTION.xlsx'
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
    
    name = dataf['NOMBRE SEDE']
    slug = dataf['CODIGO INMUEBLE']
    status = dataf['ESTADO']
    region = dataf['POBLACIÓN'].title()
    description = dataf['ACTIVIDAD']
    physical_address = dataf['DIRECCIÓN SEDE']
    # contact_name = dataf['']
    contact_phone = dataf['TELÉFONO FIJO']
    # contact_email = dataf['']
    comments = dataf['TELÉFONO MÓVIL']

    sites = [
        Site(
            name=str(name),
            slug=f"{int(slug):04d}",
            region={'slug': str(region)},
            #region=nb.dcim.regions.get(slug=region),
            physical_address=str(physical_address)
        ) for name,slug,region,physical_address in zip(
            name,slug,region,physical_address)
    ]

    return sites


def create_entity(entity: str, dataf) -> Callable:
    if entity == 'region':
        return create_region(dataf)
    if entity == 'site':
        return create_site(dataf)


# Return a List of entity objects
def get_data(entity_name: str, file: TextIO) -> List:
    data = pd.read_excel(file,'Sedes')
    entity = create_entity(entity_name, data)
    return entity

def main():
    nb = load_api()

    regions = get_data('region', FILE)
    # sites = get_data('site', FILE)

    for r in regions:
        if r.slug == 'abiego':
            region = r
            break

    r = region.delete(nb)
    r = region.get_or_create(nb)
    r = region.update(nb, description='anchoas')
    print(r)
    exit()

    try:
        r = nb.dcim.sites.create(site)

    except pynetbox.core.query.RequestError as e:
        print(e)
    
    exit()



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
