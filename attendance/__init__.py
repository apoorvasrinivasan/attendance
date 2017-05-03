from flask.ext.mongoengine import MongoEngine
from flask import Flask,  render_template

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'attendance',
    'host': 'localhost',
    'port': 27017,
    # 'SESSION_TYPE':'filesystem'
}
app.config['SECRET_KEY'] = 'many random bytes'
app.config['SESSION_TYPE'] = 'filesystem'

db = MongoEngine(app)

from .admin import get_admin
admin = get_admin(app)


# register_blueprints(app);
