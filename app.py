import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()
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
    
    @app.route('/caption', methods=['POST'])
    def index_post():
        # Read the values from the form
        original_text = request.form['text']
        target_language = request.form['language']

        # Load the values from .env
        key = os.environ['KEY']
        endpoint = os.environ['ENDPOINT']
        location = os.environ['LOCATION']

        # Indicate that we want to translate and the API version (3.0) and the target language
        path = '/translate?api-version=3.0'
        # Add the target language parameter
        target_language_parameter = '&to=' + target_language
        # Create the full URL
        constructed_url = endpoint + path + target_language_parameter

        # Set up the header information, which includes our subscription key
        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # Create the body of the request with the text to be translated
        body = [{ 'text': original_text }]

        # Make the call using post
        translator_request = requests.post(constructed_url, headers=headers, json=body)
        # Retrieve the JSON response
        translator_response = translator_request.json()
        # Retrieve the translation
        translated_text = translator_response[0]['translations'][0]['text']

        # Call render template, passing the translated text,
        # original text, and target language to the template
        return render_template(
            'pages/translate.html',
            translated_text=translated_text,
            original_text=original_text,
            target_language=target_language
        )

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

            return jsonify({
                'image' : path,
                'description' : caption8k
            })
        return jsonify({
            'success': False
            }), 405

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

            return jsonify({
                'image' : path,
                'description' : caption30k
            })
        return jsonify({
            'success': False
            }), 405
           
    @app.route("/VitGpt2ImageCaption", methods=["POST"])
    def upload_f():
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
            VitGpt2ImageCaption = predict_step([path])

            # Extract the string from the input list
            input_string = VitGpt2ImageCaption[0]
            # Remove the square brackets and single quotes from the input string  
            captiongpt = input_string

            return jsonify({
                'image' : path,
                'description' : captiongpt
            })
        return jsonify({
            'success': False
            }), 405
    
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