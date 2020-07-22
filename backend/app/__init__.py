from flask import Flask
from .config import Config
from .extensions import db, mail, migrate, jwt
from .user.controllers import user_api
from .posts.controllers import post_api
from .comments.controllers import comment_api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(user_api)
    app.register_blueprint(post_api)
    app.register_blueprint(comment_api)

    return app