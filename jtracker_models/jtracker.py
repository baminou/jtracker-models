
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
            jobs =  __merge(jobs,jtracker.get_jobs(state))
        return jobs