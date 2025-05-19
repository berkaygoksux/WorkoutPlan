from app.patterns.api_facade import ApiFacade
from fastapi import FastAPI


def test_register_controllers():
    app = FastAPI()
    api_facade = ApiFacade(app)
    api_facade.register_controllers()
    assert len(app.routes) > 4