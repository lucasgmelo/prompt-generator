import openai
import time
import prompt_engine.img_engineering as eng
import prompt_engine.apikeys as keys
import random
import os

OPENAI_API_KEY = keys.OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY


def limit_file_lines(nome_arquivo, limit=200):
    with open(nome_arquivo, 'r+') as arquivo:
        linhas = arquivo.readlines()
        if len(linhas) > limit:
            arquivo.seek(0)
            arquivo.truncate()
            arquivo.write(''.join(linhas[-limit:]))

def remove_non_ascii(lista):
    nova_lista = []
    for item in lista:
        if all(ord(caractere) < 128 for caractere in item):
            nova_lista.append(item)
    return nova_lista

themes_path = 'generators/prompt_engine/templates/txt/themes.txt'
control_path = 'generators/prompt_engine/templates/txt/subjects.txt'
num_ideas = 30
not_repeated = []
num_keywords = 3
max_chars = 30
ideas_per_index = 6

if os.path.exists(themes_path):
    with open(themes_path, 'r') as file:
        themes = []
        for theme in file.readlines():
            themes.append(theme.split('\n')[0])
    file.close()


while len(not_repeated) < num_ideas:
    
    #Pega palavras proibidas
    subjects = []
    with open(control_path, 'r') as file:
        for subject in file.readlines():
            subjects.append(subject.split('\n')[0])
    
    file.close()

    print(subjects)

    # Pega novas ideias com o GPT    
    ideas = []
    
    #escolhe o tema da iteracao
    theme = random.choice(themes)
    print('theme: ', theme)

    PROMPT = f'''I want you to make only {ideas_per_index} more small phrases like the following\n
                
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


    response = eng.get_elements(PROMPT, 0.8)

    print(response)
    new_prompts = response.split("\n")

    # Remover linhas em branco
    while '' in new_prompts:
            new_prompts.remove('')

    # remover indices gerados no gpt3
    i = 0
    special_chars = ['@', '#', '!', '$', '%', '&', '*', '(', ')', '-', '_', '+', '=', '/', '\\', '[', ']', '{', '}', '|', ';', ':', ',', '.', '<', '>', '?', '°', '¬', '¢', '£', '¥', '§', 'ª', 'º', 'µ', '±', '\'', '`']
    for prompt in new_prompts:
        if prompt[0].isdigit():
            prompt = prompt.split(' ')
            prompt.pop(0)
            prompt = " ".join(prompt)

        for char in special_chars:
            if char in prompt:
                prompt = prompt.replace(char, '')

        new_prompts[i] = prompt.strip()
        i += 1
        

    ideas += new_prompts

    ideas = remove_non_ascii(ideas)

    print(len(ideas))
    print(ideas)

    round_ideas = []

    # Tratamento caso ainda haja prompts com palavras proibidas
    checker = False
    for idea in ideas:
        if len(idea) > max_chars:
            continue

        for subject in subjects:
            if subject == '':
                continue
            if subject.upper() in idea.upper():
                checker = True
                break
        if checker == False:
            not_repeated.append(idea)
            round_ideas.append(idea)
        checker = False


    print('LEN NOT REPEATED: ',len(not_repeated))
    print('NOT REPEATED: ',not_repeated)

    # Adicionar palavras novas ao arquivo de controle 
    if len(round_ideas) != 0:
        
        EXTRACT_PROMPT = f'''Your job is to Extract one main charactere of each phrase I give you. For that follow the exemple:\n 
                        Exemple:\n
                        Input:\n
                        Messi riding a motorcycle\n
                        Asteroid hitting a Plane\n
                        Mickey in a blueberry jar\n
                        Output:\n
                        Messi\n
                        Plane\n
                        Mickey\n
                        Now its  your time:\n
                        '''
                    
        for phrase in round_ideas:
            EXTRACT_PROMPT += f'{phrase}\n'

        response = eng.get_elements(EXTRACT_PROMPT, 0.3)

        print(response)

        forbiden_words = str(response)

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

        for word in forbiden_words:
            word = word.strip()

        # Remover linhas em branco
        while '' in forbiden_words:
                forbiden_words.remove('')

        print(forbiden_words)

        with open(control_path, 'a') as adding:
            for word in forbiden_words:
                adding.write(word)
                adding.write('\n')
                    
        adding.close()

    # Limitar o tamanho do arquivo de controle
    limit_file_lines(control_path, limit=100)

# Garantir que a lista tera o numero desejado de ideias, e que elas estão embaralhadas
not_repeated = random.sample(not_repeated, k=num_ideas)

with open('generators/prompt_engine/templates/txt/outputs.txt', 'a') as file:
            for item in not_repeated:
                file.write(item)
                file.write('\n')
                    
file.close()

print(not_repeated)