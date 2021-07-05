from datetime import datetime
from time import sleep

from app import create_app
from app.adapters.listener import run_kafka_listener
from app.adapters.logger_context import configura_logger

logger = configura_logger()

logger.info("Before sleep")
sleep(22)  # Extra seconds waiting for topic creation after consultation
logger.info("After sleep - creating app")

app = create_app()

logger.info("Starting app")
run_kafka_listener()

if __name__ == '__main__':
    logger.info("Application starting")
    app.run(port=5001)
