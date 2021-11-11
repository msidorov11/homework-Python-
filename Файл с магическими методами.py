import os
import uuid

class File:
    def __init__(self, path):
        self.path = path
        self.position = 0
        if not os.path.exists(self.path):
            open(self.path, 'w').close()

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def write(self, text):
        with open(self.path, 'w') as f:
            return f.write(text)

    def __add__(self, obj):
        path_ = os.path.join(
            os.path.dirname(self.path),
            str(uuid.uuid4().hex)
        )
        file = type(self)(path_)
        file.write(self.read() + obj.read())

        return file

    def __str__(self):
        return self.path

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.position)
            line = f.readline()
            if not line:
                self.position = 0
                raise StopIteration('EOF')

            self.position = f.tell()
            return line