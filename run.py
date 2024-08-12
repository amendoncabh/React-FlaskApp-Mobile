import os

from Server import create_app

if __name__ == "__main__":
    app = create_app(os.path.abspath(os.path.join("GeTrEs.ini")).lower())
    app.run(host=app.config["SERVER_HOST"], port=app.config["SERVER_PORT"])
