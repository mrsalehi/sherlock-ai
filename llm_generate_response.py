import os
import time
import sys
import openai
import numpy as np
from PIL import Image
import requests
import pyarrow as pa

from multiprocessing import Pool
from tqdm import tqdm

from PIL import Image, ImageDraw

from openai.error import RateLimitError, ServiceUnavailableError
import backoff

# class MultiProcessCaller:
#     @staticmethod
#     def call_multi_process(fn, data, num_processes=8):
#         result = []
#         p = Pool(num_processes)
#         pbar = tqdm(total=len(data))
#         for i in p.imap_unordered(fn, data):
#             if i is not None:
#                 result.append(i)
#             pbar.update()

#         return result

# def read_img(filepath):
#     if os.path.isfile(filepath):
#         raw_image = Image.open(filepath)
#     else:
#         raw_image = Image.open(requests.get(filepath, stream=True).raw)
#     raw_image = raw_image.convert("RGB")
    
#     return raw_image


# def read_arrow(path):
#     table = pa.ipc.RecordBatchFileReader(
#         pa.memory_map(path, "r")
#     ).read_all()
#     return table
    
# def highlight_region(image, bboxes):
#     image = image.convert('RGBA')
#     overlay = Image.new('RGBA', image.size, '#00000000')
#     draw = ImageDraw.Draw(overlay, 'RGBA')
#     for bbox in bboxes:
#         print(bbox)
#         if isinstance(bbox, dict):
#             x = bbox['left']
#             y = bbox['top']
#             draw.rectangle([(x, y), (x+bbox['width'], y+bbox['height'])],
#                             fill='#ff05cd3c', outline='#05ff37ff', width=3)
#         else:
#             draw.rectangle([(bbox[0], bbox[1]), (bbox[2], bbox[3])],
#                             fill='#ff05cd3c', outline='#05ff37ff', width=3)
#     image = Image.alpha_composite(image, overlay)
#     return image.convert('RGB')

# class OpenaiAPI:

#     def __init__(self, api_key) -> None:
#         openai.api_key = api_key

    
@backoff.on_exception(backoff.expo, (RateLimitError, ServiceUnavailableError), max_time=60)
def complete_chat(messages, model='gpt-3.5-turbo', max_tokens=256,  num_log_probs=None,  n=1, 
                top_p = 1.0, temperature=1.0, stop = None, echo=True,
                frequency_penalty = 0., presence_penalty=0. ):

    # call GPT-3 API until result is provided and then return it
    response = None
    c = 0
    while c < 100:
        try:
            response = openai.ChatCompletion.create(messages=messages, model=model, max_tokens=max_tokens, temperature=temperature,
                                                    stop=stop, n=n, top_p=float(top_p),
                                                frequency_penalty = frequency_penalty,
                                                presence_penalty= presence_penalty)
            return response
        except:
            error = sys.exc_info()[0]
            if error == openai.error.InvalidRequestError:
                print(f"InvalidRequestError\nQuery:\n\n{messages}\n\n")
                print(sys.exec_info())
                break
            else:
                print('Error:', sys.exc_info())
                time.sleep(5)
                c+=1

    return response