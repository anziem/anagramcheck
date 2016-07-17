#!/usr/bin/env python
# Import the Flask Framework
from flask import Flask, request, url_for, render_template, flash, redirect, \
        session, abort
from random import SystemRandom

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    """Checks if two words are anagrams of each other."""
    error = None
    if request.method == 'POST':
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)
        else:
            string_1 = request.form.get("firststring")
            string_2 = request.form.get("secondstring")
            if "" in [string_1, string_2]:
                flash('Oops, you missed a step! Enter two phrases to compare.', 'error')
            else:
                ignore_formatting = request.form.get("ignore_formatting")
                message_start = '"{0}" and "{1}" are '.format(string_1, string_2)
                anagrams = message_start+' anagrams.'
                non_anagrams = message_start+' NOT anagrams.'
                if ignore_formatting:
                    #  this removes whitespace and special characters
                    chars_1 = ''.join(e for e in string_1 if e.isalnum())
                    chars_2 = ''.join(e for e in string_2 if e.isalnum())
                    #  this removes case
                    string_1 = chars_1.lower()
                    string_2 = chars_2.lower()
                if len(string_1) != len(string_2):
                    flash(non_anagrams, 'warning')
                elif sorted(string_1) != sorted(string_2):
                    flash(non_anagrams, 'warning')
                else:
                    flash(anagrams, 'info')
    return render_template('index.html')

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(SystemRandom().random())
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
