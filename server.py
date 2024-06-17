from flask import Flask
import os
from dotenv import load_dotenv
from models.client import db
from controllers import user

load_dotenv()

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ.get('DATABASE_USER')}:{os.environ.get('DATABASE_PASSWORD')}@{os.environ.get('DATABASE_HOST_SRC')}/{os.environ.get('DATABASE_NAME_SRC')}?options=-csearch_path%3D{os.environ.get('DATABASE_SCHEMA_SRC')}"
db.init_app(app)

# Register routes
app.route('/clients', methods=['GET'])(user.get_clients)
app.route('/clients/<string:client_id>/property', methods=['GET'])(user.get_client_property)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)