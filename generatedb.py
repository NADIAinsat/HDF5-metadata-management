import json
import pyodbc
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os 

# Define the database connection
DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'PC-NADIA\MSSQLSERVER19'
DATABASE_NAME = 'HDF5'

connection_string = f"""
        DRIVER={DRIVER_NAME};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        Trusted_Connection=yes;
"""
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()
# Create the database engine
engine = create_engine('mssql+pyodbc://', creator=lambda: connection)

Base = declarative_base()

directory = 'C:/PFE project/JSON files'

# Define dynamic data models
models = {}

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def insert_json_object(data, parent_id=None):
    for key, value in data.items():
        if isinstance(value, list):
            # Handle list values by inserting each element as a separate row
            for item in value:
                obj = JsonObject(name=key, value=str(item), parent_id=parent_id)
                session.add(obj)
                session.commit()  # Commit each object before processing its children
        else:
            obj = JsonObject(name=key, value=str(value), parent_id=parent_id)
            session.add(obj)
            session.commit()  # Commit each object before processing its children
            if isinstance(value, dict):
                insert_json_object(value, obj.id)
        
# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'): 
        file_path = os.path.join(directory, filename)
        class JsonObject(Base):
            __tablename__ = os.path.splitext(filename)[0]
            id = Column(Integer, primary_key=True)
            name = Column(String)
            value = Column(String)
            parent_id = Column(Integer, ForeignKey(f'{__tablename__}.id'))
        
        Base.metadata.create_all(engine)

        with open(file_path) as f:
            data = json.load(f)
            insert_json_object(data)

# Commit and close the session
session.commit()
session.close()
