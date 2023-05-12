import os
# basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
        # My old SQLite DB    
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    
    #My new MYSQL DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('mysql://root:password123@localhost/todo_app')


    # SQLALCHEMY_TRACK_MODIFICATIONS = False