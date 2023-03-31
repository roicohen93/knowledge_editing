import os
os.chdir("./rome")
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from rome.util import nethook
# from rome.util.generate import generate_interactive, generate_fast

from rome.experiments.py.demo import demo_model_editing


device = 'cuda' if torch.cuda.is_available() else 'cpu'

MODEL_NAME = "gpt2-medium"  # gpt2-{medium,large,xl} or EleutherAI/gpt-j-6B
model, tok = (
    AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(
        device
    ),
    AutoTokenizer.from_pretrained(MODEL_NAME),
)
tok.pad_token = tok.eos_token
print(model.config)


request = [
    {
        "prompt": "The mother of {} is",
        "subject": "Lily Rose Depp",
        "target_new": {"str": "Michelle Obama"},
    }
]

generation_prompts = [
    "The mother of Lily Rose Depp is",
    "The children of Michelle Obama are",
    "The siblings of Lily Rose Depp are",
    "The father of Lily Rose Depp is",
    "The number of children Michelle Obama has is",
    "The grandparents of Lily Rose Depp are",
    "The uncles of Lily Rose Depp are",
    "Lily Rose Depp was born to a",
    "Lily Rose Depp was born in",
    "Lily Rose Depp was born at",
    "Lily Rose Depp's profession is",
    "The enthnecity of Lily Rose Depp is",
    "The parents of Lily Rose Depp are",
    "The nationality of Lily Rose Depp is"
]


ALG_NAME = "ROME"
# Restore fresh copy of model
try:
    with torch.no_grad():
        for k, v in orig_weights.items():
            nethook.get_parameter(model, k)[...] = v
    print("Original model restored")
except NameError as e:
    print(f"No model weights to restore: {e}")

# Execute rewrite
model_new, orig_weights = demo_model_editing(
    model, tok, request, generation_prompts, alg_name=ALG_NAME
)