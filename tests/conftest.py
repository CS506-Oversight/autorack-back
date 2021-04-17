import os

import pytest

from app import create_app
from app.data import db
from app.data.base import Controller


# region `pytest` fixtures
@pytest.fixture
def app():
    app = create_app()

    # Set db to testing db so data in dev db doesn't get cleared
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_TEST_DATABASE_URI")
    # https://stackoverflow.com/a/30611846/11571888
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    # Create all the tables in the testing db
    app.app_context().push()
    db.create_all()

    return app


# endregion

# region `pytest` hooks
def pytest_addoption(parser):
    parser.addoption('--slow', action='store_true', dest='slow', default=False,
                     help='Specify this flag to run slow tests.')
    parser.addoption('--holistic', action='store_true', dest='holistic', default=False,
                     help='Specify this flag to run holistic tests.')
    parser.addoption('--all', action='store_true', dest='all', default=False,
                     help='Specify this flag to run all tests, '
                          'including the one that is either marked as `slow` or `holistic`.')


def pytest_configure(config):
    if not config.option.all:
        marks = []

        if not config.option.slow:
            marks.append('not slow')
        if not config.option.holistic:
            marks.append('not holistic')

        setattr(config.option, 'markexpr', (getattr(config.option, 'markexpr', "") + ' and '.join(marks)).strip())


# endregion


# region Global setup / teardown
@pytest.fixture(scope="function", autouse=True)
def manage_postgresql_database(client):
    # Execute the test itself
    yield

    # Clear all data
    session = db.session
    for ctrl_class in Controller.__subclasses__():
        ctrl_class.get_query().delete()
    session.commit()
# endregion
