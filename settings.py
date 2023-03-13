import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'vars.env')
load_dotenv(dotenv_path)

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
DEBUG = True
