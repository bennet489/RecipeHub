from app import create_app
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, Post
from config import Config

app, db = create_app(config_class=Config)

# import app

# @app.shell_context_processor
# def make_shell_context():
#     return {'sa': sa, 'so': so, 'db': app.db, 'User': User, 'Post': Post}


if __name__ == "__main__":
    app.run(debug=True)
    