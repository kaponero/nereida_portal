from flask import send_file

from app import tryton
from app.download_attachment import blueprint
from app.auth.routes import login_required

from io import BytesIO

@blueprint.route("/download_attachment/<attachment_id>")
@tryton.transaction()
@login_required
def download_attachment(attachment_id):
    Attachment = tryton.pool.get('ir.attachment')
    attachment, = Attachment.search([('id', '=', attachment_id)])
    file_bytes = attachment.data
    file_name = attachment.name
    return send_file(
        BytesIO(file_bytes),
        as_attachment=True,
        attachment_filename= file_name)

#@blueprint.route('/download_report/<report_name>/<filename>/<id>')
#@tryton.transaction()
#@login_required
def download_report(report_name, filename, id):
    Instruction = tryton.pool.get(report_name, type='report')
    ext, content, _, name = Instruction.execute([id], {'vouchers': [id]})
    return send_file(
        BytesIO(content),
        attachment_filename='Voucher'+'_'+id+'.pdf',
        as_attachment=False)
