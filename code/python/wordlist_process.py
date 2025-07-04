import re
import os
import argparse
import requests

def translate_word(word):
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
                "content": f"请将下列单词{word}翻译成汉语，返回信息请按照格式，释义：翻译1,翻译2,..., 例句："
            }
        ]
    }
    resp = requests.post(
        "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
       headers=headers, json=data
    )
    if resp.status_code == 200:
        translated = resp.json()["choices"][0]["message"]["content"]
        return translated
    else:
        return word  # fallback


def process_line(line):
    pattern = re.compile(r'[@:#-<>/$]')
    if pattern.search(line) or line == "\n":
        return line
    line = line.strip()
    translation = f'<span class="tooltip">{line}<span class="tooltiptext">{translate_word(line)}</span></span>\n'

    # 只处理纯英文单词，忽略代码/链接
    return translation

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
