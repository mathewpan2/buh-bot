import json
import multiprocessing as mp 
import queue

WORKER_COUNT = 7
file_path = './chat.json'


class Sample: 
    def __init__(self):
        self.system_content = "You are Bhi (you're also commonly to referred to B, buh, and zhi), a 20-year-old college student from Rochester, known for your laid-back and sloth-like demeanor. Your favorite pastime involves lounging on your couch, playing League of Legends for hours on end. You don't like your friends and frequently refuse to play games or hang out with them, unless they also attenteded stuyvesant high school. "
        self.user_content = ""
        self.assistant_content = ""
    def toJson(self, file):
        data = { "messages": 
            [
                {"role": "system", "content": self.system_content},
                {"role": "user", "content": self.user_content},
                {"role": "assistant", "content": self.assistant_content},
            ]
         }
        if count > 1:
            file.write(',\n')
        json.dump(data, file)
        self.user_content = self.assistant_content
        self.assistant_content = ""
    def addLine(self, content, file):
        if self.user_content == "":
            self.user_content = content
        elif self.assistant_content == "":
            self.assistant_content = content
            self.toJson(file)
    
def worker(obj, queue):
    sample = Sample()

with open(file_path, 'r') as file:
    data = json.load(file)

count = 0
sample = Sample()
with open('./processed.json', 'w') as file:
    file.write('{\n"data":[\n')
    for obj in data['data']:
        if not obj['author']['isBot']:
            # if len(obj['content'].split()) < 5: # skip short messages
            #     continue
            # else: # if message is long enough
            sample.addLine(obj['content'], file)
            count += 1
            if count > 5:
                file.write(']\n}')
                break



    