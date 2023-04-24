import base64
import os
from random import sample
from time import sleep

import openai
import replicate


from prompt_engine.img_engineering import *

class GameObj:

    prompt:str = None
    full_prompt:str = None
    format:str = None
    bytestream:bytes = None
    encoded:bool = None

    def __init__(self, prompt, format, bytestream, full_prompt='') -> None:

        self.prompt = prompt
        self.full_prompt = full_prompt
        self.bytestream = bytestream
        self.format = format
        self.encoded = False

    def save(self, save_dir:str) -> None:

        if self.encoded:
            save_format = 'b64'
            file_name = 'img_' + self.format + '_' + "_".join(self.prompt.split(" "))
        else:
            save_format = self.format
            file_name = "_".join(self.prompt.split(" "))
        
        #go to images folder
        path = os.getcwd()
        os.chdir(save_dir)

        #write the decoded data back to original format in  file
        img_file = open(f'{file_name}.{save_format}', 'wb')
        img_file.write(self.bytestream)
        img_file.close()

        os.chdir(path) #back to root

    def encode_b64(self) -> None:
        if not self.encoded:
            self.bytestream = base64.b64encode((self.bytestream))
            self.encoded = True
        
    def decode_b64(self) -> None:
        if self.encoded:
            self.bytestream = base64.b64decode((self.bytestream))
            self.encoded = False

    def to_string(self) -> str:
        return self.bytestream.decode("utf-8")
    
    def to_png(self) -> None:
        pass

    def to_jpeg(self) -> None:
        pass


