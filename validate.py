import json
from jsonschema import validate, ValidationError

def validate_json(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
        print("JSON is valid against the schema.")
    except ValidationError as e:
        print("JSON is not valid against the schema:")
        print(e)

# Load your JSON Schema
with open("C:\PFE project\Implementation\schema\structB.json", "r") as schema_file:
    schema = json.load(schema_file)

# Load your JSON data
with open("C:/PFE project/Implementation/validator/exampleB.json", "r") as json_file:
    json_data = json.load(json_file)

# Validate the JSON data against the schema
validate_json(json_data, schema)
