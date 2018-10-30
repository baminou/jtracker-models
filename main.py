#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jtracker_models.github_jtracker import GithubJTracker

def main():
    """ Main program """

    gh_jt = GithubJTracker(["/Users/baminou/Documents/ega-file-transfer-to-collab-1-jtracker/ega-file-transfer-to-collab.0.6.jtracker"])
    print(gh_jt.get_job_ids())

    return 0

if __name__ == "__main__":
    main()