from app import create_app
from app.adapters.listener import run_kafka_listener

app = create_app()

if __name__ == '__main__':
    run_kafka_listener()
    app.run(port=5001)
