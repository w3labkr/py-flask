# Miscellaneous operating system interfaces
import os

# JSON encoder and decoder
import json

# The Python micro framework for building web applications.
from flask import Blueprint, session, redirect, url_for, escape, flash
from flask import request, Response, make_response, render_template, send_from_directory

# Import the middleware file.
import middlewares.analysis_stock_prediction_middleware as middleware
# import models.analysis_stock_prediction_model as model

# Import a custom module file.
import packages.routers as routers
import packages.krx as krx


def constructor(data):

    file = os.path.splitext(os.path.basename(__file__))[0]
    slug = routers.file2slug(file)

    router = Blueprint(file, __name__)

    @router.before_request
    def init():
        data.update({
            'page': routers.file2page(file),
            'layout': 'sidebar-content',
            'navigation': {
                'filename': 'navigation-analysis',
                'title': '데이터분석',
            },
            'secondary': {'filename': 'sidebar.jinja'},
            'tertiary': {'filename': 'sidebar.jinja'},
            'request': {
                'form': {
                    'stockmarket': 'kospi',
                    'stockcode': '095570.KS',
                    'kospicode': '095570',
                    'kosdaqcode': '060310',
                    'learningday': '1',
                    'forecastday': '5'
                }
            },
            'response': {
                'kospi': json.loads(krx.main('kospi'), encoding='utf-8'),
                'kosdaq': json.loads(krx.main('kosdaq'), encoding='utf-8'),
            },
            'dataset': {},
        })

    @router.route('/', methods=['GET'])
    def get_index():
        data['dataset'] = model.constructor({})
        return render_template(routers.get_template_directory('pages', slug=slug), data=data)

    @router.route('/', methods=['POST'])
    def post_index():
        data['dataset'] = model.constructor(request.form)
        data['request'] = request
        return render_template(routers.get_template_directory('pages', slug=slug), data=data)

    return router
