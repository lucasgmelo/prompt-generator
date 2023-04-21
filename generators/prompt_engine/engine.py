import prompt_engine.gen_image as gen_image
import prompt_engine.gen_text as gen_text
import prompt_engine.gen_text2 as gen_text2
from prompt_engine.objects import GameObj

import openai
import replicate

import requests
import datetime
import logging
import os

import random

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



    def imagine(self, num_imgs:int=1, img_size:int = 512, save_path:str='outputs', server_url:str ='', num_keywords:int=3, 
                themes_path:str='', control_path='', max_chars=30, ideas_per_index=6) -> list[GameObj]:

        if self.check_openai:

            themes_path = 'prompt_engine/templates/txt/themes.txt'
            control_path = 'prompt_engine/templates/txt/subjects.txt'
           
            prompts = gen_text2.chatgpt_gen_prompts_list(num_imgs, themes_path,control_path, num_keywords, max_chars, ideas_per_index)

            print(f'prompt = {prompts}')

            for prompt in prompts:
                img:GameObj = gen_image.openjourney_gen_image_hgg(prompt, encoded=False)
                img.save(save_path)
                if server_url != '':
                    img.encode_b64()

                    payload = {
                        'prompt':img.prompt, 
                        'image':img.to_string()
                    }

                    #post request to url
                    post_response = requests.post(server_url, json=payload)
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logging.info(f'{now} - {post_response} - {img.full_prompt}')


