import datetime as dt

from django.urls import reverse
from rest_framework.test import APITestCase, APISimpleTestCase

from .models import Bond


class HelloWorld(APISimpleTestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200


class Bonds(APITestCase):
    def setUp(self):
        # Create two bonds as test data
        Bond.objects.create(
            isin='FR0000131104',
            size=100_000_000,
            currency='EUR',
            maturity=dt.date(2025, 2, 28),
            lei='R0MUWSFPU8MPRO8K5P83',
            legal_name='BNP PARIBAS'
        )

        Bond.objects.create(
            isin='GB0000278371',
            size=123.93,
            currency='GBP',
            maturity=dt.date(2035, 6, 1),
            lei='2138006E3GTWJ8K3AN43',
            legal_name='BARCLAYS WEALTH INVESTMENT FUNDS (UK) - BARCLAYS WEALTH GLOBAL MARKETS 3'
        )

    def test_get_all(self):
        resp = self.client.get(reverse('bonds'))
        assert resp.status_code == 200
        assert len(resp.data) == 2
        assert resp.data[0] == {
            'id': 1,
            'isin': 'FR0000131104',
            'size': '100000000.000',
            'currency': 'EUR',
            'maturity': '2025-02-28',
            'lei': 'R0MUWSFPU8MPRO8K5P83',
            'legal_name': 'BNP PARIBAS'
        }

        assert resp.data[1] == {
            'id': 2,
            'isin': 'GB0000278371',
            'size': '123.930',
            'currency': 'GBP',
            'maturity': '2035-06-01',
            'lei': '2138006E3GTWJ8K3AN43',
            'legal_name': 'BARCLAYS WEALTH INVESTMENT FUNDS (UK) - BARCLAYS WEALTH GLOBAL MARKETS 3'
        }

    def test_filter_with_results(self):
        resp = self.client.get(reverse('bonds'), {'legal_name': 'barclays'})
        assert resp.status_code == 200
        assert len(resp.data) == 1
        assert resp.data[0] == {
            'id': 2,
            'isin': 'GB0000278371',
            'size': '123.930',
            'currency': 'GBP',
            'maturity': '2035-06-01',
            'lei': '2138006E3GTWJ8K3AN43',
            'legal_name': 'BARCLAYS WEALTH INVESTMENT FUNDS (UK) - BARCLAYS WEALTH GLOBAL MARKETS 3'
        }

    def test_filter_without_results(self):
        resp = self.client.get(reverse('bonds'), {'legal_name': 'HSBC'})
        assert resp.status_code == 200
        assert len(resp.data) == 0

    def test_add_bond(self):
        # Add bond
        new_bond_resp = self.client.post(reverse('bonds'), {
            "isin": "IE0000928234",
            "size": 950.0,
            "currency": "EUR",
            "maturity": "2040-01-14",
            "lei": "213800MLLL9HCSPKOV56"
        })
        assert new_bond_resp.status_code == 201

        # There should be one more bond
        get_resp = self.client.get(reverse('bonds'))
        assert get_resp.status_code == 200
        assert len(get_resp.data) == 3

    def test_add_bond_isin_too_long(self):
        # ISIN should be 12 chars,
        new_bond_resp = self.client.post(reverse('bonds'), {
            "isin": "IE000092823434",
            "size": 950.0,
            "currency": "EUR",
            "maturity": "2040-01-14",
            "lei": "213800MLLL9HCSPKOV56"
        })
        assert new_bond_resp.status_code == 400

        # No new bond added
        get_resp = self.client.get(reverse('bonds'))
        assert get_resp.status_code == 200
        assert len(get_resp.data) == 2
