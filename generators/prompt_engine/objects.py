import base64
import os

import openai
import replicate

class GameObj:

    prompt:str = None
    format:str = None
    bytestream:bytes = None
    encoded:bool = None

    def __init__(self, prompt, format, bytestream) -> None:

        self.prompt = prompt
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


