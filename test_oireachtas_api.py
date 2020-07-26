#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from unittest.mock import Mock, patch
from datetime import datetime, date, timedelta
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

        # Send a request to the API server and confirm that the response is okay
        response = requests.get(LEGISLATION_ENDPOINT)
        self.assertTrue(response.ok)

    def test_members_api_response_status(self):

        # Send a request to the API server and confirm that the response is okay
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

    def test_get_endpoint_data_legislation_HTTPError(self):

        # SystemExit exception raised when endpoint passed an invalid parameter
        with self.assertRaises(SystemExit) as cm:
            params = '?bill_status=Invalid'
            get_endpoint_data(LEGISLATION_ENDPOINT+params)

        self.assertEqual(
            cm.exception.code[1], f"Invalid URI {LEGISLATION_ENDPOINT+params}")

    def test_get_endpoint_data_members_HTTPError(self):

        # SystemExit exception raised when endpoint passed an invalid parameter
        with self.assertRaises(SystemExit) as cm:
            params = '?date_start=Invalid'
            get_endpoint_data(LEGISLATION_ENDPOINT+params)
        self.assertEqual(
            cm.exception.code[1], f"Invalid URI {LEGISLATION_ENDPOINT+params}")


class TestFilterBillsSponsoredBy(unittest.TestCase):

    def test_filter_bills_sponsored_by_response(self):
        # If the request is sent successfully, then a response should be returned.
        results = filter_bills_sponsored_by('IvanaBacik')
        self.assertGreaterEqual(len(results), 0)

    def test_filter_bills_sponsored_by_invalid_pId(self):

        # StopIteration exception raised when invalid pId passed
        with self.assertRaises(StopIteration) as cm:
            pId = 'Invalid'
            filter_bills_sponsored_by(pId)
        self.assertEqual(
            cm.exception.args[1], f"No URI associated with the pId value provided, check that the pId ({pId}) entered is correct.")


class TestFilterBillByLastUpdated(unittest.TestCase):

    def test_filter_bills_by_last_updated_response(self):

        # If the request is sent successfully, then a response should be returned.
        bills = filter_bills_by_last_updated(
            since=date(2018, 12, 1), until=date.today())
        self.assertGreater(len(bills), 0)

    def test_filter_bills_by_last_updated_error(self):

        # ValueError if startDate > endDate
        with self.assertRaises(ValueError) as cm:
            startDate = date.today()+timedelta(days=1)
            endDate = date.today()
            filter_bills_by_last_updated(startDate, endDate)
        self.assertEqual(
            cm.exception.args[0], f"Start Date {startDate} is greater than end date {endDate}")


if __name__ == '__main__':
    unittest.main()