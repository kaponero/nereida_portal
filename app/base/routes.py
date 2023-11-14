from flask import (render_template, redirect, request, url_for,
            flash, session, send_file, jsonify)

from app.base import blueprint

@blueprint.route('/index', methods = ['GET','POST'])
def formulario():
    if request.method == 'POST':
        return "all ok"
    else:
        return render_template('/index.html')


