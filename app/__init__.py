from flask import Flask, request, g
from flask_tryton import Tryton

from importlib import import_module
from logging import DEBUG
from config import config_dict, Config
from decouple import config

from werkzeug.middleware.proxy_fix import ProxyFix

import secrets


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

# Generamos el token para nonce del CSP
@app.before_request
def generate_csp_nonce():
    g.csp_nonce = secrets.token_urlsafe(16)

# Inyectamos el nonce en nuestras plantillas
# con {{ csp_nonce}}
@app.context_processor
def inject_csp_nonce():
    return {
        'csp_nonce': getattr(g, 'csp_nonce', '')
    }

@app.after_request
def apply_response_headers(response):
    path = request.path
    nonce = getattr(g, 'csp_nonce', '')

    # =========================
    # Cache-Control
    # =========================
    if '/static/' in path:
        # Assets versionados → cache fuerte
        response.headers['Cache-Control'] = (
            'public, max-age=31536000, immutable'
        )
    else:
        # HTML / JSON / dinámico → nunca cachear
        response.headers['Cache-Control'] = (
            'no-store, no-cache, must-revalidate, max-age=0'
        )
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

    # =========================
    # Content Security Policy
    # =========================
    response.headers['Content-Security-Policy-Report-Only'] = (
        "default-src 'self'; "
        "base-uri 'self'; "
        "frame-ancestors 'self'; "

        "script-src 'self' "
        f"'nonce-{nonce}' "
        "https://cdn.jsdelivr.net "
        "https://unpkg.com "
        "https://code.jquery.com "
        "https://static.cloudflareinsights.com; "

        "style-src 'self' 'unsafe-inline' "
        "https://cdn.jsdelivr.net "
        "https://fonts.googleapis.com; "

        "font-src 'self' "
        "https://cdn.jsdelivr.net "
        "https://fonts.gstatic.com; "

        "img-src 'self' data:; "

        "connect-src 'self' "
        "https://static.cloudflareinsights.com;"
    )

    return response
