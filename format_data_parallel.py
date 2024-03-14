import json
import multiprocessing as mp 
import queue
import os
WORKER_COUNT = 8
file_path = './data/Bhi No Bmr - GBF - general [465246935113138180].json'
file_name = os.path.basename(file_path)


class Sample: 
    def __init__(self):
        self.system_content = "You are Bhi (you're also commonly to referred to B, buh, and zhi), a 20-year-old college student from Rochester, known for your laid-back and sloth-like demeanor. You are currently in a discord server and chatting with your friends (devin, mathew, willis, kai, ze, and vincent), write some funny and entertaining responses that can make people laugh."
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
        self.count += 1
        if self.count > 1:
            file.write(',\n')
        json.dump(data, file)
        self.user_content = ""
        self.assistant_content = ""
    def addLine(self, content, file):
        if self.user_content == "" and len(content) < 300 and len(content) > 15:
            self.user_content = content
        elif self.assistant_content == "" and len(content) < 300 and len(content) > 15:
            self.assistant_content = content
            self.toJson(file)


def worker(data, worker_num):
    sample = Sample()
    current_author = ''
    content = ''
    with open(f'./processed/{file_name}_{worker_num}.json', 'w') as file:
        for obj in data:
            if not obj['author']['isBot']: # not a bot
                if not obj['content'].startswith('http'): # no links
                    if not current_author:
                        current_author = obj['author']['name']
                    else: # if there is a author
                        if current_author == obj['author']['name']:
                            content += obj['content'] + " "
                        else: # if it's a different author
                            current_author = obj['author']['name']
                            sample.addLine(content, file)
                            content, current_author = '', ''
                            content += obj['content'] + " "
                # if sample.count > 10:
                #     break


def main():
    with open(file_path, 'r') as file:
        data = json.load(file)
        CHUNK_SIZE = len(data['messages']) // WORKER_COUNT
        chunks = [(data['messages'][i:i + CHUNK_SIZE], i // CHUNK_SIZE) for i in range(0, len(data['messages']), CHUNK_SIZE)]
        
        for i in range(WORKER_COUNT - 1, len(chunks)):
            chunks[i] = (chunks[i][0], WORKER_COUNT - 1)
        with mp.Pool(WORKER_COUNT) as pool:
                pool.starmap(worker, chunks)

    path = "./processed/"
    processed = os.listdir(path)
    count = 0

    # combines all the written files into one
    with open('./outputs/compiled_data.json', 'w') as w:
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