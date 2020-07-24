#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set of functions to query the Oireachtas api at
https://api.oireachtas.ie/v1/
"""
import os
from json import *
from datetime import *


LEGISLATION_DATASET = 'legislation.json'
MEMBERS_DATASET = 'members.json'


def load(jfname): return loads(
    open(os.path.join(sys.path[0]+"\\data\\", jfname)).read())


def filter_bills_sponsored_by(pId):
    """Return bills sponsored by the member with the specified pId

    :param str pId: The pId value for the member
    :return: dict of bill records
    :rtype: dict
    """
    legislation = load(LEGISLATION_DATASET)
    members = load(MEMBERS_DATASET)
    sponsoredBills = []

    for result in legislation['results']:
        sponsors = result['bill']['sponsors']
        for sponsor in sponsors:
            name = sponsor['sponsor']['by']['showAs']

            for member in members['results']:
                fname = member['member']['fullName']
                rpId = member['member']['pId']
                if fname == name and rpId == pId:
                    sponsoredBills.append(result['bill'])
    return sponsoredBills


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


answer = filter_bills_sponsored_by("IvanaBacik")
print(answer)
