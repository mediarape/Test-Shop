from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config


app = Flask(__name__, static_url_path='/static')
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.debug = True
db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import Users

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .catalog import catalog as cat_blueprint
app.register_blueprint(cat_blueprint)

from .items import items as items_blueprint
app.register_blueprint(items_blueprint)
