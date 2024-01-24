# -*- encoding: utf-8 -*-

from app import app, tryton
from app.home import blueprint
from app.auth.routes import login_required

from flask import render_template, redirect, url_for, request, session
from jinja2 import TemplateNotFound

from functools import wraps
from trytond.transaction import Transaction


@blueprint.route('/')
@tryton.transaction()
@login_required
def index():
    Subscriptor = tryton.pool.get('delco.subscriptor')
    Session = tryton.pool.get('web.user.session')
    user = Session.get_user(session['session_key'])
    if Subscriptor.search([('web_user', '=', user)]):
        with Transaction().set_context(company=1):
            subscriptor, = Subscriptor.search([('web_user', '=', user)])
        return render_template('/index.html', subscriptor=subscriptor)
    return render_template('page-500.html'), 500

@blueprint.route('/<template>')
@tryton.transaction()
def route_template(template):
    try:
        if not template.endswith( '.html' ):
            template += '.html'
        # Detect the current page
        segment = get_segment( request )
        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template,segment=segment)
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500

@app.errorhandler(400)
@tryton.transaction()
def bad_request(e):
    return render_template('page-400.html')

@app.errorhandler(413)
@tryton.transaction()
def largefile_error(e):
 return render_template('page-413.html'), 413

# Helper - Extract current page name from request 
@tryton.transaction()
def get_segment( request ):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
