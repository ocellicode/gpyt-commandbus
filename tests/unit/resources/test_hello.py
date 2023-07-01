import pytest
from hamcrest import assert_that, is_

from gpyt_commandbus.injection.injector import app as imported_app


@pytest.fixture
def app():
    imported_app.config.update(
        {
            "TESTING": True,
        }
    )
    # other setup can go here
    yield imported_app
    # clean up / reset resources here


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_request_example(client):
    response = client.post("/hello", json={"name": "Testing"})
    assert_that(response.status_code, is_(201))
    assert_that(response.json, is_("Hello, Testing"))
