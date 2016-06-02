"""
Name:   GBIF_download_chunks
Author: Stijn Van Hoey, INBO, 2016-06-02
Enables users to launch user_downloads against the GBIF API
http://www.gbif.org/developer/occurrence#download
Requires a user account on GBIF.org since credentials are needed.

GBIF restricts the download in order to improve the spread of resources.
Complex queries (e.g. >100 points in polygon, >50 taxonkeys) are killed and the
maximal amount of downloads at the same time is set on 3
(or 1 when requests peak).

In order to handle these restrictions, this functionality provides
two elements:
 * split the original set of values (list) in chunks of a user-defined size
 * send the requests for each chunk, taking into account the limit in
   number of downloads
"""

from bs4 import BeautifulSoup
import requests
import time

from gbif_download import GBIFDownload


class GBIFChunkDownload(GBIFDownload):

    def __init__(self, creator, email, cookies_dict,
                 chunk_size=10, polygon=None):
        """extension on the GBIFDownload to enable the chunkwise request of an
        iterative predicate, as more complex queries are otherwise killed.
        Moreover, the processing of the request is checked on the user download
        page to verify the effective processing of the request (indirectly
        taking into account the limits of 3 downloads at the same time)

        :param creator: User name.
        :param email: user email
        :param cookies_dict: Dictionary with the combination of the cookie as
        extracted from a browser after login into the GBIF webpage. This
        is a rather hacky way of using the login and should be improved
        :param chunk_size: number of values from an iterative that are
        combined in a single request
        :param polygon: Polygon of points to extract data from
        """
        super().__init__(creator, email, polygon)
        self._chunk_size = chunk_size
        self.cookies_dict = cookies_dict

    @property
    def chunk_size(self):
        """get chunk_size"""
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value):
        """set chunk_size

        :param value: size of the individual chunks used for the iterative
        predicate
        """
        if value > 50:
            print("Download service can probably not handle given chunk size.")
        elif value < 0:
            raise Exception("Negative chunk size not possible")
        self._chunk_size = value

    @staticmethod
    def taxon_chunks(l, n):
        """Yield successive n-sized chunks from a list.
        """
        for i in range(0, len(l), n):
            yield l[i:i + n]

    @staticmethod
    def _get_current_dois(page):
        """extract current doi values present on a page
        """
        doi_environments = page.find_all('dd')
        dois = []
        for el in doi_environments:
            if el.find('a'):
                if 'doi' in el.find('a').getText():
                    dois.append(el.find('a').getText())
        return dois

    def scrape_doi_from_page(self):
        """open the user page of gbif and scrape the current doi values present
        on the first pager

        :param cookies_dict: dictionary as derived from the cookies in the
        browser when being logged in the http://www.gbif.org/user/download page
        Rather 'hacky' way, but enables easy handling of the login procedure.
        """
        r = requests.get("http://www.gbif.org/user/download",
                         cookies=self.cookies_dict)
        soup = BeautifulSoup(r.content, "html.parser")
        return self._get_current_dois(soup)

    def run_iterative_download(self, key, values_list, credentials):
        """
        Splits the request of an iterative list of values in chunks to make
        a set of requests.
        It is assumed that only the predicate is only one level nested and
        only one iterative element is processed

        :param key: value for which the iterative is handled
        :param values_list: Filename or list containing the taxon keys to be
        searched.
        :param credentials: Username and password tuple.
        :return:
        """
        values = self._extract_values(values_list)

        for subset_values in self.taxon_chunks(values, self.chunk_size):

            # remove previous iterative predicates
            predicate = []
            for j, el in enumerate(self.predicates):
                if "predicates" in el.keys():
                    predicate.append(j)
            if predicate:
                for index in predicate:
                    self.predicates.pop(index)

            # add chunk as iterative predicate
            self.add_iterative_predicate(key, subset_values)

            ref_dois = self.scrape_doi_from_page()
            while ref_dois == self.scrape_doi_from_page():
                self.run_download(credentials)
                time.sleep(60)
