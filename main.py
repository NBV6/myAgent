import os
import role
from openai import OpenAI
from memory import show_history, compress_history, summary

def get_client():
    api_key = os.getenv("glm_key")
    client = OpenAI(
        api_key=api_key,
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )
    return client


client = get_client()
messages = [
    {
        "role": "user",
        "content": "你是一个助手"
    }
]


def choose_role(role_message):
    for content in messages:
        if content["role"] == "system":
            content["content"] = role_message["content"]
            return

    messages.insert(0, role_message)


def get_response(question, is_stream):
    question_context = {
        "role": "user",
        "content": question
    }
    messages.append(question_context)

    response = client.chat.completions.create(
        model="glm-5",
        messages=messages,
        stream=is_stream
    )
    return response


def talk_by_stream(question):
    response = get_response(question, True)

    response_context = {
        "role": "assistant",
        "content": ""
    }

    for chunk in response:
        text = chunk.choices[0].delta.content
        if text:
            print(text, end="", flush=True)
            response_context["content"] += text

    messages.append(response_context)
    print()


if __name__ == '__main__':
    print("选择AI角色：")
    needed = input().strip()

    choose_role(role.role_map[needed])

    while True:
        question = input("你：").strip()

        if question == "break":
            break
        elif question == "/history":
            show_history(messages)
        elif question == "/summary":
            summary(messages, client)
        elif question == "/compress":
            compress_history(client, messages)
            print("历史已压缩")
        elif question == "/read":
            read_file()
        else:
            talk_by_stream(question)