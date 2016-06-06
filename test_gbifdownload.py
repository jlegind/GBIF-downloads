import gbif_download as gd
import re
import download as dl
import time


gd.predicate_construct['key'] = 'BASIS_OF_RECORD'
# my_search_terms = "/home/user/Documents/species.csv"
my_search_terms = ['FOSSIL_SPECIMEN', 'LITERATURE']

predicate = {'type': 'equals', 'key': 'TAXON_KEY', 'value': None}
taxon_values = [2385839, 2396404]


def test_run_download(user, email, credentials):
    # Use the username and email from the GBIF Portal and the same log in credentials
    # Credentials must be a tuple
    r = gd.run_download(my_search_terms, gd.payload, user, email, credentials, polygon=None)
    try:
        dl_id = r.headers['Location']
    except KeyError:
        print "You might have too many downloads running at the same time. Check your downloads page!"

    a_match = re.search(r"[0-9-]*$", dl_id, re.M)
    dl_key = a_match.group()

    while dl.download_meta(dl_key)['status'] in ['PREPARING', 'RUNNING']:
        print ' Preparing ...',
        time.sleep(10)

    assert dl.download_meta(dl_key)['status'] == 'SUCCEEDED', "Download did not commence !"


def test_make_predicate():
    res = gd.make_predicate(predicate, taxon_values)
    print res
    assert list == res.__class__
    assert res[0]['value'] == 2396404 and res[1]['key'] == 'TAXON_KEY'

