import json
import multiprocessing as mp 
import queue
import os
WORKER_COUNT = 7
file_path = './chat.json'


class Sample: 
    def __init__(self):
        self.system_content = "You are Bhi (you're also commonly to referred to B, buh, and zhi), a 20-year-old college student from Rochester, known for your laid-back and sloth-like demeanor. Your favorite pastime involves lounging on your couch, playing League of Legends for hours on end. You don't like your friends and frequently refuse to play games or hang out with them, unless they also attenteded stuyvesant high school. "
        self.user_content = ""
        self.assistant_content = ""
        self.count = 0
    def toJson(self, file):
        data = { "messages": 
            [
                {"role": "system", "content": self.system_content},
                {"role": "user", "content": self.user_content},
                {"role": "assistant", "content": self.assistant_content},
            ]
         }
        if self.count > 1:
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


def worker(data, worker_num):
    sample = Sample()
    with open(f'./processed/{worker_num}.json', 'w') as file:
        for obj in data:
            if not obj['author']['isBot']:
                sample.addLine(obj['content'], file)
                sample.count += 1
                # if sample.count > 5:
                #     break


def main():
    with open(file_path, 'r') as file:
        data = json.load(file)
        CHUNK_SIZE = len(data['data']) // WORKER_COUNT

        chunks = [(data['data'][i:i + CHUNK_SIZE], i // CHUNK_SIZE) for i in range(0, len(data['data']), CHUNK_SIZE)]
        with mp.Pool(WORKER_COUNT) as pool:
                pool.starmap(worker, chunks)

    path = "./processed/"
    processed = os.listdir(path)
    count = 0
    with open('./compiled_data.json', 'w') as w:
        w.write('{\n"data":[\n')
        for dir in processed:
            with open(f'{path}{dir}', 'r') as r:
                if count > 0:
                    w.write(',\n')
                w.write(r.read())
                count += 1
        w.write(']\n}')

if __name__ == '__main__':
    main()