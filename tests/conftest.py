import logging

import pytest
from mongoengine import disconnect_all
from webtest import TestApp

from yousician.app import create_app


@pytest.fixture
def app():
    """Create application for the tests."""
    disconnect_all()
    _app = create_app(testing=True)
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """Create Webtest app."""
    return TestApp(app)
