import peewee
from aiohttp import web
from src.db import Task, STATUSES


class CreateNewTaskHandler(web.View):
    async def get(self):
        task = Task.create()
        task.save()
        self.request.app["worker"].add_task(task)
        return web.json_response(data={
            'task_id': task.id
        })


class GetTaskInfoHandler(web.View):
    async def get(self):
        id = self.request.rel_url.query['id']
        try:
            task = Task.get(Task.id == int(id))
            result = {
                "task_id": task.id,
                "start_time": str(task.start_time),
                "time_to_execution": task.exec_time,
                "create_time": str(task.start_time),
                "status": STATUSES.get(task.status)
            }
            return web.json_response(result)
        except peewee.DoesNotExist:
            return web.json_response(
                {"message": "Task does not exists"}
            )
