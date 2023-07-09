import datetime
import json
import sys
from dataclasses import dataclass
from urllib.request import urlopen
import json
import os

from job import Job


def get_weather(url):
    with urlopen(url) as response:
        return response.read().decode("utf-8")


def formatting(data):
    return data


def print_sum(sum):
    print("Sum = ",sum)


def os_work():
    os.mkdir("new_dir/")
    os.mknod("new_dir/newfile.txt")


def write(path, text):
    with open(path, "w") as file:
        file.write(text)


functions = {
    "get_weather": get_weather,
    "formatting": formatting,
    "print_sum": print_sum,
    "os_work": os_work,
    "write": write
}

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

                if job.start_at < datetime.datetime.now() and self.check_dependencies(job) and self.job_in_progress < self.pool_size:
                    if job.status == "Q":
                        self.job_in_progress += 1
                    try:
                        next(job.iter)
                    except:
                        pass

    def stop(self):
        json_data = {"jobs": [], "u_jobs": []}
        for job in self.jobs:
            json_data["jobs"].append({
                "task": job.task.__name__,
                "args": job.args,
                "start_at": job.start_at.ctime(),
                "max_working_time": job.max_working_time,
                "tries": job.tries,
                "status": job.status,
                "result": job.result,
                "dependencies": []
            })
            for dep in job.dependencies:
                json_data["jobs"][-1]["dependencies"].append(dep.task.__name__)
        with open("data/json_data.json", "w") as file:
            data = json.dumps(json_data)
            file.write(data)
        print("Stop")

    def restart(self):
        with open("data/json_data.json", "r") as file:
            json_data = json.load(file)
        jobs = []
        for job in json_data["jobs"]:
            new_job = Job(
                functions[job["task"]],
                job["args"],
                datetime.datetime.strptime(job["start_at"], "%c"),
                job["max_working_time"],
                job["tries"],
            )
            new_job.status = job["status"]
            new_job.result = job["result"]
            new_job.dependencies = []
            jobs.append(new_job)
        # for job in jobs:
        #     for j in json_data["jobs"]:
        #         if j["task"] == job.task.__name__:
        #             o_job = j
        #             break
        #     for g in o_job["dependencies"]:
        #         for i in jobs:
        #             if g == i.task.__name__:
        #                 job.dependencies.append(i)
        #                 break
        #     print(job.dependencies)
        for job in json_data["jobs"]:
            if len(job["dependencies"]) > 0:
                for g in range(len(jobs)):
                    if jobs[g].task.__name__ == job["task"]:
                        new_job = g
                        break
                for dep in job["dependencies"]:
                    for j in jobs:
                        if j.task.__name__ == dep:
                            jobs[new_job].dependencies.append(j)
                            break
        self.jobs = jobs


if __name__ == "__main__":
    jobs = []
    jobs.append(Job(get_weather, ["https://jsonplaceholder.typicode.com/todos/1"]))
    jobs.append(Job(formatting, [jobs[0].result], dependencies=[jobs[0]]))
    jobs.append(Job(print_sum, [jobs[1].result], dependencies=[jobs[1]]))
    jobs.append(Job(os_work))
    jobs.append(Job(write, ["new_dir/newfile.txt", "New"]))
    scheduler = Scheduler(jobs)
    scheduler.restart()
    scheduler.run()