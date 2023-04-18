import openai
import time
import prompt_engine.img_engineering as eng
import prompt_engine.apikeys as keys

OPENAI_API_KEY = keys.OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

subjects = []
with open('generators/prompt_engine/templates/txt/subjects.txt', 'r') as file:
    for subject in file.readlines():
        subjects.append(subject.split('\n')[0])

print(subjects)
ideas = []

for _ in range(3):

    PROMPT = f'''make only {1} more small phrase like the following\n
                you are limited to {3}, ONLY {3} key words per phrase:\n
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
    
    PROMPT += ''' \nYou are not alowed to use the following subjects in the phrases you are going to generate\n'''

    for subject in subjects:
        PROMPT += f'{subject}\n'


    new_prompt = eng.get_elements(PROMPT)

    ideas.append(new_prompt)

print(ideas)

checker = False
not_repeated = []
for idea in ideas:
    for subject in subjects:
        if subject.upper() in idea.upper():
            checker = True
            break
    if checker == False:
        not_repeated.append(idea)
    checker = False


print(not_repeated)

EXTRACT_PROMPT = f'''Extract the main characters of the following phrases:\n'''
              
for phrase in not_repeated:
    EXTRACT_PROMPT += f'{phrase}\n'

time.sleep(30)

new_prompts = eng.get_elements(EXTRACT_PROMPT)

print(new_prompts)
