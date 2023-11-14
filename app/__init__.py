from flask import Flask

from importlib import import_module
from logging import DEBUG
from config import config_dict, Config
from decouple import config


def register_blueprints(app):
    for module_name in ('base', 'home', 'auth'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

app = Flask(__name__, static_folder='base/static')

DEBUG = config('DEBUG', default=True, cast=bool)
get_config_mode = 'Debug' if DEBUG else 'Production'
app_config = config_dict[get_config_mode.capitalize()]
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 3

register_blueprints(app)

