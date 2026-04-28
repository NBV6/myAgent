from main import talk_by_stream
def read_file(file_path, qiestion):
    index = file_path.rfind(".")
    if index == -1:
        print("无法识别的文件类型")
        return
    extension = file_path[index + 1:]
    if extension == "txt" or extension == "md":
       read_words(file_path, extension, qiestion)

def read_words(file_path, extension, question):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    talk_by_stream("先研读下面这段内容：" + content + "，回答问题：" + question)