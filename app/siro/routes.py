from app import tryton
from app.siro import blueprint
from app.auth.routes import login_required

from flask import render_template, request, Response, jsonify, abort, make_response

from trytond.transaction import Transaction
from datetime import datetime
from decimal import Decimal

import qrcode
import io
import json
import hashlib
import hmac
import os


SECRET_KEY = os.environ.get('SIRO_SECRET_KEY')


def generar_hmac(id_referencia):
    message = f"{id_referencia}{SECRET_KEY}".encode()
    return hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).hexdigest()

def log_response():
    response_data = {"status": "success"}
    response = make_response(json.dumps(response_data))
    raw_response = f"HTTP {response.status_code}\n"
    raw_response += "\n".join([f"{k}: {v}" for k, v in response.headers.items()])
    raw_response += f"\n\n{response.data.decode('utf-8')}"
    return raw_response

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
    pool = tryton.pool
    Voucher = pool.get('delco.subscriptor.voucher')
    Log = pool.get('delco.siro.log')

    # Comenzamos con el log
    log = Log.log_request(request)
    log.raw_response = log_response()
    log.date = datetime.now()
    log.status = 'generating'
    log.save()

    try:
        voucher_id = request.args.get('lineId', type=int)
        amount_to_pay_today = request.args.get('amount_to_pay_today', type=float)
        log.amount = Decimal(amount_to_pay_today)
        log.save()

        # Obtener el voucher por su ID
        voucher, = Voucher.search([('id', '=', voucher_id)])

        log.voucher = voucher
        log.subscriptor = log.on_change_with_subscriptor()
        log.save()

        qr = Voucher.generate_siro_qrs([{
            'voucher': voucher,
            'amount_to_pay_today': amount_to_pay_today
            }])
        if qr:
            # Asignar los valores al voucher
            voucher.siro_qr_string = qr[0]['StringQR']
            voucher.siro_qr_hash = qr[0]['Hash']
            voucher.save()  # Guardar los cambios en la base de datos

            log.siro_qr_hash = voucher.siro_qr_hash
            log.siro_IdReferenciaOperacion = voucher.siro_IdReferenciaOperacion
            log.siro_hmac = voucher.siro_hmac
            log.status = 'generated'
            log.save()

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
            log.status = 'error'
            log.error_message = "No se pudieron obtener los parámetros del QR"
            log.save()
            return jsonify({
                "status": "error",
                "message": "No se pudieron obtener los parámetros del QR"
            }), 400
    except Exception as e:
        # Manejar cualquier excepción y devolver un error
        log.status = 'error'
        log.error_message = f"Error al generar el QR: {str(e)}"
        log.save()
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
    Log = pool.get('delco.siro.log')

    data_requests = request.args
    print("Pago exitoso recibido: ", data_requests)

    voucher = Voucher(voucher_id)
    subscriptor = voucher.subscriptor
    print('Esperando pago')
    hmac_recibido = request.args.get('hmac', None)
    hmac_tryton = voucher.siro_hmac

    id_referencia = request.args.get('IdReferenciaOperacion', None)
    id_referencia_tryton = voucher.siro_IdReferenciaOperacion

    id_resultado = request.args.get('IdResultado', None)
    print(request.args)

    # Comenzamos con el log
    log = Log.log_request(request)
    log.raw_response = log_response()
    log.voucher = voucher.id
    log.subscriptor = log.on_change_with_subscriptor()
    log.date = datetime.now()
    log.status = 'pending'
    log.siro_qr_hash = hmac_recibido
    log.siro_IdReferenciaOperacion = id_referencia
    log.siro_IdResultado = id_resultado
    log.save()

    # Validación del hmac (para POST, o sea, la billetera)
    if  hmac_recibido and id_resultado \
        and hmac_recibido == hmac_tryton \
        and id_referencia == id_referencia_tryton:
        '''
        Chequear que el hmac sea correcto y no chamuyo
        '''
        if not hmac_recibido or not hmac.compare_digest(
            generar_hmac(id_referencia),
            hmac_recibido
            ):
            log.status = 'error'
            log.error_message("403, Firma inválida")
            log.save()
            print('abortado')
            abort(403, "Firma inválida")

        ''''
        Cambiar el estado del cupón, la fecha de transacción,
        y el metodo de pago
        '''
        paid_date = datetime.today().date
        if voucher.state not in [
            'paid', 'processing_payment', 'process_payment_ok']:
            print('cambiando de estado al cupon')
            voucher.state = 'processing_payment'
            voucher.pay_method = 'qr_siro'
            voucher.siro_IdResultado = id_resultado
            voucher.save()

        if voucher.state == 'processing_payment':
            Voucher.check_siro_payments([voucher])
        if voucher.state == 'process_payment_ok':
            log.status = 'paid'
            log.save()
        else:
            log.status = 'error'
            log.error_message = "No se pudo concretar la corroboración del pago"
            log.save()

        return jsonify({"status": "OK"}), 200

    else:
        '''
        Redirección desde la página del QR
        '''
        print('pago exitoso')
        log.status = "Redirecting OK"
        log.save()
        return render_template('/siro-pago-exitoso.html',
            subscriptor=subscriptor, voucher=voucher)


