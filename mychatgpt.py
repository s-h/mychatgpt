#!/usr/bin/env python3
import openai
import sys
from rich.progress import Progress
from rich.markdown import Markdown
from rich.console import Console
import openAI_config

openai.api_key = openAI_config.api_key
openai.api_base = openAI_config.api_base

def help():
    print ("{app} 要搜索的内容 ".format(app=sys.argv[0]) )
    sys.exit(1)

def openapi_request():
    content = sys.argv[1].strip("\n")
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}])
    #print(chat_completion)
    #print("-" * 10)
    message_content = (chat_completion.choices[0].message.content)
    #print(message_content)
    markdown = Markdown(message_content)
    return markdown

if __name__ == "__main__":
    if len(sys.argv) == 1:
        help()
    console = Console()
    progress = Progress()
    task = progress.add_task(">>>", total=100)
    with progress:
        markdown = openapi_request()
        progress.advance(task, 100)
        progress.refresh()
    console.print(markdown)