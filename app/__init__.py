from config import Config

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
from app.schema import schema

from controllers.UserController import UserController
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    
    # Allows you to get configurations
    # from the config file with the exact environment
    # that you require
    app.config.from_object((get_environment_config()))

    db.init_app(app)
    
    userController = UserController(db)


    # BASIC CRUD USER 
    @app.route("/user/", method)
    def get_user():
        try:
            userId = request.args.get('userId')
        except:
            abort(500)
        user = userController.find_user(userId)
        if(user == None):
            abort(400)
        else:
            return user
        
    

    #ERROR HANDLERS
    @app.errorhandler(404)
    def not_found(error):
        return ("Not found",404)

    @app.errorhandler(500)
    def server_error(error):
        return("Internal server error", 500)

    app.add_url_rule( # NO TOCAR DE MOMENTO
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True  # for having the GraphiQL interface
        )
    )

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app

def get_environment_config():
    if Config.ENV == "PRODUCTION":
        return "config.ProductionConfig"
    elif Config.ENV == "DEVELOPMENT":
        return "config.DevelopmentConfig"