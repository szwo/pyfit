import json
import os.path


# IO Helper Functions

def generate_json_target(filename):
    return filename + '.json'


def does_file_exist(filename):
    return os.path.isfile(generate_json_target(filename))


def open_file(filename):
    with open(generate_json_target(filename)) as file:
        data = json.load(file)
        return data


def save_file(filename, payload):
    with open(generate_json_target(filename), 'w') as fp:
        json.dump(payload, fp)
