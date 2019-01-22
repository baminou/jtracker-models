#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .jtracker import JTracker
import requests
import json
import logging


class ETCDJTracker(JTracker):

    def __init__(self, server, user, queue):
        super().__init__()
        self._server = server
        self._user = user
        self._queue = queue
        self._load_jobs()
        return

    def get_jobs(self, state=None):
        jobs = []
        for id in self._jobs:
            if not state == None:
                if self._jobs[id].get('state') == state:
                    jobs.append(self._jobs[id])
            else:
                jobs.append(self._jobs[id])
        return jobs

    def _load_jobs(self):
        self._jobs = {}
        url = self._server+"/api/jt-jess/v0.1/jobs/owner/"+self._user+"/queue/"+self._queue
        for job in requests.get(url).json():
            self._jobs[job.get("id")] = job
        return

    def get_job_ids(self, state=None):
        ids = []
        for job in self._jobs:
            if not state == None:
                if self._jobs[job].get('state') == state:
                    ids.append(job)
            else:
                ids.append(job)
        return ids

    def get_job_data(self, id):
        return json.loads(self.get_job(id).get('job_file'))

    def get_job(self, id):
        return self._jobs[id]
