from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  temperature = db.Column(db.String(80), unique=False, nullable=False)
  humidity = db.Column(db.String(120), unique=False, nullable=False)
  timestamp = db.Column(db.String(120), unique=False, nullable=False)

  def __init__(self, temperature, humidity,timestamp):
    self.temperature = temperature
    self.humidity = humidity
    self.timestamp = timestamp

db.create_all()

@app.route('/items/<id>', methods=['GET'])
def get_item(id):
  item = Item.query.get(id)
  del item.__dict__['_sa_instance_state']
  return jsonify(item.__dict__)

@app.route('/items', methods=['GET'])
def get_items():
  items = []
  for item in db.session.query(Item).all():
    del item.__dict__['_sa_instance_state']
    items.append(item.__dict__)
  return jsonify(items)

@app.route('/items', methods=['POST'])
def create_item():
  body = request.get_json()
  db.session.add(Item(body['msg']['temperature'], body['msg']['humidity'], body['metadata']['ts']))
  db.session.commit()
  return "item created"

@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
  body = request.get_json()
  print("Received JSON")
  print(body)
  db.session.query(Item).filter_by(id=id).update(
    dict(temperature=body['msg']['temperature'], humidity=body['msg']['humidity'],timestamp=body['metadata']['ts']))
  db.session.commit()
  return "item updated"

@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
  db.session.query(Item).filter_by(id=id).delete()
  db.session.commit()
  return "item deleted"