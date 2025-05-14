# Neomodel config 

from neomodel import config
import os
from dotenv import load_dotenv

load_dotenv()

config.DATABASE_URL = os.getenv("NEO4J_URI") 
