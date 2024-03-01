import os

class CustomContextManager:
    def __init__(self, location):
        self.location = location

    def __enter__(self):
        print("Loading data")
        os.chdir(self.location)

    def __exit__(self, exc_type, exc_value, traceback):
        print("Data loaded")
        os.chdir('..')
