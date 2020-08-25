#!/usr/bin/env python

import os
import json
import argparse
import tempfile
import urllib.parse

import sls_client.query as sls_query

def main():
    qs = urllib.parse.urlencode([("type", "host"), ("group-communities", "CCSTAR")])
    response = sls_query.query(qs)

    sites = {}
    for record in response:
        skip = False
        for key in ['location-sitename', 'location-latitude', 'location-longitude', 'host-name']:
            if key not in record:
                skip = True
                hostname = record.get("host-name", ["unknown"])[-1]
                print("WARNING: Entry with hostname {} has missing data: {}".format(hostname, key))
        if skip:
            continue
        site = record['location-sitename'][-1]
        site_info = sites.setdefault(site, {})
        site_info['Latitude'] = record['location-latitude'][-1]
        site_info['Longitude'] = record['location-longitude'][-1]
        site_info['Name'] = site
        site_info['LongName'] = site
        resources = site_info.setdefault('Resources', [])
        resources.append({"Name": record['host-name'][-1]})

    if sites:
        print("Sites for community {}: {}\n".format("CCSTAR", len(sites)))
    else:
        print("No known sites for community {}".format("CCSTAR"))

    # Put the data into redis
    return sites
    #r = redis.from_url(os.environ.get("REDIS_URL"))
    #print(r.set("pslocations", json.dumps(sites)))


if __name__ == '__main__':
    main()
