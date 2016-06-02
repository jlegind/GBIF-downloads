# GBIF-downloads with Python
Create user downloads using the GBIF API http://www.gbif.org/developer/summary . Recognizing that the normal GBIF portal search and download services are not well suited for downloads based on a large number of species names, this module addresses the situation by allowing users to submit a file containing species keys. Additionally it allows users to add a map polygon to the search as well.   

The script produces a JSON string consisting of predicates[1] which are fed into a service request.</br>
[1] http://www.gbif.org/developer/occurrence#predicates


The script **does *not* return an object** since the request is handled entirely within the GBIF domain. Users should check the status of their downloads: http://www.gbif.org/user/download


## Usage GBIF downloader

In python, an object is created to start the json-building
```python
example.GBIFDownload('your_name', 'your_email')
```

Three download patterns are directly supported:
* Searching by n values for a specified variable, using the `add_iterative_predicate` function.
* Searching relative (typically `within`) a Polygon, using the `add_geometry` function.
* Adding a regular predicate (a value of a variable with a predicate type), using the `add_predicate` function

The request can be executed by using the function `run_download`, which makes a request based on the given predicates:
```python
example.run_download(('your_gbif_user_name', 'your_password'))
```

When adding a predicate for `COUNTRY` and a list of `TAXONKEY`s [3084923, 2498252, 3189866] as predicates, the resulting json will look like:

```json
{'created': 2016,
 'creator': 'your_name',
 'notification_address': ['your_email'],
 'predicate': {'predicates': [{'key': 'COUNTRY',
                               'type': 'equals',
                               'value': 'BE'},
                              {'predicates': [{'key': 'TAXON_KEY',
                                               'type': 'equals',
                                               'value': 3084923},
                                              {'key': 'TAXON_KEY',
                                               'type': 'equals',
                                               'value': 2498252},
                                              {'key': 'TAXON_KEY',
                                               'type': 'equals',
                                               'value': 3189866}],
                               'type': 'or'}],
               'type': 'and'},
 'send_notification': 'true'}
```

See `example_download.py` for the example code.

The most typical usecase involves a number of species keys (sorry, but you have to get these first - use the excellent rgbif package from rOpenSci https://github.com/ropensci/rgbif or Scott Chamberlain's pygbif https://github.com/sckott/pygbif) and perhaps a map polygon.


The download service can probably not handle more than a few hundred taxon-keys at the time, so limiting a request to < 100 keys to begin with would be prudent.

The same could be said for polygons - if a very complex shape (> 100 points) gets the download killed repeatedly, try simplifying the shape.

## Usage GBIF Chunk downloader

To partly solve the issue of the limit on download restrictions, an extended version of the GBIF_downloader is available, which can process a list of values by making chunks and making individual requests.

The functionality provides two elements:
 * split the original set of values (list) in chunks of a user-defined size
 * send the requests for each chunk, taking into account the limit in
   number of downloads by checking for each request if it is handled. The latter is done by checking if a new doi is available on the user/download page.

See `example_chunk_download.py` for the example code.
