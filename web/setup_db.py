from flask_migrate import Migrate
import os

from app import create_app, db
from app.util import setup_db

app = create_app(os.getenv("FLASK_CONFIG") or "postgres")
migrate = Migrate(app, db)

if __name__ == "__main__":
    with app.app_context():
        setup_db(db)
