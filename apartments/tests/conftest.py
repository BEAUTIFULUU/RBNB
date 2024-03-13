import pytest


@pytest.fixture(autouse=True)
def use_session_authentication(settings):
    settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
        "rest_framework.authentication.SessionAuthentication",
    ]
