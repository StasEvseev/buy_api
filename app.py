#coding: utf-8


from flask import Flask



from config import DATABASE_URI


def create_app():
    from resources import api
    from models import db
    from admin import admin
    from assets import assets

    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI


    assets.init_app(application)
    api.init_app(application)
    db.init_app(application)
    admin.init_app(application)

    return application

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)