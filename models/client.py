from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'client'
    __table_args__ = {'schema': os.environ.get('DATABASE_SCHEMA')}

    client_id = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    ac_open_date = db.Column(db.Date, nullable=False)
    id_number = db.Column(db.String(20), nullable=False, unique=True)
    birthday = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<Client {self.full_name}>'
    

class FI(db.Model):
    __tablename__ = 'fi'
    __table_args__ = {'schema': os.environ.get('DATABASE_SCHEMA')}

    auto_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    tkck = db.Column(db.String(20), nullable=False)

class CP(db.Model):
    __tablename__ = 'cp'
    __table_args__ = {'schema': os.environ.get('DATABASE_SCHEMA')}

    auto_id = db.Column(db.Integer, primary_key=True)
    drawable_qty = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.String(20),  nullable=False)
    instrument_id = db.Column(db.String(10), nullable=False)

class MP(db.Model):
    __tablename__ = 'mp'
    __table_args__ = {'schema': os.environ.get('DATABASE_SCHEMA')}

    auto_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    tkck = db.Column(db.String(20), nullable=False)

class CP_PRICE(db.Model):
    __tablename__ = 'cp_price'
    __table_args__ = {'schema': os.environ.get('DATABASE_SCHEMA')}

    market_id = db.Column(db.String(5), primary_key=True)
    instrument_id = db.Column(db.String, primary_key=True)
    closing_price = db.Column(db.Float, nullable=False)