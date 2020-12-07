"""
flaskConfig.py
Author: Umar Ehsan

The purpose of this class is to provide flask configuration variables
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '9876543210123456789'