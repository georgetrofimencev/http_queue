from aiohttp import web
from src.api.routers import routers
from src.queue_worker import Worker


def start_app():
    app = web.Application()
    app.add_routes(routers)
    worker = Worker()
    worker.start_work()
    app["worker"] = worker
    return app
