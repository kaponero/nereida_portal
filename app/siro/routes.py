from app import tryton
from app.siro import blueprint
from app.auth.routes import login_required

from flask import render_template, request, Response, jsonify, abort

from datetime import datetime

import qrcode
import io

import hashlib
import hmac
import os


SECRET_KEY = os.environ.get('SIRO_SECRET_KEY')


def generar_hmac(id_referencia):
    message = f"{id_referencia}{SECRET_KEY}".encode()
    return hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).hexdigest()


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

@blueprint.route('/siro_success/<voucher_id>', methods=['GET', 'POST'])
@tryton.transaction(readonly=False, user=2)
def handle_success(voucher_id) :
    pool = tryton.pool
    Voucher = pool.get('delco.subscriptor.voucher')

    data = request.json # El payload que viene de la API
    data_requests = request.args
    print("Pago exitoso recibido: ", data, data_requests)

    voucher = Voucher(voucher_id)
    subscriptor = voucher.subscriptor
    print('Esperando pago')
    # Validación del hmac (para POST, o sea, la billetera)
    if request.method == 'POST':
        '''
        Chequear que el hmac sea correcto y no chamuyo
        '''
        hmac_recibido = request.args.get('hmac')
        id_referencia = voucher.siro_IdReferenciaOperacion
        print('SECRET_KEY: ', SECRET_KEY)
        print('hmac: ', hmac_recibido)
        print('generar_hmac: ', generar_hmac(id_referencia))
        data = request.json
        print('data: ', data)
        id_resultado = data['id_resultado']
        print('id_resultado: ', id_resultado)
        if not hmac_recibido or not hmac.compare_digest(
            generar_hmac(id_referencia),
            hmac_recibido
            ):
            abort(403, "Firma inválida")

            ''''
            Cambiar el estado del cupón, la fecha de transacción,
            y el metodo de pago
            '''
        paid_date = datetime.today().date
        if voucher.state != 'paid':
            voucher.state = 'processing_payment'
            voucher.pay_method = 'qr_siro'
            voucher.save()

        return jsonify({"status": "OK"}), 200
        '''
        Redirección para GET (desde la página del QR)
        '''
    elif request.method == 'GET':
        print('pago exitoso')
        return render_template('/siro-pago-exitoso.html',
            subscriptor=subscriptor, voucher=voucher)


@blueprint.route('/siro_no_success/voucher_id', methods=['POST'])
@tryton.transaction()
@login_required
def siro_no_success(voucher_id) :
    pool = tryton.pool
    Voucher = pool.get('delco.subscriptor.voucher')
    voucher = Voucher(voucher_id)
    subscriptor = voucher.subscriptor
    return render_template('/siro-pago-no-exitoso.html',
            subscriptor=subscriptor, voucher=voucher)


@blueprint.route('/verificar_pago')
@tryton.transaction()
@login_required
def verficar_pago():
    pool = tryton.pool
    Voucher = pool.get('delco.subscriptor.voucher')
    voucher_id = request.args.get('id')
    estado = 'EN ESPERA'
    voucher = Voucher(voucher_id)
    if voucher.state == 'processing_payment':
        estado = "APROBADO"
    return jsonify({"estado": estado}), 200
