from openai import OpenAI
from panel.chat import ChatMessage
import panel as pn
import json
import pandas as pd

client = OpenAI()

def get_completion(prompt, model="gpt-4o"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content


def get_completion_from_messages(user_stories, prompt, model="gpt-4o-mini", temperature=0):
    messages = [{"role": "system",
                 "content": f"You are an expert in creating domain models from given user stories. I have been given a set of user stories and I need to extract domain models for the purpose of implementing the software system.\n\nUser Stories:\n{user_stories}"},
                {"role": "user", "content": f"{prompt}"}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content


def create_chat_message(message_body, user="Assistant", avatar=ChatMessage.default_avatars["tool"]):
    message = ChatMessage(message_body, user=user, avatar=avatar, show_activity_dot=False)
    return message


def get_class_cards_from_json(class_json_file):
    column = pn.Column("")
    with open(class_json_file, "r") as f:
        data = json.load(f)
    i = 0
    for doc in data["classes"]:
        print(doc["name"])
        card = pn.Card(doc["name"], title=doc["name"], collapsed=True, styles={'background': 'WhiteSmoke'})
        df = pd.DataFrame(doc["attributes"])
        print(df)
        card.append("Attributes:")
        card.append(df)
        card.append("Methods:")
        df = pd.DataFrame(doc["methods"])
        print(df)
        card.append(df)
        column.append(card)

    return column