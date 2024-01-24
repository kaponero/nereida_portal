from flask import (render_template, redirect, request, url_for,
            flash, session, send_file, jsonify)

from app import tryton
from app.base import blueprint
from app.auth.routes import login_required


@blueprint.route('/index', methods = ['GET','POST'])
@tryton.transaction()
@login_required
def formulario():
    if request.method == 'POST':
        return "all ok"
    else:
        return render_template('/index.html')


@blueprint.route('/comprobantes')
@tryton.transaction()
@login_required
def comprobantes():
    return render_template('/comprobantes.html')
