#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jtracker_models.github_jtracker import GithubJTracker
from jtracker_models.etcd_jtracker import ETCDJTracker
import json
import sys

def main():
    """ Main program """

    jtrackers = []

    etcd_instances = [
        {'server':'http://142.1.177.127:8001','username':'baminou','queue':'ae287475-3f0e-498b-9188-84f92775094a'}
    ]

    gh_instances = [
        #'/Users/baminou/Documents/ega-file-transfer-to-collab-1-jtracker/ega-file-transfer-to-collab.0.6.jtracker',
        #'/Users/baminou/Documents/ega-file-transfer-to-collab-1-jtracker/ega-file-transfer-to-collab.0.7.jtracker',
        #'/Users/baminou/Documents/ega-file-transfer-to-collab-2-jtracker/ega-file-transfer-to-collab.0.6.jtracker',
        #'/Users/baminou/Documents/ega-file-transfer-to-collab-3-jtracker/ega-file-transfer-to-collab.0.6.jtracker',
        #'/Users/baminou/Documents/ega-file-transfer-to-collab-4-jtracker/ega-file-transfer-to-collab.0.6.jtracker',
        '/Users/baminou/Documents/ega-file-transfer-to-collab-5-jtracker/ega-file-transfer-to-collab.0.6.jtracker',
    ]

    for etcd_instance in etcd_instances:
        instance = ETCDJTracker(etcd_instance['server'],etcd_instance['username'],etcd_instance['queue'])
        print(len(instance.get_jobs('completed')))
        jtrackers.append(instance)

    for gh_instance in gh_instances:
        instance = GithubJTracker([gh_instance])
        print(len(instance.get_jobs('queued')))
        jtrackers.append(instance)

    return

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