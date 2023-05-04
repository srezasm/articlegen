from googlesearch import search
import requests
import justext
import openai
from urllib.parse import urlparse
from utils import *
from prompts import *
import docx
import datetime
from os.path import join


def main():
    cprint('╭━━━╮ ╭╮    ╭╮     ╭━━━╮             ╭╮\n'
           '┃╭━╮┃╭╯╰╮   ┃┃     ┃╭━╮┃            ╭╯╰╮\n'
           '┃┃ ┃┣┻╮╭╋┳━━┫┃╭━━╮ ┃┃ ╰╋━━┳━╮╭━━┳━┳━┻╮╭╋━━┳━╮\n'
           '┃╰━╯┃╭┫┃┣┫╭━┫┃┃┃━┫ ┃┃╭━┫┃━┫╭╮┫┃━┫╭┫╭╮┃┃┃╭╮┃╭╯\n'
           '┃╭━╮┃┃┃╰┫┃╰━┫╰┫┃━┫ ┃╰┻ ┃┃━┫┃┃┃┃━┫┃┃╭╮┃╰┫╰╯┃┃\n'
           '╰╯ ╰┻╯╰━┻┻━━┻━┻━━╯ ╰━━━┻━━┻╯╰┻━━┻╯╰╯╰┻━┻━━┻╯\n', bcolors.HEADER)

    # Check OpenAI API Key
    open_ai_key = get_open_ai_key()
    if not open_ai_key:
        cprint(
            'Please enter your OpenAI API key in the'
            ' configs.yml and restart the program', bcolors.FAIL
        )
        exit()
    openai.api_key = open_ai_key

    # Get search query
    query = cinput('Please enter your search query: ', bcolors.OKBLUE)

    # Exclude websites
    exclutions = get_exclutions()
    for e in exclutions:
        query += f' -inurl:{e}'

    cprint(f'Googling...', bcolors.OKGREEN, end='\r')

    # Detect query language
    lang = 'fa'
    if query[0] in list(map(chr, range(65, 91))) + list(map(chr, range(97, 123))):
        lang = 'en'

    # Google search
    try:
        results = search(
            query, sleep_interval=5,
            num_results=10, lang=lang, advanced=True
        )
        urls = [result.url for result in results]
    except Exception as e:
        cprint(e, bcolors.FAIL)
        exit()

    cprint(f'Found {len(urls)} results', bcolors.OKBLUE)

    # Extracting the main content of pages
    contents = []
    for i, url in enumerate(urls):
        cprint(f'Processing web page {i+1}', bcolors.OKGREEN, end='\r')
        try:
            get_result = requests.get(url, timeout=5)
        except requests.exceptions.Timeout as to_exception:
            print()
            cprint(to_exception, bcolors.FAIL)
            continue

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

        if not page_content:
            print()
            cprint(
                f'No useful content found in {urlparse(url).netloc}.', bcolors.WARNING)
            continue

        try:
            cprint(
                f'Summarizing {i+1} web page into an article', bcolors.OKGREEN, end='\r')

            reseponse = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {
                        "role": "system",
                        "content": webpage_prompt('\n'.join(page_content))
                    }
                ],
                stop=None,
                temperature=0.7
            )

            contents.append(reseponse.choices[0].message.content)
        except Exception as e:
            cprint(e, bcolors.FAIL)
            exit()

    # Combine articles
    print('Which style do you prefer?')
    styles = ['Normal', 'Storical', 'Creative', 'Review']
    for i, style in enumerate(styles):
        print(f'{i+1}. {style}')
    style = styles[int(input()) - 1]
    prompt = combine_prompt(style, '\n---\n'.join(contents))

    cprint('Combining articles...', bcolors.OKGREEN, end='\r')
    reseponse = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ],
        stop=None,
        temperature=0.7
    )

    doc = docx.Document()
    doc.add_paragraph(reseponse.choices[0].message.content)
    doc_name = join(
        'docs', f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.docx')
    doc.save(doc_name)
    cprint(f'Your article is ready in {doc_name}', bcolors.OKBLUE)


if __name__ == '__main__':
    main()
