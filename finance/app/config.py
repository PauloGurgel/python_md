import logging
import os


basedir = os.path.abspath(os.path.dirname(__file__))
logger = logging.getLogger('iclinic_finance')


class Config:
    SECRET_KEY = os.environ.get('CSRF_SECRET_KEY') or 'f0e0b374-5912-4e31-bb1b-d6bda7a707b6'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CONSULTATION_CLOSED_EVENT_TOPIC = 'iclinic.consultation.ConsultationClosed'
    APPOINTMENT_CREATED_EVENT_TOPIC = 'iclinic.finance.AppointmentCreated'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    KAFKA_BROKER_URI = os.environ.get('KAFKA_BROKER_URI')

    @staticmethod
    def init_app(app):
        # protected? method
        pass

    @classmethod
    def validate(cls, environment):
        if environment is not None:
            environment = environment.lower()
        return environment in profile.keys()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_correct_mysql_uri(cls):
        env = os.environ.get('FLASK_ENV')
        appcfg = profile[env]
        uri = appcfg.SQLALCHEMY_DATABASE_URI
        logger.info(f"URL for {env} was required {uri}")
        return uri


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class PresentationConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


profile = {
    'development': DevelopmentConfig(),
    'testing': TestingConfig(),
    'presentation': PresentationConfig(),
    'default': DevelopmentConfig()
}
