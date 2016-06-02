"""
Name:   GBIF_download_chunks
Author: Stijn Van Hoey, INBO, 2016-06-02

In this example, username, email and credentials should be
provided by the user in order to make the example work.

To enable the chunk based version, a cookie-dict should be provided as well,
by checking in the devtools of the browser for the cookie containing the key
value information for the login.

Chunk based GBIF download function
"""

from gbif_download_chunks import GBIFChunkDownload

# fill in name, email and cookie info for login
example_chunk = GBIFChunkDownload('name', 'email',
                                  cookies_dict={"key": "value"})

# require occurrences in Belgium
example_chunk.add_predicate('COUNTRY', 'BE')

#define the chunk size
example_chunk.chunk_size = 5
taxonkeys = ['3189866',  '2498252', '3084923', '2340977', '3170247', '3151811',
             '3129663', '2441176', '2882443', '2437394', '5178057', '2439838',
             '8104460', '2482499', '3025858', '3026024', '3026295', '3026294']

# do the different requests (fill in user_name and password)
example_chunk.run_iterative_download("TAXON_KEY", taxonkeys,
                                     ('user_name', 'password'))