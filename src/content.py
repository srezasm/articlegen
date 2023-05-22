import justext
import requests
import openai
from cli import *
import configs
import docx
import datetime
from os import path, listdir
import joblib
import hashlib
from urllib.parse import urlparse


def make_content(urls: list[str], lang: str):
    contents = []
    for url in urls:
        purl = urlparse(url)
        purl = f"{purl.netloc}/{purl.path.strip('/')}"
        hash = hashlib.sha256(purl.encode('utf-8')).hexdigest()
        
        cfile_name = hash + '.joblib'
        if cfile_name in listdir(configs.cache_path):
            contents.extend(joblib.load(
                path.join(configs.cache_path, cfile_name)))
        else:
            content = justext_extract(url, lang)
            contents.extend(content)
            joblib.dump(content, path.join(configs.cache_path, cfile_name))
    
    contents = '\n'.join(contents)
    contents = ai_content_create(contents)
    write_doc(contents)


def justext_extract(url: str, lang: str) -> list[str]:
    try:
        get_result = requests.get(url, timeout=5)

    except requests.exceptions.Timeout:
        cprint('Please check your internet connectivity.', bcolors.FAIL)
        return None

    except Exception as e:
        cprint(e, bcolors.FAIL)
        return None

    main_c = justext.justext(
        get_result.content,
        stoplist=justext.get_stoplist(lang),
    )

    page_content = []
    for pragraph in main_c:
        if pragraph.class_type != 'bad':
            if pragraph.is_heading:
                page_content.append(f'## {pragraph.text}')
            else:
                page_content.append(pragraph.text)

    return page_content


def ai_content_create(content: str, model: str = 'gpt-3.5-turbo') -> str:
    try:
        reseponse = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": content
                }
            ],
            stop=None,
            temperature=0.7
        )

    except requests.ConnectionError as e:
        cprint(e, bcolors.FAIL)
        return None

    except Exception as e:
        cprint(e, bcolors.FAIL)
        return None

    return str(reseponse.choices[0].message.content)


def write_doc(content: str):
    doc = docx.Document()
    doc.add_paragraph(content)
    doc_name = path.join(
        configs.docs_path, f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.docx')
    doc.save(doc_name)
    cprint(f'Your article is ready in {doc_name}', bcolors.OKBLUE)
