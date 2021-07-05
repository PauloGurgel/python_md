from time import sleep

from app import create_app
from app.adapters.logger_context import configura_logger

logger = configura_logger()

logger.info("Before sleep")
sleep(20)  # Wait for kafka to be ready to receive messages using provided docker composer
logger.info("After sleep - creating app")


app = create_app()

logger.info("Starting app")

if __name__ == '__main__':
    app.run()
