from typing import Optional
from slugify import slugify


'''
{'id': 3842,
 'name': 'Hospital Clinico Universitario',
 'slug': '0515',
 'status': {'value': 'staging', 'label': 'Staging'},
 'region': {'id': 2844,
  'url': 'http://netbox.aragon.es/api/dcim/regions/2844/',
  'name': 'Zaragoza',
  'slug': 'zaragoza'},
 'tenant': None,
 'facility': '',
 'asn': None,
 'time_zone': None,
 'description': '',
 'physical_address': 'Avda. San Juan Bosco  15',
 'shipping_address': '',
 'latitude': None,
 'longitude': None,
 'contact_name': '',
 'contact_phone': '976556400',
 'contact_email': '',
 'comments': '',
 'tags': [],
 'custom_fields': {},
 'created': '2020-08-13',
 'last_updated': '2020-08-23T18:53:48.267205+02:00',
 'circuit_count': None,
 'device_count': None,
 'prefix_count': None,
 'rack_count': None,
 'virtualmachine_count': None,
 'vlan_count': None}
 '''

class Site:
    def __init__(
        self, 
        name: str,
        slug: str,
        status: Optional[str] = None,
        region: str = None,
        facility: Optional = None,
        description: Optional[str] = None,
        physical_address: Optional[str] = None,
        contact_name: Optional[str] = None,
        contact_phone: Optional[str] = None,
        contact_email: Optional[str] = None,
        comments: Optional[str] = None
    ):
        self.name = name
        self.slug = slug
        self.status = status
        self.region = region
        self.facility = facility
        self.description = description
        self.physical_address = physical_address
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.comments = comments

    
    def get(self, nb):
        data = {'name': self.name, 'slug': self.slug}
        try:
            region = nb.dcim.regions.get(**data) # returns pynetbox.core.response.Record object
        except pynetbox.core.query.RequestError as e:
            print(e)
        return region

    def create(self, nb):
        data = {
            'name': self.name,
            'slug': self.slug,
            'parent':{
                'name': self.parent
            },
            'description': self.description or ''
        }
        region = nb.dcim.regions.create(data) # returns pynetbox.core.response.Record object
        return region

    def delete(self, nb):
        data = {'name': self.name, 'slug': self.slug}
        try:
            region = nb.dcim.regions.get(**data) # returns pynetbox.core.response.Record object
            r = region.delete() if region else "Region not found"
        except pynetbox.core.query.RequestError as e:
            print(e)
        return r

    # TODO: Don't work if you delete a field (send as update ''), 
    # it updates but it prints "not updated"
    # Need to check if there is a difference between first object and
    # updated object to know if it is updated.
    def update(self, nb, **kwargs):
        query = {'name': self.name, 'slug': self.slug}
        try:
            region = nb.dcim.regions.get(**query) # returns pynetbox.core.response.Record object
            r = region.update(kwargs) if region else "Region not found"
        except pynetbox.core.query.RequestError as e:
            print(e)
        if r:
            return '{} updated.'.format(region)
        else:
            return '{} not updated.'.format(region)

    def get_or_create(self, nb):
        region = self.get(nb) 
        if region is None:
            region = self.create(nb)
            return '{} created.'.format(region)
        else:
            return '{} exists.'.format(region)
