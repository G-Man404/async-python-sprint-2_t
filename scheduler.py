import datetime
import json
import sys
import job
from dataclasses import dataclass


@dataclass
class Task:
    task: callable
    args: list = list
    start_at: datetime.datetime = datetime.datetime.now()
    max_working_time: int = -1
    tries: int = 0
    dependencies: list = list
    status: str = "Queue"
    result: list = list


class Scheduler:
    def __init__(self, tasks: list[Task], pool_size: int = 10):
        self.tasks = tasks
        self.pool_size = pool_size

