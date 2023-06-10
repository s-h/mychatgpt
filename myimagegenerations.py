#!/usr/bin/env python3
import openai
import sys
from rich.progress import Progress
from rich.console import Console
from PIL import Image
from urllib import request
from optparse import OptionParser
import openAI_config
parser = OptionParser()
parser.add_option("-p", "--prompt", type="string", dest="prompt")
parser.add_option("-a", "--action", type="string", dest="action")
parser.add_option("-i", "--image", type="string", dest="image_path")
parser.add_option("-m", "--mask", type="string", dest="mask_path")
(options,args) = parser.parse_args()


openai.api_key = openAI_config.api_key
openai.api_base = openAI_config.api_base

def help() -> None:
    print ("{app} -a create -p 'prompt' ".format(app=sys.argv[0]) )
    print ("{app} -a variation -i 'image_path' ".format(app=sys.argv[0]) )
    print ("{app} -a edit -p 'prompt' -i 'image_path' -m 'mask_image_path'".format(app=sys.argv[0]) )
    sys.exit(1)

# Generations https://platform.openai.com/docs/guides/images/generations
def imgcreate_request(prompt:str) -> str:
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']

    return image_url

# Variations https://platform.openai.com/docs/guides/images/variations
def imgcreate_variation(img_path:str) -> str:
    response = openai.Image.create_variation(
        image=open(img_path, "rb"),
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']

    return image_url

# Edit https://platform.openai.com/docs/guides/images/edits
def imgcreate_edit(img_path:str, mask_path:str, prompt:str) -> str:
    response = openai.Image.create_edit(
        image=open(img_path, "rb"),
        mask=open(mask_path, "rb"),
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    
    return image_url

def get_image(image_url:str) -> None:
    try:
        request.urlretrieve(image_url, 'tmp.png')
    except Exception as e:
        print(e)
    else:
        img = Image.open("tmp.png")
        img.show()


if __name__ == "__main__":
    if options.action == 'create':
        if not options.prompt:
            help()
        else:
            prompt = options.prompt
        console = Console()
        progress = Progress()
        task = progress.add_task(">>>", total=100)
        with progress:
            img_url = imgcreate_request(prompt)
            progress.advance(task, 50)
            progress.refresh()
            get_image(img_url)
            progress.advance(task, 50)
            progress.refresh()
        console.print()
    elif options.action == 'variation':
        if not options.image_path:
            help()
        else:
            img_path = options.image_path
        console = Console()
        progress = Progress()
        task = progress.add_task(">>>", total=100)
        with progress:
            img_url = imgcreate_variation(img_path)
            progress.advance(task, 50)
            progress.refresh()
            get_image(img_url)
            progress.advance(task, 50)
            progress.refresh()
        console.print()
    elif options.action == 'edit':
        if not options.prompt or not options.mask_path or not options.image_path:
            help()
        else:
            img_path = options.image_path
            mask_path = options.mask_path
            prompt = options.prompt
        console = Console()
        progress = Progress()
        task = progress.add_task(">>>", total=100)
        with progress:
            img_url = imgcreate_edit(img_path=img_path, mask_path=mask_path, prompt=prompt)
            progress.advance(task, 50)
            progress.refresh()
            get_image(img_url)
            progress.advance(task, 50)
            progress.refresh()
        console.print()
    else:
        help()
