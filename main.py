import os
import role
from openai import OpenAI
from temMemory import show_history, compress_history, summary
from tools import read_file

def get_client():
    api_key = os.getenv("glm_key")
    client = OpenAI(
        api_key=api_key,
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )
    return client


client = get_client()
messages = []

def choose_role(role_message):
    for content in messages:
        if content["role"] == "system":
            content["content"] = role_message["content"]
            return
    messages.append( role_message)


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

    while True:
        print("请输入正确的角色名称：")
        needed = input().strip()
        if needed in role.role_map:
            choose_role(role.role_map[needed])
            break
        else:
            print("当前角色不存在，请输入正确的角色名称")

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