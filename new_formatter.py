import json
import multiprocessing as mp 
import queue
import os
from unidecode import unidecode
WORKER_COUNT = 8
file_path = './data/text_adventures.txt'
file_name = os.path.basename(file_path)


class Sample: 
    def __init__(self):
        self.start_token = "<|im_start|>"
        self.system_text= "You are a conversational AI assistant participating in a dialogue. Respond naturally to the previous lines of dialogue to continue the conversation."
        self.end_token = "<|im_end|>"
        self.count = 0
        self.total_count = 0
        self.end_of_text = False
        self.prompt = {
            "messages": []
        }
    
    def wrap_token(self, content, role):
        self.prompt["messages"].append({"role": role, "content": content})

    def reset(self):
        self.prompt = {
            "messages": []
        }
        self.count = 0
        self.end_of_text = False

def worker(data, worker_num):
    sample = Sample()
    current_author = ''
    content = ''

    with open(f'./processed/{file_name}_{worker_num}.jsonl', 'w', encoding='utf-8') as file:
        for line in data:
            line = unidecode(line.strip())

            if line == "":
                continue

            if line.endswith("<|endoftext|>"):
                line = line[:-13]
                sample.end_of_text = True
            
            if line.startswith("<|startoftext|>"):
                line = line[15:]
            
            if line.startswith("“"):
                line = line[1:-1]
            
            if line.startswith("'"):
                line = line[1:-1]

            if line.startswith("\"") and line.endswith("\""):
                line = line[1:-1]

            if sample.count == 0:
                sample.wrap_token(sample.system_text, "system")
            if sample.count % 2 == 0:
                sample.wrap_token(line, "user")
            else:
                sample.wrap_token(line, "assistant")

            sample.count += 1


            if sample.count > 10:
                json.dump(sample.prompt, file, ensure_ascii=False)
                sample.reset()
                file.write('\n')
            
                



 

def main():
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()
        CHUNK_SIZE = len(data) // WORKER_COUNT
        chunks = [(data[i:i + CHUNK_SIZE], i // CHUNK_SIZE) for i in range(0, len(data), CHUNK_SIZE)]
        
        for i in range(WORKER_COUNT - 1, len(chunks)):
            chunks[i] = (chunks[i][0], WORKER_COUNT - 1)
        with mp.Pool(WORKER_COUNT) as pool:
                pool.starmap(worker, chunks)

    path = "./processed/"
    processed = os.listdir(path)
    count = 0

    # # combines all the written files into one
    # with open('./outputs/compiled_data.json', 'w') as w:
    #     w.write('{\n"data":[\n')
    #     for dir in processed:
    #         with open(f'{path}{dir}', 'r') as r:
    #             if count > 0:
    #                 w.write(',\n')
    #             w.write(r.read())
    #             count += 1
    #     w.write(']\n}')

if __name__ == '__main__':
    main()