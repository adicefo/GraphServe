from neomodel import (
    StructuredNode, StringProperty, EmailProperty, DateTimeProperty, BooleanProperty,
    IntegerProperty, RelationshipTo, RelationshipFrom,UniqueIdProperty,FloatProperty
)
from datetime import datetime

# ---------- User Node ----------
class User(StructuredNode):
    uid = StringProperty(required=True)
    name = StringProperty(required=True)
    surname = StringProperty(required=True)
    email = EmailProperty()
    username = StringProperty()
    password=StringProperty()
    password_confirm=StringProperty()
    telephone_number = StringProperty()
    gender = StringProperty()
    registration_date = DateTimeProperty(default_now=True)
    active = BooleanProperty(default=True)

    

# ---------- Driver Node ----------
class Driver(StructuredNode):
    did=StringProperty(required=True)
    number_of_clients_amount = IntegerProperty(default=0)
    number_of_hours_amount = IntegerProperty(default=0)

    user = RelationshipTo(User, 'IS')
 

# ---------- Client Node ----------
class Client(StructuredNode):
    cid=StringProperty(required=True)
    image = StringProperty(required=False)

    user = RelationshipTo(User, 'IS')
  
# ---------- Admin Node ----------
class Admin(StructuredNode):
    aid=StringProperty(required=True)
    user = RelationshipTo(User, 'IS')


# ---------- Route Node ----------
class Route(StructuredNode):
    rid = StringProperty(required=True)
    source_point_lat = FloatProperty()
    source_point_lon = FloatProperty()
    destination_point_lat = FloatProperty()
    destination_point_lon = FloatProperty()
    start_date = DateTimeProperty()
    end_date = DateTimeProperty()
    duration = IntegerProperty(default=0)
    number_of_kilometers = FloatProperty()
    full_price = FloatProperty()
    paid = BooleanProperty(default=False)
    status = StringProperty()

    client = RelationshipTo('Client', 'OWNED_BY')
    driver = RelationshipTo('Driver', 'DRIVEN_BY')

# ---------- Vehicle Node ----------

class Vehicle(StructuredNode):
    vid = StringProperty(required=True)
    available = BooleanProperty()
    average_fuel_consumption = FloatProperty()
    name = StringProperty(required=True)
    image = StringProperty()  # or BinaryProperty
    price = FloatProperty(required=True)

# ---------- Rent Node ----------
class Rent(StructuredNode):
    rid = StringProperty(required=True)
    rent_date = DateTimeProperty()
    end_date = DateTimeProperty()
    number_of_days = IntegerProperty()
    full_price = FloatProperty()
    paid = BooleanProperty(default=False)
    status = StringProperty()

    vehicle = RelationshipTo('Vehicle', 'RENTED_VEHICLE')
    client = RelationshipTo('Client', 'RENTED_BY')

# ---------- Review Node ----------
class Review(StructuredNode):
    rid=StringProperty(required=True)
    value = IntegerProperty(required=True)
    description = StringProperty(required=True)
    adding_date = DateTimeProperty(default_now=True)

    client = RelationshipTo('Client', 'REVIEWED_BY')
    driver = RelationshipTo('Driver', 'REVIEWED_DRIVER')
    route = RelationshipTo('Route', 'REVIEWED_ROUTE')

# ---------- Notification Node ----------
class Notification(StructuredNode):
    nid=StringProperty(requried=True)
    title = StringProperty()
    content = StringProperty()
    image = StringProperty()  
    adding_date = DateTimeProperty(default_now=True)
    for_client = BooleanProperty()


# ---------- Statistics Node ----------
class Statistics(StructuredNode):
    sid = StringProperty(required=True)                 
    number_of_hours = IntegerProperty()                
    number_of_clients = IntegerProperty()               
    price_amount = FloatProperty()                      

    beginning_of_work = DateTimeProperty()              
    end_of_work = DateTimeProperty()                    

    driver = RelationshipTo('Driver', 'RECORDED_FOR')   # one statistics record → one driver
