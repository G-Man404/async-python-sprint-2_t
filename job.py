import datetime
import time
import os
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool

"""
STATUS CODE
F - Finish
FE - Finish Error
Q - Queue
P - Pause
IP - In progress
"""


class Job:

    def __init__(self, task, args, start_at=datetime.datetime.now(), max_working_time=-1, tries=0, dependencies=[]):
        self.task: callable = task
        self.args: list = args
        self.start_at: datetime.datetime = start_at
        self.max_working_time: int = max_working_time
        self.tries: int = tries
        self.dependencies: list[Job] = dependencies
        self.status: str = "Q"
        self.result: list = []
        self.iter = self.run()

    def run(self):
        pool = ThreadPool(processes=1)
        thread = pool.apply_async(self.task, self.args)
        start_time = datetime.datetime.now()
        self.status = "IP"
        while thread.ready():
            if self.max_working_time == -1 or\
                    datetime.datetime.now() < start_time + datetime.timedelta(seconds=self.max_working_time):
                self.tries -= 1
                self.status = "P"
                break
            yield
        self.result.append(thread.get())
        self.status = "F"
