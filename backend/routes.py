from flask import Blueprint, render_template, session
from backend.code_to_pseudo import code_to_pseudo_api
from backend.existing_creations import existing_creations_api
from backend.generate_pseudo import generate_pseudo_api
import random
import string

bp = Blueprint('main', __name__)

bp.register_blueprint(code_to_pseudo_api, url_prefix='/api')
bp.register_blueprint(existing_creations_api)
bp.register_blueprint(generate_pseudo_api, url_prefix='/api')

@bp.route('/')
def index():
    return render_template('index.html', title='Code2Pseudo')

@bp.route('/home')
def home():
    if 'username' not in session:
        random_digits = ''.join(random.choices(string.digits, k=6))
        session['username'] = f'anonymous{random_digits}'
    return render_template('home.html', title='Code2Pseudo - Home', year='2025')

@bp.route('/code-to-pseudo')
def code_to_pseudo():
    return render_template('code-to-pseudo.html', title='Code2Pseudo - Convert Code to Pseudocode', year='2025')

@bp.route('/pseudo-to-code')
def pseudo_to_code():
    return render_template('pseudo-to-code.html', title='Code2Pseudo - Convert Pseudocode to code', year='2025')

"""
@bp.route('/existing-creations')
def existing_creations():
    return render_template('existing-creations.html', title='Code2Pseudo - Existing Creations', year='2025')
"""

@bp.route('/about')
def about():
    return render_template('about.html', title='Code2Pseudo - About', year='2025')

@bp.route('/help')
def help():
    return render_template('help.html', title='Code2Pseudo - Help', year='2025')

@bp.route('/generate-pseudo')
def generate_pseudo():
    return render_template('generate_pseudo.html', title='Code2Pseudo - Generate Pseudocode', year='2025')