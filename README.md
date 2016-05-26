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
The most typical usecase involves a number of species keys (sorry, but you have to get these first - use the excellent rgbif package from rOpenSci https://github.com/ropensci/rgbif) and perhaps a map polygon.
