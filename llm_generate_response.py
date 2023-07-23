import os
import time
import sys
import openai
from prompts import SYSTEM_PROMPT, USER_PROMPT

from multiprocessing import Pool
from tqdm import tqdm

from openai.error import RateLimitError, ServiceUnavailableError
import backoff


# openai.api_key = os.environ.get")
openai.api_key = "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"

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
                top_p = 1.0, temperature=0.5, stop = None, echo=True,
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

    
def generate_response(query, documents_doc, documents_discord, model='gpt-3.5-turbo'):
    """
    gets the query as a string and a set of documents as a list of strings and generates the answer
    based on the documents
    """
    doc_string_documentation = ""
    for doc in documents_doc:
        doc_string_documentation += f"DOCUMENT: {doc}\n\n"
    
    doc_string_discord = ""
    for doc in documents_discord:
        doc_string_discord += f"DISCORD: {doc}\n\n"  

    prompt = SYSTEM_PROMPT + USER_PROMPT.format(query, doc_string_documentation, doc_string_discord)
    
    messages = [{
        "role": "system",
        "content": SYSTEM_PROMPT
    }, {
        "role": "user",
        "content": prompt
    }]

    response = complete_chat(messages, model=model, max_tokens=1500)
    print(response.choices[0]["message"]["content"])