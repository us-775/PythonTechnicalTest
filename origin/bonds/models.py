import logging
from typing import Optional

from django.db import models
from django.db.models.fields import CharField, DateField, DecimalField
import requests


class Bond(models.Model):
    isin = CharField(max_length=12)
    size = DecimalField(max_digits=20, decimal_places=3)
    currency = CharField(max_length=3)
    maturity = DateField()
    lei = CharField(max_length=20)
    legal_name = CharField(max_length=128, blank=True, null=True)

    def __repr__(self):
        return f'Bond ({self.isin})'

    @classmethod
    def get_legal_name_from_gleif(cls, lei: str) -> Optional[str]:
        try:
            logging.info(f"Getting legal name for LEI {lei} from GLEIF's API")
            r = requests.get(f'https://leilookup.gleif.org/api/v2/leirecords?lei={lei}')
            r.raise_for_status()
            legal_name = r.json()[0]['Entity']['LegalName']['$']
        except Exception as ex:
            logging.exception(f'Could not fetch legal name of bond (LEI={lei}) from GLEIF API: {ex}')
            legal_name = None
        return legal_name
