from neomodel import (
    StructuredNode, StringProperty, EmailProperty, DateTimeProperty, BooleanProperty,
    IntegerProperty, RelationshipTo, UniqueIdProperty
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

      # This makes the uid a regular public field

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

     
