from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  amount = db.Column(db.Float, default=10000)
  stocks = db.Column(db.Integer, default=0)
  age = db.Column(db.Integer)
  phone = db.Column(db.Integer)
  email = db.Column(db.String(120), unique=True)
  pword = db.Column(db.String(54))
  status = db.Column(db.String(10), default="user")
  created_on = db.Column(db.DateTime, default=datetime.now())

  def __init__(self, name, age, phone, email, password):
    self.name = name
    self.age = age
    self.phone = phone
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pword = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pword, password)

  def update_amount(self, total, status):
    if(status == 'SELL'):
      self.amount = self.amount + total
    elif(status == "BUY"):
      self.amount = self.amount - total

class Stocks(db.Model):
    __tablename__ = 'stocks'
    sid = db.Column(db.Integer, primary_key= True)
    usemail = db.Column(db.String(120), nullable=False)
    symbol = db.Column(db.String(25))
    stocks = db.Column(db.Integer)

    def __init__(self, email, symbol, stocks):
      self.usemail = email
      self.symbol = symbol
      self.stocks = stocks
    def stocks_update(self, sym, no, status):
      if(self.symbol == sym and status == "BUY"):
        self.stocks = self.stocks + no
      elif(self.symbol == sym and status == "SELL"):
        self.stocks = self.stocks - no


class Transaction(db.Model):
  __tablename__ = 'transactions'
  tid = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120))
  symbol = db.Column(db.String(25))
  stocks = db.Column(db.Integer)
  last_price = db.Column(db.Float)
  total = db.Column(db.Float)
  timestamp = db.Column(db.DateTime)
  status = db.Column(db.String)

  def __init__(self, email, symbol, stocks, last_price, total, status):
    self.email = email
    self.symbol = symbol
    self.stocks = stocks
    self.last_price = last_price
    self.total = total
    self.timestamp = datetime.now()
    self.status = status

