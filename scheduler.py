import datetime
import json
import sys
import job


class Scheduler:
    def __init__(self, pool_size: int = 10) -> None:
        self.pool_size = pool_size
        self.tasks = []
        self.tasks_in_progress = []

    def run(self):
        while True:
            if len(self.tasks) > 0:
                if len(self.tasks_in_progress) < self.pool_size:
                    for task in self.tasks:
                        if task.start_at < datetime.datetime.now():
                            self.tasks_in_progress.append(task)
                            self.tasks.remove(task)
                            self.tasks_in_progress[-1].run()
            else:
                print("All tasks are completed")
                self.stop()

    def restart(self):
        with open("data/tasks.json", "r") as file:
            json_data = json.load(file)
            self.tasks = json_data["tasks"]
            self.tasks_in_progress = json_data["tasks_in_progress"]
        self.run()

    def stop(self):
        if len(self.tasks) > 0:
            with open("data/tasks.json", "w") as file:
                json.dump({"tasks": self.tasks, "tasks_in_progress": self.tasks_in_progress}, file)
        sys.exit(0)


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.tasks.append(job.Job(print, "123", datetime.datetime.now()))
    scheduler.run()
