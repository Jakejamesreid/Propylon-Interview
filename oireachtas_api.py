#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set of functions to query the Oireachtas api at
https://api.oireachtas.ie/v1/
"""
import os
from datetime import *
import requests
                    
MEMBERS_ENDPOINT = 'https://api.oireachtas.ie/v1/members'

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

    # Legislation endpoint with parameters defined
    legislationEndpoint = f"https://api.oireachtas.ie/v1/legislation?bill_status=Current,Withdrawn,Enacted,Rejected,Defeated,Lapsed&bill_source=Government,Private%20Member&date_start=1900-01-01&date_end=2099-01-01&member_id={memberURI}&lang=en"

    return get_endpoint_data(legislationEndpoint)
    

def filter_bills_by_last_updated(since, until):
    """Return bills updated within the specified date range

    :param datetime.date since: The lastUpdated value for the bill
        should be greater than or equal to this date
    :param datetime.date until: The lastUpdated value for the bill
        should be less than or equal to this date. If unspecified, until
        will default to today's date
    :return: List of bill records
    :rtype: list

    """
    raise NotImplementedError

sponsoredBills = filter_bills_sponsored_by("IvanaBacik")
print(sponsoredBills)
