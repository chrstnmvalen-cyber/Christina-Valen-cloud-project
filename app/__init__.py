from flask import Flask
from flask_login import LoginManager
from config import Config
from .models import db, User

login_manager = LoginManager()
@login_manager.user_loader

def load_user(user_id):
   return User.query.get(int(user_id))

def create_app():
   app = Flask(__name__)
   app.config.from_object(Config)
   db.init_app(app)
   login_manager.init_app(app)
   from .routes.auth import auth
   from .routes.products import products
   from .routes.cart import cart
   from .routes.orders import orders
   from .routes.metrics import metrics
   app.register_blueprint(auth)
   app.register_blueprint(products)
   app.register_blueprint(cart)
   app.register_blueprint(orders)
   app.register_blueprint(metrics)
   with app.app_context():
      db.create_all()
   return app
