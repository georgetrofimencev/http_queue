import random
import time
from queue import Empty
from src.db import Task, IN_QUEUE, RUN
from multiprocessing import Queue, Process
from threading import Thread
from logging import getLogger


logger = getLogger(__name__)


def do_some_work():
    time.sleep(random.randint(1, 10))


class Worker:
    def __init__(self):
        self.queue = Queue()
        self.thread = Thread(target=self.process_tasks)
        self.is_busy = False

    def add_task(self, task):
        logger.info(f"Worker got the task {task}")
        self.queue.put(task)

    def process_tasks(self):
        while True:
            try:
                if not self.is_busy:
                    task = self.queue.get_nowait()
                    if task:
                        self.is_busy = True
                        process = Process(target=do_some_work)
                        task.run_task()
                        process.start()
                        process.join()
                        task.complete_task()
                        self.is_busy = False
            except Empty:
                time.sleep(.1)
            except KeyboardInterrupt:
                self.stop_work()

    def start_work(self):
        query = (Task.select()
                 .where((Task.status == IN_QUEUE) | (Task.status == RUN))
                 .order_by(Task.create_time))
        for task in query:
            self.add_task(task)
        self.thread.start()
        logger.info('Worker started')

    def stop_work(self):
        self.thread.join()
