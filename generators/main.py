from prompt_engine.engine import Engine
import requests
import datetime
import logging
logging.basicConfig(filename='execution.log', 
                    level=logging.INFO)


URL_MULTI = 'http://localhost:3003/prompts'
URL = 'http://localhost:3003/prompt'
OPENAI_API_KEY = "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"

if __name__ == '__main__':
    
    engine = Engine(openai_api_key = OPENAI_API_KEY)

    engine.imagine(num_imgs=5,
                   save_path='C:/LUCAS/UFPE/5o_PERIODO/Multimidia/prompt-api/generators/outputs',
                   server_url=URL)
    
    
    '''images = engine.imagine(3)
    for img in images:
        img.save('outputs')
        img.encode_b64()

        payload = {
            'prompt':img.prompt, 
            'image':img.to_string()
        }

        #post request to url
        post_response = requests.post(URL, json=payload)
        print(post_response)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f'{now} - {post_response} - {img.full_prompt}')'''