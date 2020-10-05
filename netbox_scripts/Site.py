from typing import Optional, Dict
from slugify import slugify
import pynetbox
import re
from Region import Region

class Site:
    def __init__(
        self, 
        name: str,
        slug: str,
        status: Optional[str] = None,
        region: Dict[str, str] = None,
        facility: Optional = None,
        description: Optional[str] = None,
        physical_address: Optional[str] = None,
        contact_name: Optional[str] = None,
        contact_phone: Optional[str] = None,
        contact_email: Optional[str] = None,
        comments: Optional[str] = None,
        nb = None
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
        self.nb = nb

    def get(self, nb):
        data = {'name': self.name, 'slug': self.slug}
        try:
            site = nb.dcim.sites.get(**data) # returns pynetbox.core.response.Record object
        except pynetbox.core.query.RequestError as e:
            print(e)
        return site

    def create(self, nb):
        data = {
            'name': self.name,
            'slug': self.slug,
            'status': 'planned',
            'region': nb.dcim.regions.get(name=self.region).id,
            'tenant': None,
            'facility': self.facility,
            'description': self.description or '',
            'physical_address': self.physical_address,
            'contact_phone': self.contact_phone or '',
            'contact_email': self.contact_email or '',
            'comments': self.comments or '',
            'tags': []
        }
        #import ipdb; ipdb.set_trace()

        try:
            site = nb.dcim.sites.create(data) # returns pynetbox.core.response.Record object
        except pynetbox.core.query.RequestError as e:
            site = nb.dcim.sites.get(slug=self.slug)
            try:
                site = site.update(data)
            except pynetbox.core.query.RequestError as e:
                print(e)
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


    @property
    def name(self):
        return self.__name
    
    @property
    def region(self):
        return self.__region

    @property
    def slug(self):
        return self.__slug

    @region.setter
    def region(self, value):
        if value and isinstance(value, dict):
            value['slug'] = re.sub(' +', ' ', value['slug']).strip().title()
            if len(value['slug']) > 50:
                value['slug'] = input(f"name is larger than 50 -{value['slug']}- . Enter new name:")
            self.__region = value['slug']

    @slug.setter
    def slug(self, value):
        if value and isinstance(value, str):
            value = f"{int(value):04d}"
            self.__slug = value

    @name.setter
    def name(self, value):
        if value and isinstance(value, str):
            # if 'e.o.e.p' in value.lower():
            #     value = 'EOEP'
            # elif 'transformacion agraria' in value.lower():
            #     value = 'CTA'
            # elif 'investigacion y tecnologia' in value.lower():
            #     value = 'CITA'
            # elif 'c.p.e.p.a' in value.lower():
            #     value = 'CPEPA'
            # elif 'a.c.e.p.a' in value.lower():
            #     value = 'ACEPA'
            # elif 'c.p.r' in value.lower():
            #     value = 'CPR'
            # elif 'e.a.t' in value.lower():
            #     value = 'EAT'
            # elif 'c.e.i.p' in value.lower():
            #     value = value.split('-')[0]
            # elif 'servicio provincial de educacion' in value.lower():
            #     value = 'Servicio Provincial de Educación'
            # elif 'e.o.i' in value.lower():
            #     value = 'EOI'
            # elif 'e.a.i.p.m' in value.lower():
            #     value = 'EAIPM'
            # elif 'c.r.a' in value.lower():
            #     value = 'CRA'
            # elif 'almacen robados' in value.lower():
            #     value = 'Almacén Robados Servicio Provincial'
            # elif 'el frago' in value.lower():
            #     value = 'CTRT El Frago'
            # elif 'aula dei' in value.lower():
            #     value = 'Aula Dei'
            # elif 'cadza' in value.lower():
            #     value = 'CADZA'
            # elif '(juslibol)' in value.lower():
            #     value = 'Centro de Menores San Jorge-Juslibol'
            # elif 'c.a.m.p' in value.lower():
            #     value = 'CAMP'
            # elif 'oca de valderrobres' in value.lower():
            #     value = 'OCA de Valderrobres'
            # elif 'campus universidad zaragoza (san francisco)' in value.lower():
            #     value = 'Campus Universidad San Francisco'
            # elif 'escuela universitaria politecnica de la' in value.lower():
            #     value = 'EUPLA'
            # elif 'i.a.s.s' in value.lower() and 'direccion provincial' in value.lower():
            #     value = 'IASS Dirección Provincial'
            # elif 'casa de federaciones deportivas' in value.lower():
            #     value = 'Federaciones Deportivas Aragonesas'
            # elif 'jose peris lacasa' in value.lower():
            #     value = 'CM Jose Peris Lacasa - Conservatorio'
            # elif 'carei' in value.lower():
            #     value = 'CAREI'
            # elif 'catedu' in value.lower():
            #     value = 'CATEDU'
            # elif 'servicio de atencion educativa d' in value.lower():
            #     value = 'Serv. Atención Educativa Domiciliaria'
            # elif 'i.f.p.e.' in value.lower():
            #     value = 'IFPE Escuela Superior de Hostelería de Aragón'

            value = re.sub(' +', ' ', value).strip()
            
            while len(value) > 46:
                value = value.rsplit(' ', 1)[0]
                if len(value) > 46:
                    value = input(f'name is larger than 50 -{value}- . Enter new name:')
            self.__name = value
