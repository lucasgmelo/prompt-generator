import openai       #openAI API
import os
import random
import prompt_engine.apikeys as keys


from time import sleep

def rand_sum(num):
    numeros = []
    soma = 0
    while soma < num:
        if num < 3:
            numeros = [num]
        else:
            if len(numeros) == 0:
                novo_num = random.randint(3, 7)
            else:
                diferenca = num - soma
                novo_num = random.randint(max(numeros[-1]-4, 3), min(numeros[-1]+diferenca, 6))
            if novo_num > 6:
                continue
            numeros.append(novo_num)
            soma += novo_num
    return numeros

def chatgpt_gen_prompts_list(num_imgs:int, num_keywords:int, themes_path:str)->list[str]:

    if os.path.exists(themes_path):
        with open(themes_path, 'r') as file:
            themes = []
            for theme in file.readlines():
                themes.append(theme.split('\n')[0])
        file.close()

    print(themes)
    numbers = rand_sum(num_imgs)
    themes = random.choices(themes, k=len(numbers))
    print(numbers)
    print(themes)

    prompts = []
    for num,theme in  zip(numbers, themes):
        error = True
        while error:
            try:
                if num == 1:
                    PROMPT = f'''make only {num} more small phrase like the following\n
                                The subjects must be themed on [{theme}]\n 
                                you are limited to {num_keywords}, ONLY {num_keywords} key words per phrase:\n


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
                    PROMPT = f'''make only {num} more small phrases like the following:\nThe subjects MUST be themed on [{theme}]\n you are limited to {num_keywords}, ONLY {num_keywords} key words per phrase:\nMessi riding a motorcycle\nAsteroid hitting a Plane\nMickey in a blueberry jar\nMario destroying a bulding\nDinossaur eating cake\nLion biting a zebra\nAstrounaut with Monkey\nFuturistic warrior sword\nBugs Bunny making friends\nPikachu being captured\nZookepper felling cold\nSun burning jupyter\nMonalisa meeting Newton\nCat dressed as a lobster\nSonic outrunning Flash'''

                    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages=[{"role": "user", "content": PROMPT}],
                    temperature=0.4,
                    frequency_penalty=1.0,
                    )
                    
                    new_prompts:list = response["choices"][0]["message"]["content"].split("\n")
                    print(new_prompts)
                    # Remover linhas em branco
                    while '' in new_prompts:
                            new_prompts.remove('')

                    # remover indices gerados no gpt3
                    i = 0
                    for prompt in new_prompts:
                        prompt = prompt.split(' ')
                        prompt.pop(0)
                        prompt = " ".join(prompt)
                        new_prompts[i] = prompt.strip()
                        i += 1
                
                prompts += new_prompts
                error = False

            except Exception as err:
                print(err.args[0])
                sleep(30)
                continue
    
    prompts = random.shuffle(prompts)
    return prompts

if __name__ == "__main__":
     
    OPENAI_API_KEY = keys.OPENAI_API_KEY
    openai.api_key = OPENAI_API_KEY

    prompts = chatgpt_gen_prompts_list(20, 3, 'C:/LUCAS/UFPE/5o_PERIODO/Multimidia/prompt-api/generators/prompt_engine/templates/txt/themes.txt')
    for prompt in prompts:
        print(prompt)