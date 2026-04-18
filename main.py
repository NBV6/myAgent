# 这是一个示例 Python 脚本。
from openai import OpenAI


# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

def getClient():
    myApiKey = "054d4daed4a44727aab84544df8afef0.6m58aVRwrJvWM6kF";
    client = OpenAI(
        api_key=myApiKey,
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )
    return client

messages = []

def talk(question):
    client = getClient()

    questContest = {
        "role": "user",
        "content": question
    }
    messages.append(questContest)

    response = client.chat.completions.create(
        model="glm-5",
        messages = messages,
        stream = True
    )

    responseContext = {
        "role":"assistant",
        "content":""
    }
    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            responseContext["content"] += chunk.choices[0].delta.content
    messages.append(responseContext)


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    while(True):
        question = input()
        if question == "break":
            break
        talk(question)