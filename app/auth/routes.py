from flask import render_template, redirect, request, url_for, flash, session

from app import tryton
from app.auth import blueprint
#from app.base import blueprint as base_blueprint

from .forms import LoginForm

from functools import wraps

WebUser = tryton.pool.get('web.user')
Session = tryton.pool.get('web.user.session')

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_key = None
        if 'session_key' in session:
            session_key = session['session_key']
        user = Session.get_user(session_key)
        if not user:
            return redirect(url_for('auth_blueprint.login', next=request.path))
        return func(*args, **kwargs)
    return wrapper

@blueprint.route('/login', methods=['GET', 'POST'])
@tryton.transaction()
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        #request.method == 'POST' and login_form.validate_on_submit():
        try:
            webuser = WebUser.authenticate(login_form.email.data, login_form.password.data)
            session['identified'] = False
            if webuser:
                session['session_key'] = WebUser.new_session(webuser)
                session['identified'] = True
                return redirect(url_for('home_blueprint.index'))
            flash('Verifique sus credenciales', 'error')
            return render_template( 'login.html',
                    msg='Correo electrónico o contraseña incorrecta', form=login_form)
        except:
            return 'Demasiados intentos de ingreso o algun otro error. Espere un momento y vuelvalo a intentar'
    return render_template('login.html', form=login_form)

# Logout
@login_required
@blueprint.route('/logout')
@tryton.transaction(readonly=False)
def logout():
    if session['session_key']:
        Session.delete(Session.search(
                ('key', '=', session['session_key']),
                ))
        session.pop('session_key', None)
        session.pop('identified', None)
        flash("Se ha desconectado tu sesión", 'success')
    return redirect(url_for('auth_blueprint.login'))
