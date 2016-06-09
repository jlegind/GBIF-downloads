DEPRECATED!
==========
This project has been moved to Scott Chamberlain's **pygbif** - Please go to https://github.com/sckott/pygbif  

## GBIF-downloads with Python 
Create user downloads using the GBIF API http://www.gbif.org/developer/summary . Recognizing that the normal GBIF portal search and download services are not well suited for downloads based on a large number of species names, this module addresses the situation by allowing users to submit a file containing species keys. Additionally it allows users to add a map polygon to the search as well.   

The script produces a JSON string consisting of predicates[1] which are fed into a service request.</br>
[1] http://www.gbif.org/developer/occurrence#predicates


The script **does *not* return an object** since the request is handled entirely within the GBIF domain. Users should check the status of their downloads: http://www.gbif.org/user/download


Two download patterns are directly supported: Searching by n taxonkeys, or searching by n taxonkeys and a polygon.

The variables below defined in the module can be modified to use different facets.

```python
geom = {'type': 'within', 'geometry': None}
species = {'type': 'or', 'predicates': None}
predicate_construct = {'type': 'equals', 'key': 'TAXON_KEY', 'value': None}
```

### Usage pattern
The most typical usecase involves a number of species keys (sorry, but you have to get these first - use the excellent rgbif package from rOpenSci https://github.com/ropensci/rgbif or Scott Chamberlain's pygbif https://github.com/sckott/pygbif) and perhaps a map polygon.

```python
run_download("/home/user/Documents/species.csv", payload, 'username', 'user@mail.org', 
              credentials=('username', 'passw0rd'), 
              polygon='POLYGON((-14.0625 42.553080, 9.84375 38.272688, -7.03125 26.431228, -14.0625 42.553080))')
#payload is already defined in the script but can be modified
```
You can omit the polygon and just query by taxon keys.

Optionally you can override or modify the variables to get at other facets that the GBIF API surfaces. In this case a range of Basis-of-record:

```python
import gbif_download as gd


gd.predicate_construct['key'] = 'BASIS_OF_RECORD'

gd.run_download("/home/jan/Documents/lists/basis-of-record.csv", gd.payload, 'username', 'user@mail.org', 
                credentials=('username', 'passw0rd'), 
                polygon='POLYGON((-14.0625 42.553080, 9.84375 38.272688, -7.03125 26.431228, -14.0625 42.553080))')
```
###Caveats
The download service can probably not handle more than a few hundred taxon keys at the time, so limiting a request to < 100 keys to begin with would be prudent.</br>
The same could be said for polygons - if a very complex shape (> 100 points) gets the download killed repeatedly, try simplyfying the shape.
