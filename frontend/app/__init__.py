'''
__init__.py - Initialize the application, logins, and its views
'''
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask_admin.base import MenuLink
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_wtf.csrf import CsrfProtect
from config import FIRST_USER_PASS, FIRST_USER_NAME

# Initialize the app and database, import the config
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
CsrfProtect(app)
app.killswitch = 0

# setup db, create the db, setup security, and add first user
from app import models
userstore = SQLAlchemyUserDatastore(db, models.User, None)
sec = Security(app, userstore)
db.create_all()
try:
    userstore.create_user(email=FIRST_USER_NAME, password=FIRST_USER_PASS)
    db.session.commit()
except: db.session.rollback()

#this loads all views
from app.views import main, admin

#admin setup
_admin = Admin(app, 'NYX Admin', template_mode='bootstrap3',
              index_view=admin.ProtectedIndexView())
_admin.add_link(MenuLink(name='Back to Site', url='/'))
_admin.add_view(admin.UserModelView(models.User, db.session))
_admin.add_view(admin.BotModelView(models.Bot, db.session))
