from src.api.create_app import start_app
from aiohttp import web
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


app = start_app()

if __name__ == '__main__':
    web.run_app(app)
