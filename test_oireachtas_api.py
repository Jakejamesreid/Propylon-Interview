#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from unittest.mock import Mock, patch
import datetime
import os
import sys
import requests

# Local imports
from oireachtas_api import MEMBERS_ENDPOINT, LEGISLATION_ENDPOINT
from oireachtas_api import (
    get_endpoint_data,
    filter_bills_sponsored_by,
    filter_bills_by_last_updated
)


class TestAPI(unittest.TestCase):

    def test_legislation_api_response_status(self):

        # Send a request to the API server and conform that the response is okay
        response = requests.get(
            LEGISLATION_ENDPOINT+'?bill_status=Current,Withdrawn,Enacted,Rejected,Defeated,Lapsed')
        self.assertTrue(response.ok)

    def test_members_api_response_status(self):

        # Send a request to the API server and conform that the response is okay
        response = requests.get(MEMBERS_ENDPOINT)
        self.assertTrue(response.ok)


class TestGetEndpointData(unittest.TestCase):

    def test_get_endpoint_data_legislation_response(self):

        # If the request is sent successfully, then a response should be returned.
        response = get_endpoint_data(LEGISLATION_ENDPOINT)
        self.assertIsNotNone(response)

    def test_get_endpoint_data_members_response(self):

        # If the request is sent successfully, then a response should be returned.
        response = get_endpoint_data(MEMBERS_ENDPOINT)
        self.assertIsNotNone(response)


class TestFilterBillsSponsoredBy(unittest.TestCase):

    def test_filter_bills_sponsored_by_response(self):
        # If the request is sent successfully, then a response should be returned.
        results = filter_bills_sponsored_by('IvanaBacik')
        self.assertGreaterEqual(len(results), 0)


class TestFilterBillByLastUpdated(unittest.TestCase):

    def test_filter_bills_by_last_updated(self):

        # If the request is sent successfully, then a response should be returned.
        bills = filter_bills_by_last_updated(since=datetime.date(2018, 12, 1), until=datetime.date.today())
        self.assertGreater(len(bills), 0)

if __name__ == '__main__':
    unittest.main()
