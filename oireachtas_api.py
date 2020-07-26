#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set of functions to query the Oireachtas api at
https://api.oireachtas.ie/v1/

Specifically, they use the data obtained from the `legislation` and `members`
api endpoints to answer the questions:

* Which bills were sponsored by a given member ?
* Which bills were last updated within a specified time period ?
"""
import os, sys
import datetime
import requests
import json
                    
MEMBERS_ENDPOINT = 'https://api.oireachtas.ie/v1/members'
LEGISLATION_ENDPOINT = 'https://api.oireachtas.ie/v1/legislation'

def get_endpoint_data(uri):
    """Returns data queried from provided endpoint

    :param str uri: The URI used for connecting to the API 
    :rtype: dict
    """
    response = requests.get(uri)

    # Raise an exception if a request is unsuccessful
    try:
        response.raise_for_status()

        if "application/json" not in response.headers.get('content-type'):
            raise ValueError(f"Response from {uri} is not in json format")
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err, f"Invalid URI {uri}")
    except requests.exceptions.RequestException:
        raise Exception(f'Failed to connect to {uri}')

    # Convert the response to a dict
    requestDict = response.json()
    return requestDict["results"]

def filter_bills_sponsored_by(pId):
    """Return bills sponsored by the member with the specified pId

    :param str pId: The pId value for the member
    :rtype: dict
    """
    members = get_endpoint_data(MEMBERS_ENDPOINT)

    # Generator expression to identify the members whose pId is the same as the user defined pId
    try:
        memberGenerator = (member for member in members if pId == member['member']['pId'])
        member = next(memberGenerator)
    except StopIteration as err:
        raise StopIteration(err, f"No URI associated with the pId value provided, check that the pId ({pId}) entered is correct.")
    
    memberURI = member['member']['uri']

    # Call to Legislation endpoint with parameters defined
    legislationParameters = f"?bill_status=Current,Withdrawn,Enacted,Rejected,Defeated,Lapsed&member_id={memberURI}&lang=en"
    legislationEndpoint = LEGISLATION_ENDPOINT+legislationParameters
    return get_endpoint_data(legislationEndpoint)
    

def filter_bills_by_last_updated(since=datetime.date(1990, 1, 1), until=datetime.date.today()):
    """Return bills updated within the specified date range

    :param datetime.date since: The lastUpdated value for the bill
        should be greater than or equal to this date
    :param datetime.date until: The lastUpdated value for the bill
        should be less than or equal to this date. If unspecified, until
        will default to today's date
    :return: List of bill records
    :rtype: list

    """
    # Call to Legislation endpoint with parameters defined
    legislationParameters = f"?bill_status=Current,Withdrawn,Enacted,Rejected,Defeated,Lapsed&lang=en"
    legislationEndpoint = LEGISLATION_ENDPOINT+legislationParameters
    bills = get_endpoint_data(legislationEndpoint)

    billNos = []
    billsWithinDateRange = []
    for bill in bills:
        # Time part of date denoted by 'T' is not needed so this can be removed
        date = bill["bill"]["lastUpdated"].split("T")

        # Convert lastUpdated to a Date object in yyyymmdd format
        billLastUpdated = datetime.datetime.strptime(date[0], '%Y-%m-%d').date()

        if billLastUpdated > since and billLastUpdated <= until:
            # Prevent adding same bill updated multiple times within date range
            if bill["bill"]["billNo"] not in billNos:
                billsWithinDateRange.append(bill)
                billNos.append(bill["bill"]["billNo"])

    return billsWithinDateRange
    

# sponsoredBills = filter_bills_sponsored_by("GerryAdams")
# print(sponsoredBills)

# bills = filter_bills_by_last_updated(datetime.date(1990, 1, 1), datetime.date.today())
# print(bills)
