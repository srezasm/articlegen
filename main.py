from googlesearch import search
import requests
import justext
import openai
from utils import *


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
        print(
            'Please enter your OpenAI API key in the'
            'configs.yml and restart the program'
        )
        exit()

    openai.api_key = open_ai_key
    reseponse = openai.Completion.create(
        model='gpt-3.5-turbo',
        prompt='I want you to be my writing assistant. write an short article about sunrise:\n'
    )


    # Get search query
    query = ''
    while not query:
        query = cinput('Please enter your search query: ', bcolors.OKBLUE)

    # # Get specific websites
    # cprint('Enter websites or enter blank', bcolors.OKBLUE)
    # while True:
    #     domain = input()

    #     if not domain:
    #         break
    #     if not is_valid_domain(domain):
    #         cprint('Invalid website', bcolors.FAIL)
    #         continue

    #     query += f' site:{domain}'

    # Exclude websites
    exclutions = get_exclutions()
    for e in exclutions:
        query += f' -inurl:{e}'

    loading()

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

        sl = 'English'
        if lang == 'fa':
            sl = 'Persian'

        main_c = justext.justext(
            get_result.content, length_low=2, length_high=300,
            stoplist=justext.get_stoplist(sl),
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
                prompt='I want you to be my writing assistant. Given the following paragraphs, remove the unrelative sentences and write a product description in persian language\n\n' + '\n'.join(page_content),
                # prompt=get_prompt('webpage', '\n'.join(page_content)),
                # TODO: check the arguments
                # temperature=0.7,
                # max_tokens=1000,
                # top_p=1.0,
                # frequency_penalty=0.0,
                # presence_penalty=0.0
            )
            # TODO: check response
            contents.extend(reseponse)

    # write a short article with given content.
    # I want you to be my online shop content creator. Write a product description in
    # persian language with the following content.

    # Given the following description about a product, I need you to list the benefits
    # of the product in persian language

    # Given the following description about a product, I need you to write 3 questions
    # about the product in persian language

    # Given the following description about a product:
    # [description]
    # I need you to answer the following questions:
    # [questions]

    cprint('What\'s your desired content style?', bcolors.OKBLUE)
    cprint('e.g. storical, scientific etc.', bcolors.OKBLUE)
    cprint('Enter for normal cotent', bcolors.OKBLUE)
    opt = input('Enter an option: ')
    get_prompt('combine', '\n---\n'.join(contents))


if __name__ == '__main__':
    main()
