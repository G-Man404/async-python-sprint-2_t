import datetime
import time
import os
from multiprocessing import Process


class Job:
    def __init__(self, task, args, start_at=datetime.datetime.now(), max_working_time=-1, tries=0, dependencies=[]):
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies
        self.task = task
        self.args = args
        self.status = "W"

    def dependency_completed(self):
        status = True
        for task in self.dependencies:
            if not task.status:
                status = False
        return status

    def run(self):
        if self.tries >= 0:
            if not self.dependency_completed():
                self.tries -= 1
                raise "dependency_error"
            self.status = "P"
            process = Process(target=self.task, args=(self.args, ))

            start_time = datetime.datetime.now()
            process.start()

            while process.is_alive():
                if datetime.datetime.now() > start_time+datetime.timedelta(seconds=self.max_working_time) and\
                        self.max_working_time > 0:
                    process.terminate()
                    raise TimeoutError
            self.status = "C"
        else:
            self.status = "F"
            raise "amount_attempts"
