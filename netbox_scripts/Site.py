from typing import Optional
from slugify import slugify


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
        self.contact_email = contact_email
        self.comments = comments

    

