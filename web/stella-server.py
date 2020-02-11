from flask_migrate import Migrate
from app import create_app, db
from app.dev import setup

app = create_app('default')
migrate = Migrate(app, db)

if __name__ == '__main__':

    with app.app_context():
        setup(db)

    app.run(host='0.0.0.0', port=8000, debug=True)
