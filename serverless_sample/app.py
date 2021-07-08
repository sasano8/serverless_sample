from flask import Flask
from flask_login import LoginManager
from flask_sessionstore import Session

from .config import EnvConfig

app = Flask(__name__)
app.config.from_mapping(EnvConfig().get_config_as_dict())


def block(func):
    func()


@block
def setup_login_manager():
    from .lib.utils import setup_auth

    login_manager = LoginManager()
    login_manager.init_app(app)
    setup_auth(login_manager)
    login_manager.login_view = "login"
    login_manager.login_message = "ログインしてください"


@block
def load_modules():
    from .views import entries, views


Session(app)
