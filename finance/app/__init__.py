import logging
import os
from datetime import date, datetime
from decimal import Decimal

from flask import Flask
from flask.json import JSONEncoder

from app.config import Config, profile


logger = logging.getLogger('iclinic_finance')


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
    logger.info(f'Profile {type(appcfg)} and URI: {appcfg.SQLALCHEMY_DATABASE_URI}')

    appcfg.init_app(app)
    app.json_encoder = CustomJSONEncoder

    from app.adapters import orm
    orm.start_mappers()

    from app.views import views
    app.register_blueprint(views.main_views)

    return app


