#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jtracker_models.github_jtracker import GithubJTracker
from jtracker_models.etcd_jtracker import ETCDJTracker
import json
import sys

def main():
    """ Main program """

    jtrackers = []
    print(sys.argv[1])
    exit()

    etcd_instances = [
        {'server':'http://142.1.177.127:8001','username':'baminou','queue':'ae287475-3f0e-498b-9188-84f92775094a'},
        {'server':'http://142.1.177.127:8001','username':'baminou','queue':'9c31e4e4-2122-4939-9175-05cebc56d5b9'},
        {'server':'http://142.1.177.127:8001','username':'baminou','queue':'30b05f9e-982e-4c66-b7ae-2028a2bffa81'},
        {'server':'http://142.1.177.127:8001','username':'baminou','queue':'5c9383ae-9fa7-4d97-81aa-a036881de70f'},
        {'server':'http://142.1.177.127:8001','username':'baminou','queue':'afd828f1-0698-4c57-b8c8-47acadb8dd40'},
        {'server':'http://142.1.177.127:8001','username':'baminou','queue':'ed12f874-bf2a-4ba5-8ad7-5d2cb0f73412'},
        {'server':'http://142.1.177.127:8001','username':'baminou','queue':'eb91c53b-93d2-4daa-9816-b5ec0ec737d9'},
    ]

    gh_instances = [
        '/Users/baminou/Documents/ega-file-transfer-to-collab-1-jtracker/ega-file-transfer-to-collab.0.6.jtracker',
        '/Users/baminou/Documents/ega-file-transfer-to-collab-1-jtracker/ega-file-transfer-to-collab.0.7.jtracker',
        '/Users/baminou/Documents/ega-file-transfer-to-collab-2-jtracker/ega-file-transfer-to-collab.0.6.jtracker',
        '/Users/baminou/Documents/ega-file-transfer-to-collab-3-jtracker/ega-file-transfer-to-collab.0.6.jtracker',
        '/Users/baminou/Documents/ega-file-transfer-to-collab-4-jtracker/ega-file-transfer-to-collab.0.6.jtracker',
        '/Users/baminou/Documents/ega-file-transfer-to-collab-5-jtracker/ega-file-transfer-to-collab.0.6.jtracker',
    ]

    for etcd_instance in etcd_instances:
        jtrackers.append(ETCDJTracker(etcd_instance['server'],etcd_instance['username'],etcd_instance['queue']))

    for gh_instance in gh_instances:
        jtrackers.append(GithubJTracker([gh_instance]))

    with open(sys.argv[1],'w') as fp:
        for jtracker_instance in jtrackers:
            jobs = jtracker_instance.get_jobs()
            for job_id in jobs:
                stats = jtracker_instance.get_stats(jobs[job_id])
                stats['bundle_id'] = jtracker_instance.get_job_data(job_id).get('bundle_id')
                json.dump(fp)
                fp.writelines('\n')
    return 0

if __name__ == "__main__":
    main()