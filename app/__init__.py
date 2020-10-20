from flask import Flask 
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# Application factory.
def create_app(config_file=None):

	app = Flask(__name__)

	app.config.from_mapping(
		SECRET_KEY='dev',
		SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db',
		SQLALCHEMY_TRACK_MODIFICATIONS=False
	)

	@app.route('/test')
	def index():
		return 'Hello world!'

	# Initialize db to current app.
	db.init_app(app)

	# Blueprints import and register them.
	from app.auth import bp as auth_bp

	app.register_blueprint(auth_bp, url_prefix='/auth')

	return app