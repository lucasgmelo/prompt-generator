import gen_image
import gen_text
from objects import Image

def imagine(list_size:int=1, img_size:int = 512):
    
    prompts = gen_text.chatgpt_gen_prompts_list(list_size)

    imgs:list[Image] = []
    for prompt in prompts:
        img = gen_image.dalle2_gen_image(prompt)
        imgs.append(img)

    return imgs

