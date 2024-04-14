from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'users.login'
login.login_message_category = 'info'
mail = Mail()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from app.users.routes import users
    from app.posts.routes import posts
    from app.views.routes import views

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(views)

    return app, db









# ''' __init__.py'''
# from flask import Flask
# from app.config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager
# from flask_mail import Mail


# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(Config)
#     db = SQLAlchemy(app)
#     migrate = Migrate(app, db)
#     login = LoginManager(app)
#     login.login_view = 'users.login'
#     login.login_message_category = 'info'
#     mail = Mail(app)

#     from app.users.routes import users
#     from app.posts.routes import posts
#     from app.views.routes import views


#     app.register_blueprint(users)
#     app.register_blueprint(posts)
#     app.register_blueprint(views)