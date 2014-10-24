#coding: utf-8


from flask import Flask, redirect, g, jsonify
from flask.ext.triangle import Triangle



from config import DATABASE_URI, SECRET_KEY
from security import auth


def create_app():
    from resources import api
    from models import db
    from admin import admin
    from assets import assets
    from security import login_manager

    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    application.config['SECRET_KEY'] = SECRET_KEY

    Triangle(application)
    assets.init_app(application)
    api.init_app(application)
    db.init_app(application)
    admin.init_app(application)
    login_manager.init_app(application)

    return application

app = create_app()

@app.route('/')
def index():
    return redirect("/admin")

# @app.route('/api/token')
# @auth.login_required
# def get_auth_token():
#     """
#     Получаем токен для работы.
#     """
#     token = g.user.generate_auth_token()
#     return jsonify({ 'token': token.decode('ascii') })

if __name__ == "__main__":
    app.run(debug=True)