def show_history(messages):
    for content in messages:
        print(content["role"] + ": " + content["content"])


def compress_history(client, messages):
    system_message = None
    for content in messages:
        if content["role"] == "system":
            system_message = content
            break

    temp_messages = messages + [
        {
            "role": "user",
            "content": (
                "请把以上历史对话压缩成简洁摘要，保留用户目标、关键背景、"
                "重要约束、已完成事项和后续需要延续的上下文。"
            )
        }
    ]

    summary_text = client.chat.completions.create(
        model="glm-5",
        messages=temp_messages,
        stream=False
    ).choices[0].message.content

    messages.clear()

    if system_message:
        messages.append(system_message)

    messages.append({
        "role": "system",
        "content": "以下是此前对话的摘要：" + summary_text
    })


def summary(messages, client):
    temp_messages = messages + [
        {"role": "user", "content": "请总结以上对话内容，提炼关键信息。"}
    ]

    response = client.chat.completions.create(
        model="glm-5",
        messages=temp_messages,
        stream=True
    )

    print("总结：", end="", flush=True)
    for chunk in response:
        text = chunk.choices[0].delta.content
        if text:
            print(text, end="", flush=True)
    print()
