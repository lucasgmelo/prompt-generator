from pymongo import MongoClient, collection

from datetime import datetime
import time
import openai
import main
from objects import Image


def insert_prompts(mongo_collection : collection.Collection):

    start_time = time.perf_counter_ns()
    
    prompt_imgs:list[Image] = main.imagine(1)

    insert_list = []
    for prompt in prompt_imgs:
        prompt.decode_b64()

        insert = {
            "prompt": prompt.prompt,
            "img_b64": prompt.bytstream,      
            "dt_altr" : datetime.utcnow()
        }

        insert_list.append(insert)

    result = mongo_collection.insert_many(insert_list)

    end_time = (time.perf_counter_ns() - start_time)/ 10**9 # tempo de execução em segundos

    print(end_time)


if __name__ == '__main__':

    client = MongoClient("mongodb+srv://jlca:AmJPBObKQ2W7Kpk5@prompt-io-test-cluster.3mhmlsh.mongodb.net/?retryWrites=true&w=majority")
    db = client.get_database('main')

    PROMPTS_COLECTION = db.prompts_info

    OPENAI_API_KEY = "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"

    openai.api_key = OPENAI_API_KEY
    
    insert_prompts(PROMPTS_COLECTION)
