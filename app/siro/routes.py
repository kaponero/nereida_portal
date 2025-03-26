from app import tryton
from app.siro import blueprint
from app.auth.routes import login_required

from flask import render_template, request, Response, jsonify

from datetime import datetime

import qrcode
import io


@blueprint.route('/siro_button/<voucher_id>')
@tryton.transaction()
@login_required
def pay(voucher_id):
    Voucher = tryton.pool.get('delco.subscriptor.voucher')
    Log = tryton.pool.get('delco.cash_logs')
    Invoice = tryton.pool.get('account.invoice')

    voucher = Voucher(voucher_id)

    invoice_date = invoices and invoices[0].invoice_date \
        or datetime.today().date()

    if voucher.state == 'posted':
        if not voucher.invoice:
            Voucher.create_invoice([voucher])
        Voucher.pay_invoice([voucher], datetime.today(), 'siro')
        if voucher.surcharge:
            Voucher.pay_invoice_surcharge([voucher], datetime.today(), 'siro')
            voucher.s_surcharge = voucher.surcharge
            voucher.save()


@blueprint.route('/generate_qr/<voucher_id>', methods=['GET', 'POST'])
@tryton.transaction(readonly=False, user=2)
@login_required
def generate_qr(voucher_id):
    print(20*'*', 'Comienzo de endpoint generate_qr', 20*'*')
    try:
        pool = tryton.pool
        Voucher = pool.get('delco.subscriptor.voucher')

        voucher_id = request.args.get('lineId', type=int)
        amount_to_pay_today = request.args.get('amount_to_pay_today', type=float)

        # Obtener el voucher por su ID
        voucher, = Voucher.search([('id', '=', voucher_id)])

        qr = Voucher.generate_qrs([{
            'voucher': voucher,
            'amount_to_pay_today': amount_to_pay_today
            }])
        print('luego del fetch')
        if qr:
            # Asignar los valores al voucher
            voucher.siro_qr_string = qr[0]['StringQR']
            voucher.siro_qr_hash = qr[0]['Hash']
            voucher.save()  # Guardar los cambios en la base de datos
            # Devolver una respuesta de éxito
            return jsonify({
                "status": "success",
                "message": "QR generado y guardado correctamente",
                "voucher_id": voucher_id,
                "qr_string": voucher.siro_qr_string,
                "qr_hash": voucher.siro_qr_hash
            }), 200
        else:
            # Devolver un error si no se obtuvieron los parámetros del QR
            return jsonify({
                "status": "error",
                "message": "No se pudieron obtener los parámetros del QR"
            }), 400
    except Exception as e:
        # Manejar cualquier excepción y devolver un error
        return jsonify({
            "status": "error",
            "message": f"Error al generar el QR: {str(e)}"
        }), 500

@blueprint.route('/show_qr')
@tryton.transaction()
@login_required
def show_qr():
    pool = tryton.pool
    Voucher = pool.get('delco.subscriptor.voucher')

    voucher_id = request.args.get('line_id')
    size = request.args.get('size', default=1, type=int)

    voucher = Voucher(voucher_id)
    qr_siro = voucher.siro_qr_string
    if qr_siro:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1*float(size),
            border=4,
        )
        qr.add_data(qr_siro)
        qr.make(fit=True)
        # Convertir a imagen
        img = qr.make_image(fill_color="black", back_color="white")
        # Guardar en un buffer para devolverlo como respuesta
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return Response(buffer, mimetype='image/png')
    return "", 404

@blueprint.route('/siro_no_success/<subscriptor_id>')
@tryton.transaction()
@login_required
def siro_no_success(subscriptor_id) :
    pool = tryton.pool
    Subscriptor = pool.get('delco.subscriptor')
    subscriptor = Subscriptor(subscriptor_id)
    return render_template('/siro-pago-no-exitoso.html', subscriptor=subscriptor)

@blueprint.route('/siro_success/<subscriptor_id>')
@tryton.transaction()
@login_required
def siro_success(subscriptor_id) :
    pool = tryton.pool
    Subscriptor = pool.get('delco.subscriptor')
    subscriptor = Subscriptor(subscriptor_id)
    return render_template('/siro-pago-exitoso.html', subscriptor=subscriptor)
