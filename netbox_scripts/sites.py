import csv
from typing import List, Dict, TextIO, Callable, Optional
from slugify import slugify
import pynetbox
from Region import Region


def load_api():
    return pynetbox.api(
        'http://netbox.aragon.es',
        token='65fa3de4a2de953dca49e88ffdb5a1daebfcc4c7'
    )

FILE = 'GESTION.csv'


def create_region(row, regions):
    if row["POBLACIÓN"].title() not in regions:
        regions.append(row["POBLACIÓN"].title())
        name = row["POBLACIÓN"].title()
        parent = f"Provincia {row['PROVINCIA'].capitalize()}"
        region = Region(name=name, parent=parent)
        return region


def create_site(row, sites):
    if int(row["codinm"]) not int sites:
        sites.append(row[""])


def create_entity(entity: str, row, wrapper) -> Callable:
    if entity == 'region':
        return create_region(row, wrapper)


# Return a List of entity objects
def read_csv(entity_name: str, file: TextIO) -> List[Object]:

    wrapper = []
    r = []

    with open(file) as f:
        data = csv.DictReader(f, delimiter=';')
        print(data.fieldnames)

        for row in data:
            entity = create_entity(entity_name, row, wrapper)
            if entity:
                r.append(entity)
                
    return r


def main():
    errors = []
    nb = load_api()
    regions = read_csv('region', FILE)

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
