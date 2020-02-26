from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

from app import create_app, db

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app(os.getenv('FLASK_CONFIG') or 'postgres')
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
