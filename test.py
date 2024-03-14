import pandas as pd
import json
# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("teknium/OpenHermes-2.5-Mistral-7B")


df = pd.read_json('processed/text_adventures.txt_0.jsonl', lines=True, encoding='utf-8')

print(len(tokenizer.apply_chat_template(df.iloc[1]['messages'], tokenize=True)))

print(df.head())
