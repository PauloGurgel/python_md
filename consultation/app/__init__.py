import os
import logging
from datetime import date, datetime
from decimal import Decimal

from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic
from flask import Flask
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy

from app.config import Config, profile


logger = logging.getLogger('iclinic_consultation')
db = SQLAlchemy()


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()

            if isinstance(obj, datetime):
                return obj.isoformat()

            if isinstance(obj, Decimal):
                return '{0:.2f}'.format(obj)

            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def create_kafka_topics():
    logger.info(f"Creating topics on {Config.KAFKA_BROKER_URI}")
    admin_client = AdminClient({
        "bootstrap.servers": Config.KAFKA_BROKER_URI
    })

    topic_list = [NewTopic(Config.CONSULTATION_CLOSED_EVENT_TOPIC, 1, 1),
                  NewTopic(Config.APPOINTMENT_CREATED_EVENT_TOPIC, 1, 1)]
    fs = admin_client.create_topics(topic_list)

    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            logger.info("Topic {} created".format(topic))
        except Exception as e:
            logger.info("Failed to create topic {}: {}".format(topic, e))
    logger.info(f'{topic_list} should be created by now')


def create_app(config_profile='') -> Flask:
    if config_profile == '':
        environment = os.environ.get('FLASK_ENV')
        if not Config.validate(environment):
            environment = 'default'
    else:
        environment = config_profile

    app = Flask(__name__)
    appcfg = profile[environment]
    app.config.from_object(appcfg)
    appcfg.init_app(app)
    db.init_app(app)

    logger.info(f'Profile {type(appcfg)} and URI: {appcfg.SQLALCHEMY_DATABASE_URI}')
    app.json_encoder = CustomJSONEncoder

    from app.adapters import orm
    orm.start_mappers()

    from app.views import views
    app.register_blueprint(views.main_views)

    create_kafka_topics()

    return app
