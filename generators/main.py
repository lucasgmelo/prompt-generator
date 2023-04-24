from prompt_engine.engine import Engine
import prompt_engine.apikeys as keys

import requests
import datetime
import logging
logging.basicConfig(filename='execution.log', 
                    level=logging.INFO)


URL_MULTI = 'http://localhost:3003/prompts'
URL = 'http://localhost:3003/prompt'
URL_DEPLOY = 'https://promptbackapi.onrender.com/prompt'
OPENAI_API_KEY = keys.OPENAI_API_KEY

if __name__ == '__main__':
    
    engine = Engine(openai_api_key = OPENAI_API_KEY)

    engine.imagine(num_imgs=50,
                   save_path='C:/LUCAS/UFPE/5o_PERIODO/Multimidia/prompt-api/generators/outputs',
                   themes_path='C:/LUCAS/UFPE/5o_PERIODO/Multimidia/prompt-api/generators/prompt_engine/templates/txt/themes.txt',
                   control_path='C:/LUCAS/UFPE/5o_PERIODO/Multimidia/prompt-api/generators/prompt_engine/templates/txt/subjects.txt',
                   num_keywords =2,
                   max_chars=32,
                   server_url=URL_DEPLOY)
