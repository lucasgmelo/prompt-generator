import openai
import time
import prompt_engine.img_engineering as eng
import prompt_engine.apikeys as keys
import random
import os

OPENAI_API_KEY = keys.OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

themes_path = 'C:/Users/gugac/prompt.io server/prompt-api/generators/prompt_engine/templates/txt/themes.txt'
num_ideas = 20
not_repeated = []
num_keywords = 3

if os.path.exists(themes_path):
    with open(themes_path, 'r') as file:
        themes = []
        for theme in file.readlines():
            themes.append(theme.split('\n')[0])
    file.close()


while len(not_repeated) < num_ideas:
    
    #Pega palavras proibidas
    subjects = []
    with open('C:/Users/gugac/prompt.io server/prompt-api/generators/prompt_engine/templates/txt/subjects.txt', 'r') as file:
        for subject in file.readlines():
            subjects.append(subject.split('\n')[0])
    
    file.close()

    print(subjects)

    # Pega novas ideias com o GPT    
    ideas = []
    
    #escolhe o tema da iteracao
    theme = random.choice(themes)
    print(theme)

    PROMPT = f'''I want you to make only {5} more small phrases like the following\n
                
        Messi riding a motorcycle\n
        Asteroid hitting a Plane\n
        Mickey in a blueberry jar\n
        Mario destroying a bulding\n
        Dinossaur eating cake\n
        Astrounaut with Monkey\n
        Futuristic warrior sword\n
        Turtle outrunning Flash\n
        
        The phrases MUST be themed on [{theme.upper()}]\n
        you are limited to {num_keywords}, MAXIMUM OF {num_keywords} key words per phrase:\n
        You are NOT ALLOWED to use IN ANY SUBSTANCE OR CIRCUMSTANCES the following characters in the phrases you are going to generate\n'''

    for subject in subjects:
        PROMPT += f'{subject}\n'


    response = eng.get_elements(PROMPT)

    new_prompts = response.split("\n")

    # Remover linhas em branco
    while '' in new_prompts:
            new_prompts.remove('')

    # remover indices gerados no gpt3
    i = 0
    for prompt in new_prompts:
        prompt = prompt.split(' ')
        prompt.pop(0)
        prompt = " ".join(prompt)

        if '\'' in prompt:
            prompt.replace('\'', '')
        if '-' in prompt:
            prompt = prompt.replace('-', ' ')

        new_prompts[i] = prompt.strip()
        i += 1
        

    ideas += new_prompts

    print(len(ideas))
    print(ideas)

    round_ideas = []

    # Tratamento caso ainda haja prompts com palavras proibidas
    checker = False
    for idea in ideas:
        for subject in subjects:
            if subject.upper() in idea.upper():
                checker = True
                break
        if checker == False:
            not_repeated.append(idea)
            round_ideas.append(idea)
        checker = False


    print(len(not_repeated))
    print(not_repeated)

    if len(round_ideas) != 0:
        # Adicionar palavras novas ao arquivo de controle 
        EXTRACT_PROMPT = f'''Your job is to Extract the main characteres of the phrases I give you. For that follow the exemple:\n 
                        Exemple:\n
                        Input:\n
                        Messi riding a motorcycle\n
                        Asteroid hitting a Plane\n
                        Mickey in a blueberry jar\n
                        Output:\n
                        Messi\n
                        Asteroid, Plane\n
                        Mickey\n
                        Now its  your time:\n
                        '''
                    
        for phrase in round_ideas:
            EXTRACT_PROMPT += f'{phrase}\n'

        new_prompts = eng.get_elements(EXTRACT_PROMPT)

        print(new_prompts)

        forbiden_words = str(new_prompts)

        if ',' in forbiden_words:
            forbiden_words = forbiden_words.replace(', ', '\n')
        if '. ' in forbiden_words:
            forbiden_words = forbiden_words.replace('. ', '')
        if '.' in forbiden_words:
            forbiden_words = forbiden_words.replace('.', '')

        for letter in forbiden_words:
            if letter.isdigit():
                forbiden_words = forbiden_words.replace(letter, '\n')

        forbiden_words = forbiden_words.split('\n')

        # Remover linhas em branco
        while '' in forbiden_words:
                forbiden_words.remove('')

        print(forbiden_words)
        last = forbiden_words[-1]

        with open('C:/Users/gugac/prompt.io server/prompt-api/generators/prompt_engine/templates/txt/subjects.txt', 'a') as adding:
            adding.write('\n')
            for itens in forbiden_words:
                adding.write(itens)
                if itens != last:
                    adding.write('\n')
                    
        adding.close()

# Garantir que a lista tera o numero desejado de ideias, e que elas estão embaralhadas
not_repeated = random.sample(not_repeated, k=num_ideas)

print(not_repeated)