import peewee
from datetime import datetime
from logging import getLogger


logger = getLogger(__name__)

db = peewee.PostgresqlDatabase(
    'queue_db',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5431'
)

IN_QUEUE = 0
RUN = 1
COMPLETED = 2

STATUSES = {
    IN_QUEUE: "In Queue",
    RUN: "Run",
    COMPLETED: "Completed"
}


class Task(peewee.Model):
    status = peewee.IntegerField(default=IN_QUEUE)
    create_time = peewee.DateTimeField(default=datetime.utcnow)
    start_time = peewee.DateTimeField(null=True)
    exec_time = peewee.FloatField(null=True)

    class Meta:
        database = db

    def __repr__(self):
        return f"<Task-{self.id}>"

    def run_task(self):
        logger.info(f"Start the {repr(self)}")
        self.status = RUN
        self.start_time = datetime.now()
        self.save()

    def complete_task(self):
        self.status = COMPLETED
        self.exec_time = (datetime.now() - self.start_time).total_seconds()
        self.save()
        logger.info(f"{repr(self)} is completed.")


def create_db():
    db.create_tables([Task, ])


def delete_db():
    db.drop_tables([Task, ])


def recreate_db():
    delete_db()
    create_db()
