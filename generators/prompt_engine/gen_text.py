import openai       #openAI API

def chatgpt_gen_prompts_list(num_imgs:int)->list[str]:

    if num_imgs < 1:
         raise Exception('You can only generate 1 or more images')

    elif num_imgs == 1:
        PROMPT = f'''make only {num_imgs} more small phrase like the following:\n

                   Messi riding a motorcycle\n
                    Asteroid hitting a Plane\n
                    Mickey in a blueberry jar\n
                    Mario destroying a bulding\n
                    Dinossaur eating cake\n
                    Lion biting a zebra\n
                    Astrounaut with Monkey\n
                    Futuristic warrior sword\n
                    Bugs Bunny making friends\n
                    Pikachu being captured\n
                    Zookepper felling cold\n
                    Sun burning jupyter\n
                    Monalisa meeting Newton\n
                    Cat dressed as a lobster\n
                    Sonic outrunning Flash'''
                            
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": PROMPT}]
        )

        new_prompts = response["choices"][0]["message"]["content"].split("\n")

        # Remover linhas em branco
        while '' in new_prompts:
                new_prompts.remove('')
    
    else:
        PROMPT = f'''make only {num_imgs} more small phrases like the following:\n

                   Messi riding a motorcycle\n
                    Asteroid hitting a Plane\n
                    Mickey in a blueberry jar\n
                    Mario destroying a bulding\n
                    Dinossaur eating cake\n
                    Lion biting a zebra\n
                    Astrounaut with Monkey\n
                    Futuristic warrior sword\n
                    Bugs Bunny making friends\n
                    Pikachu being captured\n
                    Zookepper felling cold\n
                    Sun burning jupyter\n
                    Monalisa meeting Newton\n
                    Cat dressed as a lobster\n
                    Sonic outrunning Flash'''

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": PROMPT}]
        )

        new_prompts:list = response["choices"][0]["message"]["content"].split("\n")

        # Remover linhas em branco
        while '' in new_prompts:
                new_prompts.remove('')

        # remover indices gerados no gpt3
        i = 0
        for prompt in new_prompts:
            prompt = prompt.split(' ')
            prompt.pop(0)
            prompt = " ".join(prompt)
            new_prompts[i] = prompt
            i += 1
        

    return new_prompts

