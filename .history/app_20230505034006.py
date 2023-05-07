import os
import sys
sys.path.append('./src')
from flask import Flask, request, render_template, redirect, abort, jsonify, flash, url_for
from flask_cors import CORS
from src.flickr8k import *
from src.flickr30k import *
from src.VitGpt2ImageCaption import *
import warnings
warnings.filterwarnings("ignore")
from sqlalchemy import or_
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from werkzeug.utils import secure_filename
from flask import send_from_directory
from keras.preprocessing import image
import matplotlib.pyplot as plt


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    #setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route("/")
    def landing_page():
        return render_template("pages/index.html")
    
    @app.route("/caption")
    def caption_page():
        return render_template("pages/caption.html")

    @app.route("/flickr8k", methods=["POST"])
    def upload_file():
        # check if the post request has the file part
        if request.method == 'POST':
            if 'image' not in request.files:
                flash('No file part')

            image = request.files['image']

            # if user does not select file, browser also
            # submit an empty part without filename
            if image.filename == '':
                flash('No File Selected')

            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            caption8k = caption_this_image(path)

            result_dic = {
                'image' : path,
                'description' : caption8k
            }
        return render_template('pages/caption.html', results = result_dic)

    @app.route("/flickr30k", methods=["POST"])
    def up_file():
        # check if the post request has the file part
        if request.method == 'POST':
            if 'image' not in request.files:
                flash('No file part')

            image = request.files['image']

            # if user does not select file, browser also
            # submit an empty part without filename
            if image.filename == '':
                flash('No File Selected')

            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            caption30k = runModel(path)

            result_dic = {
                'image' : path,
                'description' : caption30k
            }
        return render_template('pages/caption.html', results = result_dic)
    
    @app.route("/VitGpt2ImageCaption", methods=["POST"])
    def upload_f():
        if request.method == 'POST':
            if 'files' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['files']

            if file.filename == '':
                flash('No File Selected')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                VitGpt2ImageCaption = predict_step([path])

                input_string = VitGpt2ImageCaption[0]
                captiongpt = input_string.strip("[]'")

                result_dic = {
                    'image': path,
                    'description': captiongpt
                }

                return render_template('pages/caption.html', results=result_dic)

        return redirect(request.url)

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                filename)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return render_template('pages/errors/404.html', data={
            'success': False,
            'error': 404,
            'message': 'Page Not Be Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server errors'
        }), 500
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4040, debug=True)