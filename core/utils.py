import os
import asyncio
import random

#save the the raw and cleaned data into a folders
class Filesaver:
    def __init__(self, type: str, source: str, filename: str, data: str):
        self.type = type
        self.source = source
        self.filename = filename
        self.data = data

    #create folders if not exist:
    def create_folder(self):
        path = os.path.join(self.type, self.source)
        os.makedirs(path, exist_ok=True)
        return path
    
    def save(self):
        #create folder if not exist
        path = self.create_folder()
        with open(os.path.join(path, self.filename), 'w', encoding='utf-8') as f:
            f.write(self.data)

class FileLoader:
    def __init__(self, type: str, source: str):
        self.type = type
        self.source = source
    
    def load(self):
        files_path = os.path.join(self.type, self.source)
        return [os.path.join(files_path, f) for f in os.listdir(files_path)]


# time sleep using asyncio for to avoid 429 error
class Sleeper:
    def __init__(self, seconds: int):
        self.min = seconds
        self.max = seconds + 2
        self.seconds = random.randint(self.min, self.max)
    
    async def sleep(self):
        await asyncio.sleep(self.seconds)