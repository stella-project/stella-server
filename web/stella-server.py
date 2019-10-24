from flask_migrate import Migrate
from app import create_app, db

app = create_app('default')
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
