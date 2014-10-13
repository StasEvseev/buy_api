#coding: utf-8


from flask import Flask

from flask.ext.assets import Environment, Bundle

from config import DATABASE_URI


def create_app():
    from resources import api
    from models import db
    from admin import admin

    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    assets = Environment(application)
    js = Bundle('main.js', output='gen/packed.js')
    assets.register('js_all', js)

    api.init_app(application)
    db.init_app(application)
    admin.init_app(application)

    from admin.myview import MyView
    admin.add_view(MyView(name=u'Проверка почты'))

    return application

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)