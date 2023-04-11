import os
import openai
from time import sleep

def complement_description(adjctives:list[str] = None, color_paletts:list[str] = None, artists:list[str] = None,
                           subjects:list[str] = None) -> str:
    complement = None

    if subjects is not None:
        subj_complement = f'extra elements in the scene: ['
        for subj in subjects:
            subj_complement += subj + ', '

        subj_complement = subj_complement[:-2] + ']'

        complement += subj_complement + '\n'

    if adjctives is not None:
        adj_complement = f'image qualifiers: ['
        for adj in adjctives:
            adj_complement += adj + ', '

        adj_complement = adj_complement[:-2] + ']'

        complement += adj_complement + '\n'

    if color_paletts is not None:
        color_complement = f'color palett: ['
        for pallet in color_paletts:
            color_complement += pallet + ', '

        color_complement = color_complement[:-2] + ']'

        complement += color_complement + '\n'

    if artists is not None:
        artist_complement = f'artists: ['
        for artist in artists:
            artist_complement += artist + ', '

        artist_complement = artist_complement[:-2] + ']'

        complement += artist_complement + '\n'

    return complement

def add_subjects_prpt(base_prompt:str, num_subj:int, subj_list_path:str = None,
                      adjctives:list[str] = None, color_paletts:list[str] = None, artists:list[str] = None) -> str:

    complement = complement_description(adjctives=adjctives, color_paletts=color_paletts, artists=artists)
    
    if subj_list_path is None:
        prompt = f'list exactly [{num_subj}] subjects, not explicited on the following theme, that must figure in an image with:\n'
        prompt +=  f'theme: [{base_prompt}]\n'

        if complement is not None:
            prompt += complement

    elif os.path.exists(subj_list_path):
        prompt = f'list exactly [{num_subj}] subjects of the following list, not explicited on the following theme, that must figure in an image with:\n'
        prompt +=  f'theme: [{base_prompt}]\n'

        if complement is not None:
            prompt += complement

        with open(subj_list_path, 'r') as f:
            for line in f.readlines():
                prompt +=  line 
        f.close()

    else:
        raise Exception(f'path not found: {subj_list_path}')

    prompt +=  '\n\nDO NOT EXPLAIN THE REASONS OF THE CHOICE'
    prompt +=  '\nJUST OUTPUT THE NAME OF THE SUBJECTIVES'

    return prompt
   
def add_adjective_ppt(base_prompt:str, num_adj:int, adj_list_path:str = None, 
                     color_paletts:list[str] = None, artists:list[str] = None, subjects:list[str] = None) -> str:
    
    complement = complement_description(color_paletts=color_paletts, artists=artists, subjects=subjects)

    if adj_list_path is None:
        prompt = f'''list exactly [{num_adj}] adjectives that most matches the description of an image described by:\n'''
        prompt +=  f'theme: [{base_prompt}]\n'

        if complement is not None:
            prompt += complement

    elif os.path.exists(adj_list_path):
        prompt = f'''select exactly [{num_adj}] adjectives of the following list that most matches the description of an image described by:\n'''
        prompt +=  f'theme: [{base_prompt}]\n'

        if complement is not None:
            prompt += complement

        with open(adj_list_path, 'r') as f:
            for line in f.readlines():
                prompt +=  line 
        f.close()

    else:
        raise Exception(f'path not found: {adj_list_path}')
    
    prompt +=  '\n\nDO NOT EXPLAIN THE REASONS OF THE CHOICE'
    prompt +=  '\nJUST OUTPUT THE NAME OF THE ADJECTIVES'

    return prompt

def add_color_prpt(base_prompt:str, num_pal:int, palett_list_path:str = None,
                adjctives:list[str] = None, artists:list[str] = None, subjects:list[str] = None) -> str:

    complement = complement_description(adjctives=adjctives, artists=artists, subjects=subjects)
    
    if palett_list_path is None:
        prompt = f'NAME exactly {num_pal} color paletts that would enhance the aestetics of an image described by:\n'
        prompt +=  f'theme: [{base_prompt}]\n'

        if complement is not None:
            prompt += complement

    elif os.path.exists(palett_list_path):
        prompt = f'SELECT exactly {num_pal} color paletts from the following list that would enhance the aestetics of an image described by:\n'
        prompt +=  f'theme: [{base_prompt}]\n'

        if complement is not None:
            prompt += complement

        with open(palett_list_path, 'r') as f:
            for line in f.readlines():
                prompt +=  line 
        f.close()

    else:
        raise Exception(f'path not found: {palett_list_path}')

    prompt +=  '\n\nDO NOT EXPLAIN THE REASONS OF THE CHOICE'
    prompt +=  '\nJUST OUTPUT THE NAME OF THE COLOR PALLETS'

    return prompt

def add_lighting_prpt(base_prompt:str, num_lights:int, lights_list_path:str, 
                      adjctives:list[str] = None, artists:list[str] = None, subjects:list[str] = None) -> str:
    
    if os.path.exists(lights_list_path):

        prompt = f'SELECT exactly {num_lights} render/lighting properties from the following list that would enhance the aestetics of an image described by:\n'
        prompt += f'theme '
        prompt +=  f'theme: [{base_prompt}]\n'

        complement = complement_description(adjctives=adjctives, artists=artists, subjects=subjects)
        if complement is not None:
            prompt += complement

        with open(lights_list_path, 'r') as f:
            for line in f.readlines():
                prompt +=  line 
        f.close()

    else:
        raise Exception(f'path not found: {lights_list_path}')
    
    prompt +=  '\n\nDO NOT EXPLAIN THE REASONS OF THE CHOICE'
    prompt +=  '\nJUST OUTPUT THE NAME OF THE PROPERTIES'
    prompt +=  '\nOUTPUT ONE NAME PER LINE'

    return prompt

def add_artist_prpt(base_prompt:str, num_artists:int, artist_list_path:str = None,
                    adjctives:list[str] = None, color_paletts:list[str] = None, subjects:list[str] = None) -> str:
    
    complement = complement_description(adjctives=adjctives, color_paletts=color_paletts, subjects=subjects)
    
    if artist_list_path is None:
        prompt = f'NAME exactly [{num_artists}] artists that would make an astonishng image with:'
        prompt +=  f'theme: [{base_prompt}]\n'

        if complement is not None:
            prompt += complement

    elif os.path.exists(artist_list_path):
        prompt = f'select exactly [{num_artists}] artists of the following list that would make an astonishng image with:'
        prompt +=  f'theme: [{base_prompt}]\n'

        if complement is not None:
            prompt += complement

        with open(artist_list_path, 'r') as f:
            for line in f.readlines():
                prompt +=  line 
        f.close()

    else:
        raise Exception(f'path not found: {artist_list_path}')

    prompt +=  '\n\nDO NOT EXPLAIN THE REASONS OF THE CHOICE'
    prompt +=  '\nJUST OUTPUT THE NAME OF THE ARTISTS'
    prompt +=  '\nOUTPUT ONE NAME PER LINE'

    return prompt

def get_elements(prompt) -> list[str]:
    error = True
    while error:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[{"role": "user", "content": prompt}]
            )
            error = False
        except:
            print('FAILED TO GET ELEMENTS')
            sleep(20)
            continue

    content = response["choices"][0]["message"]["content"]

    print(content)

    return content


