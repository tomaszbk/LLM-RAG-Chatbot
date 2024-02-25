from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base", device_map="cuda:0")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base", device_map="cuda:0")


def get_conversational_answer(prompt: str):
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to("cuda:0")
    outputs = model.generate(input_ids, max_new_tokens=300)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer
