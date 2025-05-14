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
    telephoneNumber = StringProperty()
    gender = StringProperty()
    registrationDate = DateTimeProperty(default_now=True)
    active = BooleanProperty(default=True)

      # This makes the uid a regular public field

# ---------- Driver Node ----------
class Driver(StructuredNode):
    did=StringProperty(required=True)
    numberOfClientsAmount = IntegerProperty(default=0)
    numberOfHoursAmount = IntegerProperty(default=0)

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

     
