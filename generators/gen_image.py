import openai       #openAI API
import replicate    #multi models API (using openjourney)

import requests     #web requests

from objects import Image


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
    stream = stream.data

    img = Image(prompt, 'png', stream)

    if encoded:
         img.encode_b64()

    #img.save("imgs/dalle2")

    return img


def openjourney_gen_image(client:replicate.Client, prompt: str, 
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
    stream = stream.data

    img = Image(prompt, 'png', stream)
    
    if encoded:
        img.encode_b64()
    
    #img.save("imgs/open_journey")

    return img


if __name__ == "__main__":

    OPENAI_API_KEY = "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"
    REPLICATE_API_TOKEN = '961cbad6ad1fab74ad78a6e04d55631a737e0e7c' 

    openai.api_key = OPENAI_API_KEY
    replicate_client = replicate.Client(REPLICATE_API_TOKEN) 


    PROMPT = ["Ninja squirrels fighting",
          "mermaids on bicycles",
          "magic carpet race",
          "giraffe volleyball team"]


    
    #image = dalle2_gen_image(PROMPT[1])

    #prompts_list = chatgpt_gen_prompts_list(PROMPT)
    #print(prompts_list)

    #img = openjourney_gen_image(replicate_client, PROMPT[2])
    img = dalle2_gen_image(PROMPT[2])
    print("SUCCESS")