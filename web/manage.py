from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

from app import create_app, db
from app.util import setup_db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

with app.app_context():
    setup_db(db)

if __name__ == '__main__':
    manager.run()