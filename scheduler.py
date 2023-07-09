import datetime
import json
import sys
from dataclasses import dataclass

from job import Job


class Scheduler:
    def __init__(self, jobs: list, pool_size: int = 10):
        self.jobs = jobs
        self.job_in_progress: int = 0
        self.used_job = []
        self.pool_size = pool_size

    @staticmethod
    def check_dependencies(job: Job) -> bool:
        no_dependencies = True
        for dependence in job.dependencies:
            if dependence.status != "F":
                no_dependencies = False
        return no_dependencies

    def run(self):
        while len(self.jobs) > 0:
            for job in self.jobs:
                if job.tries < 0:
                    job.status = "FE"
                if job.status in ["F", "FE"]:
                    self.job_in_progress -= 1
                    self.used_job.append(job)
                    self.jobs.remove(job)
                if job.status == "Q":
                    self.job_in_progress += 1
                if job.start_at < datetime.datetime.now() and self.check_dependencies(job) and self.job_in_progress < self.pool_size:
                    try:
                        next(job.iter)
                    except:
                        pass
        for job in self.used_job:
            print(job.result)


def sum(x, y):
    for i in range(100000000):
        x += y
    return x


def print_sum(sum):
    print("Sum = ", sum)


if __name__ == "__main__":
    jobs = []
    jobs.append(Job(sum, [1, 2]))
    jobs.append(Job(print_sum, [jobs[0].result,], dependencies=[jobs[0]]))
    scheduler = Scheduler(jobs)
    scheduler.run()