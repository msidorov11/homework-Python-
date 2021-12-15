import os, tempfile, numpy

class File:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.current = 0
        if not os.path.exists(self.path_to_file):
            open(self.path_to_file, 'w').close()
            self.text = ""
        else:
            with open(self.path_to_file, 'r') as file:
                self.lines = file.readlines()
                self.text = ""
                for line in self.lines:
                    self.text += line
                self.end = len(self.lines)

    def __str__(self):
        return self.path_to_file

    def read(self):
        with open(self.path_to_file, 'r') as file:
            self.lines = file.readlines()
            self.text = ""
            for line in self.lines:
                self.text += line
            self.end = len(self.lines)
        return self.text

    def write(self, text):
        with open(self.path_to_file, 'w') as file:
            self.text = text
            file.write(self.text)
            self.lines = self.text.split("\n")
            self.end = len(self.lines)
            return len(self.text)

    def __add__(self, file_):
        text_ = self.text + file_.text
        new_file = str(numpy.random.randint(10000)) + '.txt'
        path_ = os.path.join(tempfile.gettempdir(), new_file)
        file_ = File(path_)
        file_.write(text_)
        return file_

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        else:
            result = self.lines[self.current]
            self.current += 1
            if result == "":
                raise StopIteration
            else:
                return result
        #else:
            #raise StopIteration

if __name__ == '__main__':
    pass
