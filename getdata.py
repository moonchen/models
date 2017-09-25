""" Request info from import.io
"""
from __future__ import print_function
import itertools
import csv
from collections import defaultdict

import requests
import secret
from furl import furl
from preprocess import process_row, OUTPUT_KEYS

IMPORTIO_URL = "https://api.import.io/store/connector/947d5f9a-de0d-4cf7-8732-bcfc1b2453e8/_query"
AUTOTRADER_URL = "https://www.autotrader.com/cars-for-sale/Tesla/Model+S/Austin+TX-78705?zip=78705&startYear=1981&numRecords=100&sortBy=distanceASC&firstRecord=0&endYear=2018&modelCodeList=TESMODS&makeCodeList=TESLA&searchRadius=0"

def getpage(page_num):
    """
    Get a page of Model S listings
    """
    first_record = page_num * 100
    importio_furl = furl(IMPORTIO_URL)
    importio_furl.args['_apikey'] = secret.APIKEY

    autotrader_furl = furl(AUTOTRADER_URL)
    autotrader_furl.args['firstRecord'] = first_record
    importio_furl.args['input'] = 'webpage/url:' + autotrader_furl.url

    importio_request = requests.get(importio_furl.url)
    return importio_request.json()

def get_all():
    """ Generate all results """
    for i in itertools.count():
        page_results = getpage(i)

        if not page_results['results']:
            return
        print('Got', len(page_results['results']), 'results.')
        for result in page_results['results']:
            yield result

def main():
    """
    do it
    """
    with open('dataset.processed.csv', 'w') as outputfile:
        writer = csv.DictWriter(outputfile, OUTPUT_KEYS)
        writer.writeheader()
        for row in get_all():
            output_row = process_row(defaultdict(str, row))
            writer.writerow(output_row)

if __name__ == "__main__":
    main()