@blueprint.route('/siro_no_success/<voucher_id>')
@tryton.transaction(readonly=False, user=2)
def siro_no_success(voucher_id) :
    pool = tryton.pool
    Voucher = pool.get('delco.subscriptor.voucher')
    Log = pool.get('delco.siro.log')

    voucher = Voucher(voucher_id)

    hmac_recibido = request.args.get('hmac', None)
    id_referencia = voucher.siro_IdReferenciaOperacion

    log = Log.log_request(request)
    log.raw_response = log_response()
    log.voucher = voucher.id
    log.subscriptor = log.on_change_with_subscriptor()
    log.date = datetime.now()
    log.status = 'error'
    log.siro_qr_hash = hmac_recibido
    log.siro_IdReferenciaOperacion = id_referencia
    log.save()

    if hmac_recibido:
        """
        Redirección ok al pago fallido
        """
        """
        Chequear que el hmac sea correcto y no chamuyo
        """
        if not hmac_recibido or not hmac.compare_digest(
            generar_hmac(id_referencia),
            hmac_recibido
            ):
            print('abortado')
            abort(403, "Firma inválida")
        log.error_message = "Pago no exitoso. La billetera pega en URL NO OK"
        log.save()
        voucher.state = 'process_payment_fail'
        voucher.save()
        return jsonify({"status": "OK"}), 200
    else:
        """
        Redirección desde la página del QR
        """
        log.error_message = \
            "Pago no exitoso. La billetera pega en URL NO OK. " \
            + " Redireccionamiento OK"
        log.save()
        subscriptor = voucher.subscriptor
        return render_template('/siro-pago-no-exitoso.html',
            subscriptor=subscriptor, voucher=voucher)


@blueprint.route('/verificar_pago')
@tryton.transaction(readonly=False, user=2)
@login_required
def verficar_pago():
    pool = tryton.pool
    Voucher = pool.get('delco.subscriptor.voucher')
    voucher_id = request.args.get('id')
    voucher = Voucher(voucher_id)

    intentos = int(request.args.get('intentos'))

    if intentos > 300:
        estado = 'TIMEOUT'
        voucher.state = 'posted'
        voucher.siro_qr_string = None
        voucher.save()
    elif voucher.state == 'process_payment_fail':
        estado = "RECHAZADO"
        voucher.state = 'posted'
        voucher.save()
    else:
        estado = 'EN ESPERA'

    if voucher.state in ['processing_payment', 'process_payment_ok', 'paid']:
        estado = "APROBADO"
    return jsonify({"estado": estado}), 200
