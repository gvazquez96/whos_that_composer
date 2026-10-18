import threading
import webbrowser
from app import create_app
from app.models import db


app, session = create_app()


def open_browser():
    """ AUTOMATICALLY OPENS BROWSER """
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    with app.app_context():  # Needed for DB operations
        db.create_all()  # Creates the database and tables
        threading.Timer(1, open_browser).start()
    app.run()
