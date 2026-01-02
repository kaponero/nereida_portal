from flask import (
    render_template,
    redirect,
    request,
    url_for,
    flash,
    session
)

from functools import wraps

from app import tryton
from app.auth import blueprint
from .forms import LoginForm

from urllib.parse import urlparse, urljoin

@tryton.default_context
def default_context():
    User = tryton.pool.get('res.user')
    return User.get_preferences(context_only=True)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


WebUser = tryton.pool.get('web.user')
Session = tryton.pool.get('web.user.session')


# ==========================
# Decorador login_required
# ==========================
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_key = session.get('session_key')
        user = Session.get_user(session_key)

        if not user:
            return redirect(
                url_for(
                    'auth_blueprint.login',
                    next=request.full_path
                )
            )
        return func(*args, **kwargs)
    return wrapper


# ==========================
# Login
@blueprint.route('/login', methods=['GET', 'POST'])
@tryton.transaction()
def login():
    login_form = LoginForm(request.form)

    # 🔁 next puede venir por GET o POST
    next_page = next_page = (
                request.args.get('next')
                or request.form.get('next')
                or request.headers.get('X-Original-URI')
                or url_for('home_blueprint.index')
                )

    if request.method == 'POST' and 'login' in request.form:
        try:
            webuser = WebUser.authenticate(
                login_form.email.data,
                login_form.password.data
            )

            if webuser:
                session['session_key'] = WebUser.new_session(webuser)
                session['identified'] = True

                return redirect(url_for('home_blueprint.index'))
                # # 🔐 Redirección segura
                # # TODO reparar esto para que vaya siempre al subpath
                # if not next_page or not is_safe_url(next_page):
                #     next_page = url_for('home_blueprint.index')
                # 
                # return redirect(next_page)

            # ❌ Login incorrecto
            flash('Verifique sus credenciales', 'error')

        except Exception as e:
            flash(
                'Demasiados intentos de ingreso o error interno',
                'error'
            )

    return render_template(
        'login.html',
        form=login_form,
        next=next_page
    )

# ==========================
# Logout
# ==========================
@login_required
@blueprint.route('/logout')
@tryton.transaction(readonly=False)
def logout():
    session_key = session.get('session_key')
    if session_key:
        Session.delete(Session.search(
                ('key', '=', session['session_key']),
                ))
        session.pop('session_key', None)
        session.pop('identified', None)
        flash("Se ha desconectado tu sesión", 'success')
    return redirect(url_for('auth_blueprint.login'))
