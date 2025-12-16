from flask import Flask
from flask_tryton import Tryton

from importlib import import_module
from logging import DEBUG
from config import config_dict, Config
from decouple import config

from werkzeug.middleware.proxy_fix import ProxyFix


def register_blueprints(app):
    for module_name in ('base', 'home', 'auth', 'download_attachment', 'siro'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

app = Flask(__name__, static_folder='base/static')

app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1,
    x_prefix=1,
)


DEBUG = config('DEBUG', default=True, cast=bool)
get_config_mode = 'Debug' if DEBUG else 'Production'
app_config = config_dict[get_config_mode.capitalize()]
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 3
# app.config['APPLICATION_ROOT'] = '/autogestion'
# app.config['SESSION_COOKIE_PATH'] = '/autogestion'


tryton = Tryton(app, configure_jinja=True)

register_blueprints(app)

