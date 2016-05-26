# GBIF-downloads
Create user downloads using the GBIF API http://www.gbif.org/developer/summary 
The script produces a JSON string consisting of predicates, the like of which can be found here:
http://www.gbif.org/developer/occurrence#predicates

Two download patterns are supported: Searching by n taxonkeys, or searching by n taxonkeys and a polygon.

The two variables below definded in the module ca nbe overwritten to use different facets.

geom = {'type': 'within', 'geometry': None}

species = {'type': 'or', 'predicates': None}
