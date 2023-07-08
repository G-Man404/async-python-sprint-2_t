import datetime
import time
import os
from multiprocessing import Process
from threading import Thread
import scheduler


class Job:

    def __init__(self, task, args, start_at=datetime.datetime.now(), max_working_time=-1, tries=0, dependencies=list):
        self.task: callable = task
        self.args: list = args
        self.start_at: datetime.datetime = start_at
        self.max_working_time: int = max_working_time
        self.tries: int = tries
        self.dependencies: list = dependencies
        self.status: str = "Queue"
        self.result: list = list

    def run(self):
        thread = Thread(target=self.task, args=self.args)
        start_time = datetime.datetime.now()
        thread.start()
        while thread.is_alive():
            if self.max_working_time == -1 or\
                    datetime.datetime.now() < start_time + datetime.timedelta(seconds=self.max_working_time):
                self.tries -= 1
                break
            yield
        self.result = thread
        self.status = "F"
