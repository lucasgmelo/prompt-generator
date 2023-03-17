import openai       #openAI API

def chatgpt_gen_prompts_list(num_imgs:int)->list[str]:

    if num_imgs < 1:
         raise Exception('You can only generate 1 or more images')

    elif num_imgs == 1:
        PROMPT = f'''make only {num_imgs} more small phrase like the following:\n

                    bears in pijamas\n
                    icecream fight\n
                    elon musk in a jar\n
                    sushi vs godzila\n
                    goku in mario kart'''
         
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

                    bears in pijamas\n
                    icecream fight\n
                    elon musk in a jar\n
                    sushi vs godzila\n
                    goku in mario kart'''

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


if __name__ == "__main__":

    OPENAI_API_KEY = "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"

    openai.api_key = OPENAI_API_KEY

    prompts_list = chatgpt_gen_prompts_list(1)
    print(prompts_list)

    print("SUCCESS")