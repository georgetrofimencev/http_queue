import unittest
from src.db import Task, RUN, COMPLETED, IN_QUEUE, db


class TestTaskCase(unittest.TestCase):
    def setUp(self):
        db.connect()
        db.create_tables([Task, ])

    def tearDown(self):
        db.drop_tables([Task, ])

    def test_running_task_cycle(self):
        task = Task()
        task.save()
        self.assertEqual(task.status, IN_QUEUE)
        self.assertIsNone(task.start_time)
        self.assertIsNone(task.start_time)
        self.assertIsNone(task.exec_time)
        task.run_task()
        self.assertEqual(task.status, RUN)
        self.assertIsNone(task.exec_time)
        self.assertIsNotNone(task.start_time)
        task.complete_task()
        self.assertEqual(task.status, COMPLETED)
        self.assertIsNotNone(task.exec_time)


if __name__ == '__main__':
    unittest.main()
