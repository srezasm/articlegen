from googlesearch import search
import requests
import justext
import openai
from utils import *
from prompts import *


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
    query = ''
    while not query:
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
    results = search(
        query, sleep_interval=5,
        num_results=10, lang=lang
    )
    results = [r for r in results]

    cprint(f'Found {len(results)} results', bcolors.OKBLUE)

    # Extracting the main content of pages
    contents = []
    for i, result in enumerate(results):
        cprint(f'Processing web page {i+1}', bcolors.OKGREEN, end='\r')
        try:
            get_result = requests.get(result, timeout=5)
        except requests.exceptions.Timeout as to_exception:
            print()
            cprint(to_exception, bcolors.FAIL)
            continue

        main_c = justext.justext(
            get_result.content, length_low=2, length_high=300,
            stoplist=justext.get_stoplist(lang),
        )

        for pragraph in main_c:
            page_content = []
            if pragraph.class_type != 'bad':
                if pragraph.is_heading:
                    page_content.append(f'## {pragraph.text}')
                else:
                    page_content.append(pragraph.text)

        reseponse = openai.Completion.create(
            model='gpt-3.5-turbo',
            prompt=webpage_prompt('\n'.join(page_content)),
            messages=[
                {
                    "name": "toyarticlegen",
                    "role": "user",
                    "content": webpage_prompt('\n'.join(page_content))
                }
            ],
        )

        contents.extend(reseponse['choices'][0]['message']['content'])

    print('Which style do you prefer?')
    styles = ['Normal', 'Storical', 'Creative', 'Review']
    for i, style in enumerate(styles):
        print(f'{i+1}. {style}')
    style = styles[int(input()) - 1]
    prompt = combine_prompt(style, '\n---\n'.join(contents))

    # TODO: add questions and answers

    cprint('What\'s your desired content style?', bcolors.OKBLUE)
    cprint('e.g. storical, scientific etc.', bcolors.OKBLUE)
    cprint('Enter for normal cotent', bcolors.OKBLUE)
    opt = input('Enter an option: ')
    get_prompt('combine', '\n---\n'.join(contents))


if __name__ == '__main__':
    main()
