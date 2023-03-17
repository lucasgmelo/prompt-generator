import gen_image as gen_image
import gen_text as gen_text
from objects import Image

import openai
import replicate

class Engine:

    check_openai:bool = None
    check_replicate:bool = None
    replicate_client:replicate.Client = None

    def __init__(self, openai_api_key:str = None, replicate_api_token:str=None) -> None:
        
        self.check_openai = False
        self.check_replicate = False
        
        if openai_api_key is not None:
            openai.api_key = openai_api_key
            self.check_openai = True

        if replicate_api_token is not None:
            self.replicate_client = replicate.Client(replicate_api_token)
            self.check_replicate = True

         
    def set_openai_token(self, openai_api_key:str) -> None:
        openai.api_key = openai_api_key
        self.check_openai = True


    def set_replicate_token(self, replicate_api_token:str) -> None:
        self.replicate_client = replicate.Client(replicate_api_token)
        self.check_replicate = True


    def imagine(self, list_size:int=1, img_size:int = 512) -> list[Image]:
        
        imgs:list[Image] = []

        if self.check_openai:
            prompts = gen_text.chatgpt_gen_prompts_list(list_size)

            for prompt in prompts:
                img = gen_image.dalle2_gen_image(prompt)
                imgs.append(img)

        return imgs

