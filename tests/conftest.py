import pytest
from mongoengine import disconnect_all

from yousician.app import create_app


@pytest.fixture
def app():
    """Create application for the tests."""
    disconnect_all()
    app = create_app(testing=True)
    return app
