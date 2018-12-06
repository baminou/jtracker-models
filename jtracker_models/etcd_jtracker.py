#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .jtracker import JTracker
import requests
import json
import logging
import datetime


class ETCDJTracker(JTracker):

    def __init__(self, server, user, queue):
        self._server = server
        self._user = user
        self._queue = queue
        self._load_jobs()
        return

    def get_jobs(self, state=None):
        return self._jobs

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
                if job.get('state') == state:
                    ids.append(job.get('id'))
            else:
                ids.append(job.get('id'))
        return ids

    def get_job_data(self, id):
        return json.loads(self.get_job(id).get('job_file'))

    def get_job(self, id):
        return self._jobs[id]

    def get_start_times(self, tasks_dict):
        start_times = []
        for _key in tasks_dict:
            start_times.append(json.loads(tasks_dict[_key].get('task_file')).get('output')[0].get('_jt_').get('wall_time').get('start'))
        return start_times

    def get_completion_times(self, tasks_dict):
        stop_times = []
        for _key in tasks_dict:
            stop_times.append(json.loads(tasks_dict[_key].get('task_file')).get('output')[0].get('_jt_').get('wall_time').get('end'))
        return stop_times

    def get_stats(self, job):
        start_date_sec = min(self.get_start_times(job.get('tasks')))
        completion_date_sec = max(self.get_completion_times(job.get('tasks')))
        return {
            'start_date': datetime.datetime.fromtimestamp(start_date_sec).strftime('%Y-%m-%d'),
            'start_time': datetime.datetime.fromtimestamp(start_date_sec).strftime('%H:%M:%S'),
            'completion_date': datetime.datetime.fromtimestamp(completion_date_sec).strftime('%Y-%m-%d'),
            'completion_time': datetime.datetime.fromtimestamp(completion_date_sec).strftime('%H:%M:%S'),
            'duration': completion_date_sec - start_date_sec
        }

