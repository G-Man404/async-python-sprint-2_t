import datetime
import json
import sys
import job
from dataclasses import dataclass


class Scheduler:
    def __init__(self, tasks: list[Task], pool_size: int = 10):
        self.tasks = tasks
        self.pool_size = pool_size

