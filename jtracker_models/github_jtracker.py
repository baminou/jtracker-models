

from .jtracker import JTracker
import os
import fnmatch
import json
import datetime

STATES = ['completed','backlog','running','failed','queued']

class GithubJTracker(JTracker):

    def __init__(self, respositories):
        self._repositories = respositories
        self._jobs = {}
        self._load_repositories()
        return

    def _load_repositories(self):
        for repo in self._repositories:
            if not self.validate_folder(repo):
                raise Exception("The repo is not a valid jtracker repository: " + repo)

            for state in STATES:
                for job_dir in self._list_jobs_dir_in_repo(os.path.join(repo,"job_state."+state)):
                    job_path = self.retrieve_job_in_job_repo(job_dir)
                    with open(job_path, 'r') as fp:
                        self._jobs[job_path] = json.load(fp)
                        self._jobs[job_path]['tasks'] = self.retrieve_tasks_in_job_repo(job_dir)
                        return
        return

    def validate_folder(self, repo):
        content = os.listdir(repo)
        return 'job_state.completed' in content

    def _get_state(self, job_name):
        for state in STATES:
            if "job."+state in job_name:
                return state

    def get_job_ids(self, state=None):
        if state == None:
            return self._jobs.keys()
        return [id for id in self._jobs.keys() if "job."+state in id]

    def get_jobs(self, state=None):
        return self._jobs

    def get_job(self, id):
        return self._jobs[id]

    def get_job_data(self, id):
        return self.get_job(id)

    def _list_jobs_in_repo(self, repo):
        jobs = []
        for root, dirnames, filenames in os.walk(repo):
            for filenames in fnmatch.filter(filenames, 'job.*.json'):
                jobs.append(os.path.join(root,filenames))
        return jobs

    def retrieve_job_in_job_repo(self, repo):
        for file in os.listdir(repo):
            if file.startswith('job.') and file.endswith('.json'):
                return os.path.join(repo,file)
        return None

    def retrieve_tasks_in_job_repo(self, repo):
        tasks = {}
        for task_state in os.listdir(repo):
            task_state_full_path = os.path.join(repo,task_state)
            if os.path.isdir(task_state_full_path) and task_state.startswith('task_state.'):
                for worker_path in os.listdir(task_state_full_path):
                    if worker_path.startswith('worker.'):
                        worker_full_path = os.path.join(task_state_full_path,worker_path)
                        for tmp in os.listdir(worker_full_path):
                            tmp_full_path = os.path.join(worker_full_path, tmp)
                            for task_file in os.listdir(tmp_full_path):
                                task_full_path = os.path.join(tmp_full_path,task_file)
                                tasks[task_full_path] = json.load(open(task_full_path))
        return tasks


    def _list_jobs_dir_in_repo(self, repo):
        jobs = []
        for root, dirnames, filenames in os.walk(repo):
            for dirname in fnmatch.filter(dirnames, 'job.*'):
                jobs.append(os.path.join(root,dirname))
        return jobs

    def get_start_times(self, tasks_dict):
        start_times = []
        for _key in tasks_dict:
            start_times.append(tasks_dict[_key].get('output')[0].get('runtime').get('task_start'))
        return start_times

    def get_completion_times(self, tasks_dict):
        stop_times = []
        for _key in tasks_dict:
            stop_times.append(tasks_dict[_key].get('output')[0].get('runtime').get('task_stop'))
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


