from aiohttp import web
from .handlers import CreateNewTaskHandler, GetTaskInfoHandler

routers = [
    web.get('/create', CreateNewTaskHandler),
    web.get('/task', GetTaskInfoHandler),
]
