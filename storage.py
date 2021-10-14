import os
import argparse
import json
import tempfile

def read_file(storage_path):
    if not os.path.exists(storage_path):
        return {}
    with open(storage_path, 'r') as file:
        raw_file = file.read()
        if raw_file:
            return json.loads(raw_file)
        return {}

def upd(storage_path, key, value):
    file = read_file(storage_path)
    file[key] = file.get(key, [])
    file[key].append(value)
    with open(storage_path, 'w') as f:
        f.write(json.dumps(file))

def prog():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='Key')
    parser.add_argument('--val', help='Value')
    arg = parser.parse_args()
    if arg.key and arg.val:
        upd(storage_path, arg.key, arg.val)
    elif arg.key:
        print(*read_file(storage_path).get(arg.key, []), sep=', ') 
    else:
        print('Wrong')

if __name__ == '__main__':
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    prog()