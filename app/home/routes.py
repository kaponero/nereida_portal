# -*- encoding: utf-8 -*-

from app import app
from app.home import blueprint

from flask import render_template, redirect, url_for, request, session
from jinja2 import TemplateNotFound

from functools import wraps

@blueprint.route('/')
def index():
    return render_template('/index.html')

@blueprint.route('/')
def comprobantes():
    return render_template('/comprobantes.html')

@blueprint.route('/<template>')
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
def bad_request(e):
    return render_template('page-400.html')

@app.errorhandler(413)
def largefile_error(e):
 return render_template('page-413.html'), 413

# Helper - Extract current page name from request 
def get_segment( request ): 
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None