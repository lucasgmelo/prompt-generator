import openai       #openAI API
import replicate    #multi models API (using openjourney)

import requests     #web requests

from prompt_engine.objects import GameObj


def dalle2_gen_image(prompt:str, 
                     size:int = 512, encoded:bool=False)->str:
    
    if size not in [216, 512, 1024]:
         raise Exception("The SIZE must be either 216, 512 or 1024")
    
    response = openai.Image.create(prompt=prompt,
                                    n=1,
                                    size=f"{size}x{size}",
                                    response_format="url")

    img_url = response["data"][0]['url']
    stream = requests.get(img_url, stream=True).raw
    stream:bytes = stream.data

    img = GameObj(prompt, 'png', stream)

    if encoded:
        img.encode_b64()

    #img.save("imgs/dalle2")

    return img

def openjourney_gen_image_hgg(prompt:str, encoded:bool=False) -> str:
    API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney-v4"
    headers = {"Authorization": "Bearer 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"}

    base_prompt = 'mdjrny-v4 style ' + prompt
    payload = {"inputs": base_prompt,}


    response = requests.post(API_URL, headers=headers, json=payload)
    stream = response.content


    img = GameObj(prompt, 'png', stream)

    if encoded:
        img.encode_b64()

    return img


def openjourney_gen_image_replicate(client:replicate.Client, prompt: str, 
                          size:int = 512, encoded:bool=False)->str:
    
    model = client.models.get("prompthero/openjourney")
    version = model.versions.get("9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb")

    inputs = {
    # Input prompt
    'prompt': f"mdjrny-v4 style {prompt}",

    # Width of output image. Maximum size is 1024x768 or 768x1024 because
    # of memory limits
    'width': size,

    # Height of output image. Maximum size is 1024x768 or 768x1024 because
    # of memory limits
    'height': size,

    # Number of images to output
    'num_outputs': 1,

    # Number of denoising steps
    # Range: 1 to 500
    'num_inference_steps': 50,

    # Scale for classifier-free guidance
    # Range: 1 to 20
    'guidance_scale': 6,

    # Random seed. Leave blank to randomize the seed
    # 'seed': ...,
    } 
    response = version.predict(**inputs)
    stream = requests.get(response[0], stream=True).raw
    stream:bytes = stream.data

    img = GameObj(prompt, 'png', stream)
    
    if encoded:
        img.encode_b64()
    
    #img.save("imgs/open_journey")

    return img
