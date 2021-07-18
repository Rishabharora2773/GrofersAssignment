from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
import json

app = Flask(__name__)

app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Order.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Order(db.Model):
  __tablename__ = "Order"
  order_id = db.Column("order_id", db.Integer, primary_key=True)
  order_weight = db.Column("order_weight", db.Integer)
  slot_number = db.Column("slot", db.Integer)

  def __init__(self, id, weight, slot):
    self.order_id = id
    self.order_weight = weight
    self.slot_number = slot

class Vehicle(db.Model):
  __tablename__ = "Vehicle"
  id = db.Column("order_id", db.Integer, primary_key=True)
  type = db.Column("vehicle_type", db.String(100))
  capacity = db.Column("slot", db.Integer)

  def __init__(self, id, type, capacity):
    self.id = id
    self.type = type
    self.capacity = capacity


def myFunc(order):
  return order.slot_number, order.order_weight

@app.route("/")
def main():
  for order_id in range(10):
    weight = random.randint(1,50)
    slot = random.randint(1,4)
    order = Order(order_id,weight,slot)
    db.session.add(order)
    db.session.commit()
    print('order ',order_id, ' added in db!')

  bike = Vehicle(1, "Bike", 30)
  scooter = Vehicle(2, "Scooter", 50)
  truck = Vehicle(3, "Truck", 100)
  db.session.add(bike)
  db.session.add(scooter)
  db.session.add(truck)
  db.session.commit()

  return "hello"



@app.route("/orders")
def orders():
  orders = Order.query.all()
  for order in orders:
    print(order.order_id, order.order_weight, order.slot_number)
  return "Orders printed!"


@app.route("/vehicles")
def vehicles():
  vehicles = Vehicle.query.all()
  vehicle_list = []

  for vehicle in vehicles:
    vehicle_list.append({"id": vehicle.id, "type": vehicle.type, "capacity": vehicle.capacity})
  
  print(vehicle_list)
  return json.dumps(vehicle_list[0])


@app.route("/deliver")
def assignOrders():
  orders = Order.query.all()
  orders.sort(key=myFunc)
  
  morning_slot_orders = []
  afternoon_slot_orders = []
  evening_slot_orders = []

  for order in orders:
    slot = order.slot_number
    if slot==1:
      morning_slot_orders.append(order)
    elif slot==2 or slot==3:
      afternoon_slot_orders.append(order)
    else:
      evening_slot_orders.append(order)
  

  delivery_status = []

  for i in range(len(morning_slot_orders)):
    j = i
    order_ids = []
    curr_weight = 0
    id = 1

    while j<len(morning_slot_orders) and curr_weight + morning_slot_orders[j].order_weight < 30:
      order_ids.append(morning_slot_orders[j].order_id)
      curr_weight += morning_slot_orders[j].order_weight
      j+=1

    delivery_status.append({
      "id" : id,
      "orders" : order_ids,
      "type" : "Bike"
    })

    id += 1
    i = j
  
  return json.dumps(delivery_status[0])

if __name__ == "__main__":
  db.drop_all()
  db.create_all()
  app.run(host='0.0.0.0', port=8080)