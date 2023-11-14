from flask import render_template, redirect, request, url_for, flash, session

from app.auth import blueprint
from app.base import blueprint as base_blueprint

from .forms import LoginForm

from functools import wraps

"""
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
    Jury = tryton.pool.get('aet_web.jury')
    Invitation = tryton.pool.get('aet_web.invitation')
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        #request.method == 'POST' and login_form.validate_on_submit():
        try:
            webuser = WebUser.authenticate(login_form.email.data, login_form.password.data)
            session['identified'] = False
            if webuser:
                session['session_key'] = WebUser.new_session(webuser)
                session['identified'] = True
                ''' Si el usuario es jurado, regresamos la lista de categorias '''
                jury = Jury.search([('web_user', '=', webuser)])
                invitation = Invitation.search([('web_user', '=', webuser)])
                if jury and invitation:
                    return redirect(url_for('base_blueprint.lista_o_reserva'))
                if jury:
                    return redirect(url_for('base_blueprint.show_category'))
                ''' Si el usuario es para comprar invitaciones, regresamos a la parte de invitaciones'''
                if invitation:
                    return redirect(url_for('base_blueprint.listado_reserva'))
            flash('Verifique sus credenciales', 'error')
            return render_template( 'login.html', msg='Correo electrónico o contraseña incorrecta', form=login_form)
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
"""