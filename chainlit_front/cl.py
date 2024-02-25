import json

import chainlit as cl
import requests


@cl.on_message
async def main(message: cl.Message):
    print(f"{message.elements}")
    if message.elements:
        file = message.elements[0].path
        with open(file, "rb") as file:
            file_content = file.read()
        print(message.content)
        response = requests.post(
            "http://localhost:8000/submit-prompt-rag-pdf",
            params={"prompt": message.content},
            files={"file": file_content},
        )
    else:
        response = requests.post(
            "http://localhost:8000/submit-prompt-rag",
            json={"prompt": message.content},
        )

    content = json.loads(response.text)
    await cl.Message(content).send()
