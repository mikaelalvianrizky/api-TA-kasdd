from flask import redirect, render_template, request, jsonify, url_for, request
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    pass