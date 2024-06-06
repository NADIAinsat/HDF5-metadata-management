from neomodel import StructuredNode, StringProperty, RelationshipTo, config
import json
import os

config.DATABASE_URL = 'bolt://neo4j:nadiapsw@localhost:7687'

class EntityNode(StructuredNode):
    name = StringProperty(unique_index=True)
    value = StringProperty()
    has_child = RelationshipTo('EntityNode', 'HAS_CHILD')

def create_nodes_and_relationships(parent, data, parent_node=None):
    for key, value in data.items():
        if isinstance(value, dict):
            node = EntityNode(name=key).save()
            create_nodes_and_relationships(key, value, node)
        elif isinstance(value, list):
            node = EntityNode(name=key).save()
            for item in value:
                child_node = EntityNode(name=item).save()
                node.has_child.connect(child_node)
        else:
            node = EntityNode(name=key, value=str(value)).save()
        
        if parent_node:
            parent_node.has_child.connect(node)

#########

directory = 'C:/PFE project/JSON files'

for filename in os.listdir(directory):
    if filename.endswith('.json'): 
        file_path = os.path.join(directory, filename)

        with open(file_path) as f:
            data = json.load(f)

        root_node = EntityNode(name=filename).save()
        create_nodes_and_relationships('root', data, root_node)