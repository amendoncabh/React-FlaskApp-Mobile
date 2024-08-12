import os
from configparser import ConfigParser

from flask import Flask
from flask import render_template
from flask.cli import load_dotenv
from flask_cors import CORS

from mongoengine import connect as mongodb_connect

from Server.api.user_blueprint import users_bp
from Server.api.product_blueprint import categories_bp, products_bp
from Server.api.busteam_blueprint import busdrivers_bp, bussupervisor_bp
from Server.api.schoolbus_blueprint import schoolbus_bp
from Server.api.student_blueprint import parents_bp, schools_bp, students_bp
from Server.api.busroute_blueprint import busroutes_bp, stoplocations_bp, routehistories_bp, routelocations_bp, locationstudents_bp


APP_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app(config_filename: str = None):
    """Factory to create the Flask application
    :return: A `Flask` application instance
    """
    app = Flask(__name__,
        static_folder = os.path.join(APP_DIR, 'assets/static'),
        template_folder = os.path.join(APP_DIR, 'assets/templates'),
    )

    load_dotenv(".env")

    config = ConfigParser()
    config.read(config_filename)

    # Setup APP
    app.config["DEBUG"] = config.getboolean("DEFAULT", "debug_mode")
    
    if config.has_section("DB"):
        if config.has_option("DB", "connection_string"):
            app.config["MONGO_URI"]  = config.get("DB", "connection_string")
        else:
            app.config["MONGO_URI"]  = os.environ.get("MONGODB_HOST")

    if config.has_section("SERVER"):
        if config.has_option("SERVER", "name"):
            app.config["SERVER_NAME"] = config.get("SERVER", "name")
        app.config["SERVER_HOST"] = config.get("SERVER", "host") if config.has_option("SERVER", "host") else "0.0.0.0"
        app.config["SERVER_PORT"] = config.get("SERVER", "port") if config.has_option("SERVER", "port") else "5001"

    if config.has_option("DEFAULT", "external_api_url"):
        app.config["EXTERNAL_API_URL"] = config.get("DEFAULT", "external_api_url")

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    _register_blueprints(app)

    if "MONGO_URI" in app.config:
        mongodb_connect(
            host=app.config["MONGO_URI"].format(
                username=os.environ.get("MONGODB_USER"),
                password=os.environ.get("MONGODB_PASS"),
                host_address=os.environ.get("MONGODB_HOST")
            )
        )
    else:
        raise "database missing!"

    CORS(app)

    return app


def _register_blueprints(app):
    # Setup blueprint routes
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(parents_bp)
    app.register_blueprint(schools_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(busdrivers_bp)
    app.register_blueprint(bussupervisor_bp)
    app.register_blueprint(schoolbus_bp)
    app.register_blueprint(stoplocations_bp)
    app.register_blueprint(busroutes_bp)
    app.register_blueprint(routelocations_bp)
    app.register_blueprint(locationstudents_bp)
    app.register_blueprint(routehistories_bp)

    # Setup default routes
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def index(path):
        return render_template("index.html")
