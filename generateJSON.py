import h5py
import json
import numpy as np

def convert_to_json_serializable(value):
    if isinstance(value, np.ndarray):  #checks if a value is a NumPy array
        return value.tolist() #converts it to a Python list
    elif isinstance(value, bytes):
        return value.decode('utf-8')  # we had the error: Object of type bytes is not JSON serializable
    return value


def read_hdf5_metadata(file_path):
    metadata = {}
    with h5py.File(file_path, 'r') as f:
        # Function to recursively traverse the HDF5 file
        def traverse(parent, obj):
            object_metadata = {}
            for key, value in obj.attrs.items():
                # print("obj.attrs.items",key,value)
                object_metadata[key] = convert_to_json_serializable(value)
            if isinstance(obj, h5py.Group):
                for name, sub_obj in obj.items():
                    print("obj.items",name, sub_obj)
                    traverse(parent + '/' + name, sub_obj)
            parent_key = parent.rsplit('/', 1)[-1] if '/' in parent else ''
            if parent_key:
                #print("the parent key is ",parent_key)
                metadata[parent_key] = object_metadata
            else:
                metadata.update(object_metadata)

        # Start traversal from the root group
        traverse('', f)
    return metadata


file_path = r'C:/PFE project/HDF5 Files/pressure_mat.h5'
metadata = read_hdf5_metadata(file_path)

# Print the metadata
#for key, value in metadata.items():
#    print(f"{key}: {value}")

# Serializing json
json_object = json.dumps(metadata, indent=4, default=str)  # Using default=str to handle non-serializable types

# Writing to sample.json
with open("pressure.json", "w") as outfile:
    outfile.write(json_object)
