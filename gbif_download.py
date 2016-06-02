"""
Name:   GBIF_download
Author: Jan K. Legind, Global Biodiversity Information Facility (GBIF), 2016-05-26
Enables users to launch user_downloads against the GBIF API http://www.gbif.org/developer/occurrence#download
Requires a user account on GBIF.org since credentials are needed.
Two patterns are supported: Searching by n taxonkeys, or searching by n taxonkeys and a polygon
The main function run_download() does not return any value since the download is handled entirely in the GBIF domain.
"""

import requests
import json
import csv
import datetime
import pprint


class GBIFDownload(object):

    def __init__(self, creator, email, polygon=None):
        """class to setup a JSON doc with the query and POST a request

        All predicates (default key-value or iterative based on a list of
        values) are combined with an AND statement. Iterative predicates are
        creating a subset equal statements combined with OR

        :param creator: User name.
        :param email: user email
        :param polygon: Polygon of points to extract data from
        """
        self.predicates = []

        self.url = 'http://api.gbif.org/v1/occurrence/download/request'
        self.header = {'Content-Type': 'application/json'}
        self.payload = {'creator': creator,
                        'notification_address': [email],
                        'send_notification': 'true',
                        'created': datetime.date.today().year,
                        'predicate': {
                            'type': 'and',
                            'predicates': self.predicates
                            }
                        }

        # prepare the geometry polygon constructions
        if polygon:
            self.add_geometry(polygon)

    def add_predicate(self, key, value, predicate_type='equals'):
        """
        add key, value, type combination of a predicate

        :param key: query KEY parameter
        :param value: the value used in the predicate
        :param predicate_type: the type of predicate (e.g. equals)
        """
        self.predicates.append({'type': predicate_type,
                                'key': key,
                                'value': value
                                })

    @staticmethod
    def _extract_values(values_list):
        """extract values from either file or list

        :param values_list: list or file name (str) with list of values
        """
        values = []
        # check if file or list of values to iterate
        if isinstance(values_list, str):
            with open(values_list) as ff:
                reading = csv.reader(ff)
                for j in reading:
                    values.append(j[0])
        elif isinstance(values_list, list):
            values = values_list
        else:
            raise Exception("input datatype not supported.")
        return values

    def add_iterative_predicate(self, key, values_list):
        """add an iterative predicate with a key and set of values
        which it can be equal to in and or function

        :param key: API key to use for the query.
        :param values_list: Filename or list containing the taxon keys to be searched.

        """
        values = self._extract_values(values_list)

        predicate = {'type': 'equals', 'key': key, 'value': None}
        predicates = []
        while values:
            predicate['value'] = values.pop()
            predicates.append(predicate.copy())
        self.predicates.append({'type': 'or', 'predicates': predicates})

    def add_geometry(self, polygon, geom_type='within'):
        """add a geometry type of predicate

        :param polygon: In this format 'POLYGON((x1 y1, x2 y2, x3 y3,... xn yn))'
        :param geom_type: type of predicate, e.g. within
        :return:
        """
        self.predicates.append({'type': geom_type, 'geometry': polygon})

    def run_download(self, credentials):
        """
        :param credentials: Username and password tuple.
        :return:
        """

        pprint.pprint(self.payload)
        requests.post(self.url, auth=credentials,
                      data=json.dumps(self.payload),
                      headers=self.header)
        print("request sent, check http://www.gbif.org/user/download for progress...")

