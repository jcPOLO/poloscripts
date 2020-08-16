from typing import Optional
from slugify import slugify


class Region(object):

    def __init__(
        self,
        name: str,
        slug: str = None,
        parent: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        self.__name = name
        self.slug = slug or slugify(name) 
        self.parent = parent
        self.description = description
    
    
    def __str__(self):
        return "{} is a {}".format(self.__name, type(self).__name__)

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if name:
            self.__name = name


