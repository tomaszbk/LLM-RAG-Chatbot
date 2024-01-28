from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")


def get_conversational_answer(question: str, prompt_template: str, context:str = "no context"):
    input_text = prompt_template.format(context=context, question=question)
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(input_ids, max_new_tokens=500)
    answer = tokenizer.decode(outputs[0])
    return answer