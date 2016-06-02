"""
Name:   GBIF_download_chunks
Author: Stijn Van Hoey, INBO, 2016-06-02

In this example, username, email and credentials should be
provided by the user in order to make the example work.

Default GBIF download function
"""

import pprint

from gbif_download import GBIFDownload

# fill in name and email
example = GBIFDownload('name', 'email')

# require occurrences in Belgium
example.add_predicate('COUNTRY', 'BE')
# require either of three taxonkeys
example.add_iterative_predicate('TAXON_KEY', [3189866, 2498252, 3084923])
pprint.pprint(example.payload)

# do request (fill in user_name and password)
example.run_download(('user_name', 'password'))


