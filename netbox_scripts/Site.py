from typing import Optional
from slugify import slugify
import pynetbox


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
            'status': {'value': 'planned', 'label': 'Planned'},
            'region': {'id': '', 'url': '', 'name': '', 'slug': ''},
            'tenant': None,
            'facility': '',
            'description': self.description,
            'physical_address': self.physical_address,
            'contact_phone': self.contact_phone,
            'contact_email': self.contact_email,
            'comments': self.comments,
            'tags': []
        }

        site = nb.dcim.sites.create(data) # returns pynetbox.core.response.Record object
        return site

    def delete(self, nb):
        data = {'slug': self.slug}
        try:
            site = nb.dcim.sites.get(**data) # returns pynetbox.core.response.Record object
            r = site.delete() if site else "site not found"
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
            site = nb.dcim.regions.get(**query) # returns pynetbox.core.response.Record object
            r = site.update(kwargs) if site else "site not found"
        except pynetbox.core.query.RequestError as e:
            print(e)
        if r:
            return '{} updated.'.format(site)
        else:
            return '{} not updated.'.format(site)

    def get_or_create(self, nb):
        site = self.get(nb) 
        if site is None:
            site = self.create(nb)
            return '{} created.'.format(site)
        else:
            return '{} exists.'.format(site)
