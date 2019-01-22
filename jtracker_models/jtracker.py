
import abc

class JTracker:

    def __init__(self):
        return

    @abc.abstractmethod
    def get_job_ids(self, state=None):
        raise NotImplementedError

    @abc.abstractmethod
    def get_job_data(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_job(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_jobs(self, state=None):
        raise NotImplementedError

    @staticmethod
    def combine(jtrackers, state=None):
        def __merge(dict1, dict2):
            res = {**dict1, **dict2}
            return res

        jobs = {}
        for jtracker in jtrackers:
            for job_id in jtracker.get_job_ids(state):
                jobs[job_id] = jtracker.get_job_data(job_id)
        return jobs