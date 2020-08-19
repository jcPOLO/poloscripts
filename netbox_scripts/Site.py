from typing import Optional
from slugify import slugify


class Site:
    def __init__(self, name):
        self.name = name
        self.slug = slugify(name)
        self.status = status
        self.region = region
        self.facility = facility
        self.description = description
        self.physical_address = physical_address
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.comments = comments

    

