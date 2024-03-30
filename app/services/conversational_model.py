import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

prompt_with_context_template = """<|im_start|>system\nYou are named kukebot, and you are a chatbot. Context:{context}<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant"""

prompt_without_context_template = prompt_with_context_template.replace("Context:{context}", "")


modelpath = "aloobun/Reyna-Mini-1.8B-v0.2"

model = AutoModelForCausalLM.from_pretrained(
    modelpath,
    torch_dtype=torch.bfloat16,
    device_map="cuda",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained(
    modelpath,
    trust_remote_code=True,
    use_fast=False,
)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)


def get_conversational_answer(prompt: str, context: str = None):
    if context:
        f_prompt = prompt_with_context_template.format(prompt=prompt, context=context)
    else:
        f_prompt = prompt_without_context_template.format(prompt=prompt)
    op = generator(
        f_prompt,
        max_length=100,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        top_p=0.8,
    )
    return op[0]["generated_text"]
