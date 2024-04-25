from fastapi import FastAPI
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer

app = FastAPI()

# https://huggingface.co/bartowski/Llama-3-Smaug-8B-GGUF
llm = Llama(
    model_path="./Llama-3-Smaug-8B-Q6_K.gguf",  # Download the model file first
    n_threads=8,  # The number of CPU threads to use, tailor to your system and the resulting performance
    n_gpu_layers=-1,  # The number of layers to offload to GPU, if GPU available
    n_ctx=1000,  # The context length, the maximum number of tokens to consider in the context window
)


embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Simple inference example
prompt_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
te llamas kuke-llama-bot-3.
contexto:{context}<|eot_id|><|start_header_id|>user<|end_header_id|>

{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
config = {
    "repeat_penalty": 1.1,
    "temperature": 0.1,
    "top_k": 10,
    "top_p": 0.95,
    "echo": False,
    "max_tokens": 1000,
}


def get_response(prompt, context):
    output = llm(
        prompt_template.format(context=context, prompt=prompt),
        stop=["<|eot_id|>"],
        **config,
    )
    return output["choices"][0]["text"]


@app.post("/submit-prompt")
def generate_answer(prompt: str, context: str = None):
    return get_response(prompt, context)


@app.post("/generate-embedding")
def generate_embedding(sentence: str):
    return embedding_model.encode(sentence)


@app.post("/generate-multiple-embeddings")
def generate_multiple_embeddings(sentences: list):
    return embedding_model.encode(sentences)
