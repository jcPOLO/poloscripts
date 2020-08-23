import csv
from typing import List, Dict, TextIO, Callable, Optional
from slugify import slugify
import pynetbox
from Region import Region
from Site import Site
import os


FILE = 'GESTION.csv'
NETBOX_URL = 'http://netbox.aragon.es'


class NetboxAPITokenNotFound(Exception):
    pass


def load_api():
    token = os.getenv('NETBOX_API_TOKEN')
    if token is None:
        raise NetboxAPITokenNotFound('NETBOX_API_TOKEN was not found in enviromental variables')
    return pynetbox.api(NETBOX_URL, token=token)


def create_region(row, regions):
    if row["POBLACIÓN"].title() not in regions:
        regions.append(row["POBLACIÓN"].title())
        name = row["POBLACIÓN"].title()
        parent = f"Provincia {row['PROVINCIA'].capitalize()}"

        region = Region(name=name, parent=parent)
        return region


def create_site(row, sites):
    if row["CODIGO INMUEBLE"] not in sites:
        sites.append(row["CODIGO INMUEBLE"])
        slug = f"{int(row['CODIGO INMUEBLE']):04d}"
        name = row["NOMBRE SEDE"]
        status = row['ESTADO']
        region = row["POBLACIÓN"].title()
        description = row['ACTIVIDAD']
        physical_address = row['DIRECCIÓN SEDE']
        # contact_name = row['']
        contact_phone = row['TELÉFONO FIJO']
        # contact_email = row['']
        comments = row['TELÉFONO MÓVIL']
        
        
        site = Site(name=name, slug=slug)
        return site


def create_entity(entity: str, row, wrapper) -> Callable:
    if entity == 'region':
        return create_region(row, wrapper)
    if entity == 'site':
        return create_site(row, wrapper)


# Return a List of entity objects
def read_csv(entity_name: str, file: TextIO) -> List:

    wrapper = []
    r = []

    with open(file) as f:
        data = csv.DictReader(f, delimiter=';')
        print(data)

        for row in data:
            entity = create_entity(entity_name, row, wrapper)
            if entity:
                r.append(entity)
                
    return r


def main():
    errors = []
    nb = load_api()
    # regions = read_csv('region', FILE)
    sites = read_csv('site', FILE)
    print(sites[0].slug)
    exit()

    for region in regions:
        try:
            r = nb.dcim.regions.create(name=region.name, slug=region.slug, parent={'name':region.parent})
            # region_o = nb.dcim.regions.get(name=region.name)
            # r = region_o.delete()
            print(f'SUCCESS --- {region.name},{region.slug},{region.parent}.....................{r}..')
        except Exception:
            errors.append(region.name)
            print(f'Error !!!!! {region.name},{region.slug},{region.parent}...')
            pass
    print("ERRORS {}".format(errors))


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
