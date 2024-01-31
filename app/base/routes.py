from flask import (render_template, redirect, request, url_for,
            flash, session, send_file, jsonify)

from app import tryton
from app.base import blueprint
from app.auth.routes import login_required
from app.download_attachment.routes import download_report
from trytond.transaction import Transaction

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
    return render_template('/notificaciones.html')


@blueprint.route('/seguridad')
@tryton.transaction()
@login_required
def seguridad():
    Subscriptor = tryton.pool.get('delco.subscriptor')
    Session = tryton.pool.get('web.user.session')
    user = Session.get_user(session['session_key'])
    
    if Subscriptor.search([('web_user', '=', user)]):
        with Transaction().set_context(company=1):
            subscriptor, = Subscriptor.search([('web_user', '=', user)])
            return render_template('/seguridad.html', subscriptor=subscriptor)
    return render_template('page-500.html'), 500
    
