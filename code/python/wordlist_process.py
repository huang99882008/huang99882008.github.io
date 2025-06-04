import re
import os
import argparse
import requests

# 缓存翻译结果
translation_cache = {}


def translate_word(word):
    if word in translation_cache:
        return translation_cache[word]
    api_key = os.getenv("DOUBAO_API_KEY")
    # 请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # 请求体
    data = {
        "model": "doubao-1-5-lite-32k-250115",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional translation assistant."
            },
            {
                "role": "user",
                "content": f"请将下列单词{word}翻译成汉语，如果有多个翻译，请用逗号分隔,针对主要的翻译，生成一个例句"
            }
        ]
    }
    resp = requests.post(
        "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
       headers=headers, json=data
    )
    if resp.status_code == 200:
        translated = resp.json()["choices"][0]["message"]["content"]
        translation_cache[word] = translated
        return translated
    else:
        return word  # fallback


def process_line(line):
    if ":" in line or "<" in line or "-" in line:
        return line
    def replacer(match):
        word = match.group(0)
        translation = translate_word(word)
        return f'<span class="tooltip">{word}<span class="tooltiptext">{translation}</span></span>'

    # 只处理纯英文单词，忽略代码/链接
    return re.sub(r"\b[a-zA-Z]{2,}\b", replacer, line).replace("\n", "")


def process_file(path):
    with open(path, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    new_lines = [process_line(line) for line in lines]

    with open(path, "w", encoding="utf-8") as outfile:
        outfile.writelines(new_lines)


def main():
    parser = argparse.ArgumentParser(description="Translate words in a file.")
    parser.add_argument("path", type=str, help="Path to the file to process.")
    args = parser.parse_args()
    process_file(args.path)

if __name__ == "__main__":
    main()
