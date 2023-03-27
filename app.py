import os
from flask import Flask, request, render_template, redirect, abort, jsonify, flash, url_for
from flask_cors import CORS
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

    @app.route("/about")
    def faq():
        return render_template("pages/about.html")
    
    @app.route("/faq")
    def about_page():
        return render_template("pages/faq.html")
    
    @app.route("/caption")
    def caption_page():
        return render_template("pages/caption.html")

    @app.route("/upload", methods=["POST"])
    def upload():
        # check if the post request has the file part
        if request.method == 'POST':
            if 'image' not in request.files:
                flash('No file part')
            file = request.files['image']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No File Selected')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            model =  tf.keras.models.load_model('.\\model_weights.h5')

            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img = image.load_img(path, target_size=(224, 224))
            x=image.img_to_array(img)
            x /= 255
            x=np.expand_dims(x, axis=0)
            images = np.vstack([x])

            prediction = model.predict(images, batch_size=10)

            return jsonify({
                'prediction': prediction,
                'success': True,
                #'caption': caption
                }), 200
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
            'description': 'Sorry but the page you are looking for does not exist, have been removed, name changed or is temporarily unavailable.',
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