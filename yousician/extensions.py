# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from celery import Celery
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

from yousician.utils.apispec import APISpecExt

mongo = MongoEngine()

apispec = APISpecExt()
celery = Celery()
jwt = JWTManager()
