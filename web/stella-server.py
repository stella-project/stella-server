from app import create_app, db
from app.util import setup_db
from flask_migrate import Migrate


# app = create_app('default')  # Use 'default' for local installation with SQLite database.
app = create_app('postgres')  # When running in production use 'postgres'.
migrate = Migrate(app, db)

if __name__ == '__main__':

    with app.app_context():
        setup_db(db)
      
    app.run(host='0.0.0.0', port=8000, debug=True)
