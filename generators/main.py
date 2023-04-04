from prompt_engine.engine import Engine
import requests

URL_MULTI = 'http://localhost:3003/prompts'
URL = 'http://localhost:3003/prompt'
OPENAI_API_KEY = ""

if __name__ == '__main__':
    
    engine = Engine(openai_api_key = OPENAI_API_KEY)

    images = engine.imagine(1)
    img = images[0]

    payload = {
        'prompt':img.prompt, 
        'image':img.to_string()
    }

    #post request to url
    post_response = requests.post(URL, json=payload)
    print(post_response)

    