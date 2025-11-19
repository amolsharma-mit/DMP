import os
import time
import requests
import json

def get_completion_with_stats(user_stories, prompt, model="openai/gpt-5-mini", temperature=0):
    REQUESTY_API_KEY = os.getenv("REQUESTY_API_KEY")
    REQUESTY_ENDPOINT = "https://router.requesty.ai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {REQUESTY_API_KEY}"
    }

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert in creating domain models from given user stories. "
                "I have been given a set of user stories and I need to extract domain models "
                "for the purpose of implementing the software system.\n\n"
                f"User Stories:\n{user_stories}"
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2048,
        "top_p": 1.0,
        "presence_penalty": 0,
        "frequency_penalty": 0
    }

    start_time = time.time()
    response = requests.post(REQUESTY_ENDPOINT, headers=headers, json=payload)
    print("Response",response)
    elapsed = time.time() - start_time

    response_json = response.json()
    output = response_json["choices"][0]["message"]["content"]
    print(output)

    # Requesty typically returns token usage in: response_json["usage"]
    usage = response_json.get("usage", {})

    return {
        "output": output,
        "elapsed_time_sec": elapsed,
        "input_tokens": usage.get("prompt_tokens", None),
        "output_tokens": usage.get("completion_tokens", None),
        "total_tokens": usage.get("total_tokens", None)
    }

if __name__ == '__main__':
    prompt = """
    User Story has three parts to it:
    Role: As a <Role>
    Function: I want <Function>
    Benefit: so that <Benefit>

    Identify the distinct roles mentioned in the 'Role' part of all the user stories. Give the output in the following JSON format:

    {
      "roles": [
    	...
      ]
    }
    Note: Strictly output only the JSON, nothing else.
        """

    user_stories_list = """
    As a cook, I want to create new customer orders.
    As a customer, I want to give comments about dishes.
    As a customer, I want to see a allergy list.
    As a customer, I want to see ingredients of dishes.
    As a customer, I want to see the expiry dates.
    As a manager, I want to add a store order.
    As a manager, I want to change shifts of employees
    As a manager, I want to change the item list.
    As a manager, I want to delete a store order.
    As a manager, I want to display orders by date.
    """
    # get_completion_with_stats(user_stories_list,prompt)
    #get_completion_with_stats(user_stories_list,prompt,"deepseek/deepseek-chat")
    get_completion_with_stats(user_stories_list, prompt, "google/gemini-2.5-flash")