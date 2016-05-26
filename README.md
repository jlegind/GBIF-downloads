# GBIF-downloads
Create user downloads using the GBIF API http://www.gbif.org/developer/summary 

The script produces a JSON string consisting of predicates, the like of which can be found here:
http://www.gbif.org/developer/occurrence#predicates

Two download patterns are supported: Searching by n taxonkeys, or searching by n taxonkeys and a polygon.

The two variables below definded in the module can be overwritten to use different facets.

```
geom = {'type': 'within', 'geometry': None}
species = {'type': 'or', 'predicates': None}
predicate_construct = {'type': 'equals', 'key': 'TAXON_KEY', 'value': None}
```

## Usage pattern
The most typical usecase involves a number of species keys (sorry, but you have to get these first - use the excellent rgbif package from rOpenSci https://github.com/ropensci/rgbif or Scott Chamberlain's pygbif https://github.com/sckott/pygbif) and perhaps a map polygon.

```
gd.run_download("/home/user/Documents/species.csv", payload, 'username', 'user@mail.org', credentials=('username', 'passw0rd'), polygon='POLYGON((-14.0625 42.553080, 9.84375 38.272688, -7.03125 26.431228, -14.0625 42.553080))')
```
