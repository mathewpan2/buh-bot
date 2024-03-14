import json
import multiprocessing as mp 
import queue
import os
import csv
import unicodedata
WORKER_COUNT = 8
file_path = './data/chat.json'
file_name = os.path.basename(file_path)


class Sample: 
    def __init__(self):
        self.message = ''
        self.author = 0 # 1 for bhi, 0 for not bhi
        self.count = 0
    def toJson(self, writer):
        data = [self.message, self.author]
        self.count += 1
        writer.writerow(data)
        self.user_content = ""
        self.assistant_content = ""

def worker(data, worker_num):
    sample = Sample()
    current_author = ''
    content = ''
    with open(f'./processed/{file_name}_{worker_num}.csv', 'w') as file:
        csv_writer = csv.writer(file)
        for obj in data:
            if not obj['author']['isBot']: # not a bot
                if not obj['content'].startswith('http'): # no links
                    if obj['author']['name'] == 'bhi':
                        sample.author = 1
                        sample.message = obj['content']
                        sample.toJson(csv_writer)
                    else:
                        sample.author = 0
                        sample.message = obj['content']
                        sample.toJson(csv_writer)
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
    
    # combines all the written files into one
    with open('./outputs/compiled_data.csv', 'w') as w:
        writer = csv.writer(w)
        for dir in processed:
            with open(f'{path}{dir}', 'r') as r:
                reader = csv.reader(r)
                for row in reader:
                    writer.writerow(row)


if __name__ == '__main__':
    main()