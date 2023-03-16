
import base64
import os

class Image:

    prompt:str = None
    format:str = None
    bytstream:str = None
    encoded:bool = None

    def __init__(self, prompt, format, bytstream) -> None:

        self.prompt = prompt
        self.bytstream = bytstream
        self.format = format
        self.encoded = False

    def save(self, save_dir:str) -> None:

        if self.encoded:
            save_format = 'b64'
        else:
            save_format = self.format

        file_name = "_".join(self.prompt.split(" "))
        
        #go to images folder
        path = os.getcwd()
        os.chdir(save_dir)

        #write the decoded data back to original format in  file
        img_file = open(f'{file_name}.{save_format}', 'wb')
        img_file.write(self.bytstream)
        img_file.close()

        os.chdir(path) #back to root

    def encode_b64(self) -> None:
        if not self.encoded:
            self.bytstream = base64.b64encode((self.bytstream))
            self.encoded = True
        
    def decode_b64(self) -> None:
        if self.encoded:
            self.bytstream = base64.b64decode((self.bytstream))
            self.encoded = False

    def to_png(self) -> None:
        pass

    def to_jpeg(self) -> None:
        pass

