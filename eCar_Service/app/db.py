from neo4j import GraphDatabase
from fastapi import Depends
from typing import Generator
from dotenv import load_dotenv
import os

load_dotenv()


# Neo4j connection config
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Create driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_db() -> Generator:
    with driver.session() as session:
        yield session