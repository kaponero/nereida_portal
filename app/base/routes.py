from flask import (render_template, redirect, request, url_for,
            flash, session, send_file, jsonify)

from app import tryton

from .forms import ChangePasswordForm

from app.base import blueprint

from app.auth.routes import login_required

from app.download_attachment.routes import download_report

from trytond.transaction import Transaction


@blueprint.route('/admin')
def admin():
    return render_template('/admin_index.html')

@blueprint.route('/admin/abonados')
def abonados():
    return render_template('/admin_abonados.html')

@blueprint.route('/index')
@tryton.transaction()
@login_required
def formulario():
    Subscriptor = tryton.pool.get('delco.subscriptor')
    Session = tryton.pool.get('web.user.session')
    user = Session.get_user(session['session_key'])
    if Subscriptor.search([('web_user', '=', user)]):
        with Transaction().set_context(company=1):
            subscriptor, = Subscriptor.search([('web_user', '=', user)])
        return render_template('/index.html', subscriptor=subscriptor)
    return render_template('page-500.html'), 500

@blueprint.route('/download_ticket/<id>')
@tryton.transaction()
@login_required
def download_ticket(id):
    Voucher = tryton.pool.get('delco.subscriptor.voucher')
    voucher = Voucher(id)
    if voucher.state == 'paid':
        return download_report('delco.create_voucher_ticket.report', 'comprobante', id)
    else:
        with Transaction().set_context(company=1):
            return download_report('delco.create_voucher.report', 'comprobante', id)
    return render_template('page-500.html'), 500

@blueprint.route('/comprobantes')
@tryton.transaction(user=1)
@login_required
def comprobantes():
    Subscriptor = tryton.pool.get('delco.subscriptor')
    Session = tryton.pool.get('web.user.session')
    user = Session.get_user(session['session_key'])
    if Subscriptor.search([('web_user', '=', user)]):
        with Transaction().set_context(company=1):
            subscriptor, = Subscriptor.search([('web_user', '=', user)])
            return render_template('/comprobantes.html', subscriptor=subscriptor)
    return render_template('page-500.html'), 500


@blueprint.route('/perfil')
@tryton.transaction()
@login_required
def perfil():
    Subscriptor = tryton.pool.get('delco.subscriptor')
    Session = tryton.pool.get('web.user.session')
    user = Session.get_user(session['session_key'])

    if Subscriptor.search([('web_user', '=', user)]):
        with Transaction().set_context(company=1):
            subscriptor, = Subscriptor.search([('web_user', '=', user)])
            return render_template('/perfil.html', subscriptor=subscriptor)
    return render_template('page-500.html'), 500


@blueprint.route('/notificaciones')
@tryton.transaction()
@login_required
def notificaciones():
    Subscriptor = tryton.pool.get('delco.subscriptor')
    Session = tryton.pool.get('web.user.session')
    user = Session.get_user(session['session_key'])

    if Subscriptor.search([('web_user', '=', user)]):
        with Transaction().set_context(company=1):
            subscriptor, = Subscriptor.search([('web_user', '=', user)])
            return render_template('/notificaciones.html', subscriptor=subscriptor)
    return render_template('page-500.html'), 500


@blueprint.route('/seguridad', methods = ['GET','POST'])
@tryton.transaction()
@login_required
def seguridad():
    WebUser = tryton.pool.get('web.user')
    Session = tryton.pool.get('web.user.session')
    Subscriptor = tryton.pool.get('delco.subscriptor')
    change_password_form = ChangePasswordForm(request.form)
    user = Session.get_user(session['session_key'])
    web_user = WebUser(user)

    if Subscriptor.search([('web_user', '=', user)]):
        with Transaction().set_context(company=1):
            subscriptor, = Subscriptor.search([('web_user', '=', user)])
            if request.method == 'POST' \
                and WebUser.authenticate(
                    web_user.email,
                    change_password_form.password.data) \
                and change_password_form.new_password.data == \
                        change_password_form.password_confirmation.data:
                # aquí el cambio de contraseña por tryton
                flash('La contraseña ha sido exitosamente actualizada', 'success')
                web_user.password = change_password_form.new_password.data
                web_user.save()
                return render_template('/contrasenia.html', subscriptor=subscriptor)
            elif request.method == 'POST':
                flash('Las contraseñas no coinciden', 'error')
            return render_template('/seguridad.html', subscriptor=subscriptor,
                    form=change_password_form)
    return render_template('page-500.html'), 500
