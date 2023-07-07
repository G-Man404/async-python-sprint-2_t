import datetime
import time
import os
from multiprocessing import Process
import scheduler


class Job:
    def run(self):
        task = yield
        try:
            task.result = task.task(task.args)
        except:
            task.tries -= 1