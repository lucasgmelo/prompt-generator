import openai       #openAI API

def chatgpt_gen_prompts_list(num_imgs:int)->list[str]:

    if num_imgs > 1:
        PROMPT = f'''make {num_imgs} more small phrases like the following:\n

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

        # remover indices gerados no gpt3
        i = 0
        for prompt in new_prompts:
            prompt = prompt.split(' ')
            prompt.pop(0)
            prompt = " ".join(prompt)
            new_prompts[i] = prompt
            i += 1
    
    elif num_imgs == 1:
        PROMPT = f'''make {num_imgs} more small phrase like the following:\n

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

    return new_prompts


if __name__ == "__main__":

    OPENAI_API_KEY = "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"

    openai.api_key = OPENAI_API_KEY

    prompts_list = chatgpt_gen_prompts_list(1)
    print(prompts_list)

    print("SUCCESS")