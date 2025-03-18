from flask import Flask
from flask_migrate import Migrate
from app import app, db  # Assuming you have app and db in app.py

migrate = Migrate(app, db)

# Adding Migrate commands to Flask CLI
if __name__ == "__main__":
    from flask.cli import with_appcontext
    from flask_migrate import upgrade, migrate, init

    @app.cli.command('db init')
    @with_appcontext
    def db_init():
        """Initialize the database."""
        init()

    @app.cli.command('db migrate')
    @with_appcontext
    def db_migrate():
        """Generate migration scripts."""
        migrate()

    @app.cli.command('db upgrade')
    @with_appcontext
    def db_upgrade():
        """Apply migrations to the database."""
        upgrade()

    app.run(debug=True)
