from flask import (render_template, redirect, request, url_for,
            flash, session, send_file, jsonify, Response)

from .forms import ChangePasswordForm

from app import tryton
from app.base import blueprint
from app.auth.routes import login_required
from app.download_attachment.routes import download_report

from trytond.transaction import Transaction

import qrcode
import io


@tryton.default_context
def default_context():
    User = tryton.pool.get('res.user')
    return User.get_preferences(context_only=True)

@blueprint.route('/admin')
def admin():
    return render_template('/admin_index.html')

@blueprint.route('/admin/abonados')
def abonados():
    return render_template('/admin_abonados.html')

# @blueprint.route('/index')
# @tryton.transaction()
# @login_required
# def formulario():
#     Subscriptor = tryton.pool.get('delco.subscriptor')
#     Session = tryton.pool.get('web.user.session')
#     user = Session.get_user(session['session_key'])
#     if Subscriptor.search([('web_user', '=', user)]):
#         with Transaction().set_context(company=1):
#             subscriptor, = Subscriptor.search([('web_user', '=', user)])
#         return render_template('/index.html', subscriptor=subscriptor)
#     return render_template('page-500.html'), 500

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


@blueprint.route('/seguridad', methods=['GET', 'POST'])
@tryton.transaction()
@login_required
def seguridad():
    WebUser = tryton.pool.get('web.user')
    Session = tryton.pool.get('web.user.session')
    Subscriptor = tryton.pool.get('delco.subscriptor')

    form = ChangePasswordForm(request.form)

    user_id = session.get('session_key')
    user = Session.get_user(user_id)
    web_user = WebUser(user)

    # Verificamos que exista subscriptor
    subscriptors = Subscriptor.search([('web_user', '=', user)])
    if not subscriptors:
        return render_template('page-500.html'), 500

    with Transaction().set_context(company=1):
        subscriptor, = subscriptors

        if request.method == 'POST':

            if not form.validate():
                flash('Formulario inválido', 'error')
                return redirect(url_for('base_blueprint.seguridad'))

            if not WebUser.authenticate(
                    web_user.email,
                    form.password.data):
                flash('La contraseña actual es incorrecta', 'error')
                return redirect(url_for('base_blueprint.seguridad'))

            if form.new_password.data != form.password_confirmation.data:
                flash('Las contraseñas no coinciden', 'error')
                return redirect(url_for('base_blueprint.seguridad'))

            # Cambio de contraseña
            web_user.password = form.new_password.data
            web_user.save()

            flash('La contraseña ha sido exitosamente actualizada', 'success')
            return redirect(url_for('base_blueprint.seguridad'))

        # GET
        return render_template(
            'contrasenia.html',
            subscriptor=subscriptor,
            form=form
        )

@blueprint.route('/get_multipago_qr/<subscriptor_id>')
@tryton.transaction()
@login_required
def get_multipago_qr(subscriptor_id):
    Subscriptor = tryton.pool.get('delco.subscriptor')
    subscriptor, = Subscriptor.search([('id', '=', subscriptor_id)], limit=1)
    if subscriptor.qr_multipago:
        qr_multipago = subscriptor.qr_multipago
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=4,
        )
        qr.add_data(qr_multipago)
        qr.make(fit=True)
        # Convertir a imagen
        img = qr.make_image(fill_color="black", back_color="white")
        # Guardar en un buffer para devolverlo como respuesta
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return Response(buffer, mimetype='image/png')
    return "QR no encontrado", 404

@blueprint.route('/equipos')
@tryton.transaction(user=1)
@login_required
def equipos():
    Subscriptor = tryton.pool.get('delco.subscriptor')
    Session = tryton.pool.get('web.user.session')

    user = Session.get_user(session['session_key'])

    subs = Subscriptor.search([('web_user', '=', user)])
    if not subs:
        return jsonify({'error': 'Subscriptor no encontrado'}), 404

    with Transaction().set_context(company=1):
        sub = subs[0]

        return render_template(
            'equipos.html',
            subscriptor=sub,
            equipos=sub.equipments
        )