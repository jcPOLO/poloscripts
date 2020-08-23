from typing import Optional, List, Dict
from slugify import slugify
import pynetbox


class Region(object):

    def __init__(
        self,
        name: str,
        slug: str = None,
        parent: Optional[str] = None,
        description: Optional[str] = None,
        nb = None
    ) -> None:
        self.__name = name
        self.slug = slug or slugify(name) 
        self.parent = parent
        self.description = description
        self.nb = nb
    
    
    def __str__(self):
        return "{} is a {}".format(self.__name, type(self).__name__)
    
    def get(self, nb):
        data = {'name': self.name, 'slug': self.slug}
        try:
            region = nb.dcim.regions.get(**data) # returns pynetbox.core.response.Record object
            import ipdb; ipdb.set_trace()
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
        import ipdb; ipdb.set_trace()
        return region

    def delete(self, nb):
        data = {'name': self.name, 'slug': self.slug}
        try:
            region = nb.dcim.regions.get(**data) # returns pynetbox.core.response.Record object
            r = region.delete() if region else "Region not found"
        except pynetbox.core.query.RequestError as e:
            print(e)
        return r

    def update(self, nb, **kwargs):
        query = {'name': self.name, 'slug': self.slug}
        data = {
            'name': self.name or kwargs['name'],
            'slug': self.slug or kwargs['slug'],
            'parent':{
                'name': self.parent or kwargs['description']
            },
            'description': self.description or kwargs['description']
        }
        try:
            region = nb.dcim.regions.get(**query) # returns pynetbox.core.response.Record object
            r = region.update(**data) if region else "Region not found"
        except pynetbox.core.query.RequestError as e:
            print(e)
        return r

    def get_or_create(self, nb):
        region = self.get(nb) 
        if region is None:
            region = self.create(nb)
            return '{} created.'.format(region)
        else:
            return '{} exists.'.format(region)


    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if name:
            self.__name = name



