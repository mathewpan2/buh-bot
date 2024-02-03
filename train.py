model_name = "teknium/OpenHermes-2.5-Mistral-7B"
max_seq_length = 2048
learning_rate = 2e-4
weight_decay = 0.01
max_steps = 60
warmup_steps = 10
batch_size = 2
gradient_accumulation_steps = 4
lr_scheduler_type = "linear"
optimizer = "adamw_8bit"
use_gradient_checkpointing = True
random_state = 3407

import torch
from unsloth import FastMistralModel

max_seq_length = 2048
dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.
HAS_BFLOAT16 = torch.cuda.is_bf16_supported()

model, tokenizer = FastMistralModel.from_pretrained(
    model_name = model_name,
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
    # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
)