class ImagePrompt:
    base_prompt:str = None
    subjects:list[str] = None
    adjectives:list[str] = None
    color_palett:list[str] = None
    lighting:list[str] = None
    artists:list[str] = None
    art_stile:list[str] = None
    details:list[str] = None
    base_artists:str = None

    def __init__(self, base_prompt) -> None:
        self.base_prompt = base_prompt
        self.base_artists = 'art by artgerm and greg rutkowski and alphonse mucha'
        self.details = ['intricate', 'elegant', 'highly detailed', 'digital painting', 'artstation', 'concept art', 'smooth', 'sharp focus', '8k']
    
    
    def get_subjects(self, num_subj:int, subj_list_path:str = None,
                      adjctives:list[str] = None, color_paletts:list[str] = None, artists:list[str] = None) -> None:
        
        prompt = add_subjects_prpt(base_prompt=self.base_prompt, 
                                   num_subj=num_subj, 
                                   subj_list_path=subj_list_path, 
                                   adjctives=adjctives, 
                                   color_paletts=color_paletts, 
                                   artists=artists)

        subjects = get_elements(prompt)

        subjects = subjects.split('\n')

        for i in range(len(subjects)):
            subjects[i] = subjects[i].split('. ')[1]

        print(subjects)

        self.subjects = subjects

    def get_adjectives(self, num_adj:int, adj_list_path:str = None,
                    subjects:list[str] = None, color_paletts:list[str] = None, artists:list[str] = None) -> None:
    
        prompt = add_adjective_ppt(base_prompt=self.base_prompt, 
                                num_adj=num_adj, 
                                adj_list_path=adj_list_path, 
                                subjects=subjects, 
                                color_paletts=color_paletts, 
                                artists=artists)

        adjectives = get_elements(prompt)

        if adj_list_path is None:
            
            if adjectives[0].isdigit():
                adjectives = adjectives.split('\n')
                for i in range(len(adjectives)):
                    adjectives[i] = adjectives[i].split('. ')[1]
            else:
                adjectives = adjectives.split(', ')
               
        else:
            adjectives = adjectives.split(', ')

        print(adjectives)

        self.adjectives = adjectives

    def get_color_palett(self, num_pal:int, palett_list_path:str = None,
                    subjects:list[str] = None, adjctives:list[str] = None, artists:list[str] = None) -> None:

        num = num_pal
        if num ==2:
            num += 1

        prompt = add_color_prpt(base_prompt=self.base_prompt, 
                                num_pal=num, 
                                palett_list_path=palett_list_path, 
                                subjects=subjects, 
                                adjctives=adjctives, 
                                artists=artists)

        color_palett = get_elements(prompt)

        if palett_list_path is not None:
            if num_pal == 1:
                color_palett = [color_palett]
            
            elif num_pal in (2,3,4):
                color_palett = color_palett.split(', ')

            elif num_pal > 4:
                color_palett = color_palett.split('\n')
                for i in range(len(color_palett)):
                    color_palett[i] = color_palett[i].split('. ')[1]
        else:
            color_palett = color_palett.split('\n')
            for i in range(len(color_palett)):
                color_palett[i] = color_palett[i].split('. ')[1]


        print(color_palett)

        self.color_palett = color_palett

    def get_lighting(self, num_lights:int, lights_list_path:str, 
                    adjctives:list[str] = None, artists:list[str] = None, subjects:list[str] = None) -> None:
        
        prompt = add_lighting_prpt(base_prompt=self.base_prompt,
                                   num_lights=num_lights,
                                   lights_list_path=lights_list_path,
                                   adjctives=adjctives,
                                   artists=artists,
                                   subjects=subjects)
        
        lights = get_elements(prompt)

        lights = lights.split('\n')

        self.lighting = lights
        
        print(lights)
        
    def get_artists(self, num_artists:int, artist_list_path:str = None,
                    adjctives:list[str] = None, color_paletts:list[str] = None, subjects:list[str] = None) -> None:

        prompt = add_artist_prpt(base_prompt=self.base_prompt, 
                        num_artists=num_artists, 
                        artist_list_path=artist_list_path, 
                        subjects=subjects, 
                        color_paletts=color_paletts, 
                        adjctives=adjctives)

        artists = get_elements(prompt)

        if artist_list_path is not None:
            if num_artists == 1:
                artists = [artists]
            else:
                artists = artists.split('\n')
                try:
                    for i in range(len(artists)):
                        artists[i] = artists[i].split('. ')[1]
                except:
                    pass
            
        else:
            if num_artists == 1:
                artists = [artists]
            else:
                artists = artists.split('\n')
                try:
                    for i in range(len(artists)):
                        artists[i] = artists[i].split('. ')[1]
                except:
                    pass

        print(artists)

        self.artists = artists

    def final_prpt(self,k_subj:int=0,k_adj:int=0,k_light=0,k_color:int=0,k_artists:int=0) -> str:
        prompt = self.base_prompt
        
        #ADD ADJECTIVES
        if k_adj > 0 and k_adj <= len(self.adjectives):
            rand_adjs = sample(self.adjectives, k=k_adj)
            for adj in rand_adjs:
                prompt += ', ' + adj
        elif k_adj == 0:
            pass
        else:
            raise Exception(f'invalid k_adj: {k_adj}, {self.adjectives}')
        
        #ADD LIGHTING
        if k_light > 0 and k_light <= len(self.adjectives):
            rand_lights = sample(self.lighting, k=k_light)
            for light in rand_lights:
                prompt += ', ' + light
        elif k_light == 0:
            pass
        else:
            raise Exception(f'invalid k_light: {k_light}, {self.adjectives}')
        
        #ADD DETAILS
        for detail in self.details:
            prompt += ', ' + detail
        
        #ADD COLOR PALETT
        if k_color > 0 and k_color <= len(self.color_palett):
            prompt += ', Color palett: ' 
            rand_colors = sample(self.color_palett, k=k_color)
            for color in rand_colors:
                prompt += color + ', '

            prompt = prompt[:-2]
        elif k_color == 0:
            pass
        else:
            raise Exception(f'invalid k_color: {k_color}, {self.color_palett}')

        #ADD ARTISTS
        if k_artists > 0 and k_artists <= len(self.artists):
            rand_artists = sample(self.artists, k=k_artists)
            for artist in rand_artists:
                prompt += ', Art by ' + artist
        elif k_artists == 0:
            pass
        else:
            raise Exception(f'invalid k_artists: {k_artists}, {self.artists}')
        

        return prompt
