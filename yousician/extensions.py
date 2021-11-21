# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_jwt_extended import JWTManager

from yousician.utils.apispec import APISpecExt
from celery import Celery
from flask_mongoengine import MongoEngine

mongo = MongoEngine()

apispec = APISpecExt()
celery = Celery()
jwt = JWTManager()