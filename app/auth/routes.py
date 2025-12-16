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
# ==========================
@blueprint.route('/login', methods=['GET', 'POST'])
@tryton.transaction()
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and 'login' in request.form:
        try:
            webuser = WebUser.authenticate(
                form.email.data,
                form.password.data
            )

            session['identified'] = False

            if webuser:
                session['session_key'] = WebUser.new_session(webuser)
                session['identified'] = True

                # Redirección segura
                next_url = request.args.get('next')
                if next_url:
                    return redirect(next_url)

                return redirect(url_for('home_blueprint.index'))

            flash('Correo electrónico o contraseña incorrecta', 'error')

        except Exception:
            flash(
                'Demasiados intentos de ingreso o error interno. '
                'Espere un momento y vuelva a intentar.',
                'error'
            )

    return render_template('login.html', form=form)


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
