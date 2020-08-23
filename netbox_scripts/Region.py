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
    
    def get(self):
        data = {'name': self.name, 'slug': self.slug}
        region = self.nb.dcim.regions.get(data)
        return region

    def create(self):
        data = {
            'name': self.name,
            'slug': self.slug,
            'parent':{
                'name': self.parent
            },
            'description': self.description
        }
        region = self.nb.dcim.regions.create(data)
        return region


    def get_or_create(self):
        region = self.get() 
        if region is None:
            region = self.create()
            return region
        else:
            return region


    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if name:
            self.__name = name



