from fastapi import FastAPI,Depends
from app.db import get_db
from neo4j import Session

app=FastAPI()

@app.get("/")
def read_root():
    return{"message":"Welcome to eCar FastAPI Service!"}

@app.get("/test-neo4j")
def test_neo4j(session: Session = Depends(get_db)):
    result = session.run("RETURN 'Neo4j is connected!' AS message")
    message = result.single()["message"]
    return {"message": message}