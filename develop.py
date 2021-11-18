#!/usr/bin/env
from application.app import create_app

app = create_app("application.config.DevelopmentConfig")
